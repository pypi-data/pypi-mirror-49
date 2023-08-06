from __future__ import absolute_import
from pony.py23compat import PY2, imap, basestring, buffer, int_types, unicode

import os.path, sys, re, json
import sqlite3 as sqlite
from decimal import Decimal
from datetime import datetime, date, time, timedelta
from random import random
from time import strptime
from threading import Lock
from uuid import UUID
from binascii import hexlify
from functools import wraps

from pony.orm import core, dbschema, dbapiprovider
from pony.orm.core import log_orm
from pony.orm.ormtypes import Json, TrackedArray, TrackedValue
from pony.orm.sqltranslation import SQLTranslator, StringExprMonad
from pony.orm.sqlbuilding import SQLBuilder, join, make_unary_func, Param
from pony.orm.dbapiprovider import DBAPIProvider, Pool, wrap_dbapi_exceptions, Converter
from pony.orm.dbschema import DBSchema
from pony.utils import datetime2timestamp, timestamp2datetime, absolutize_path, localbase, throw, reraise, \
    cut_traceback_depth

from azure.cosmos import cosmos_client
from azure.cosmos.errors import HTTPFailure
from json import JSONDecodeError

class SqliteExtensionUnavailable(Exception):
    pass


NoneType = type(None)


class SQLiteForeignKey(dbschema.ForeignKey):
    def get_create_command(foreign_key):
        assert False  # pragma: no cover


class SQLiteSchema(DBSchema):
    dialect = 'SQLite'
    named_foreign_keys = False
    fk_class = SQLiteForeignKey


def make_overriden_string_func(sqlop):
    def func(translator, monad):
        sql = monad.getsql()
        assert len(sql) == 1
        translator = monad.translator
        return StringExprMonad(monad.type, [sqlop, sql[0]])
    func.__name__ = sqlop
    return func


class CosmosDBTranslator(SQLTranslator):
    dialect = 'SQLite'


class CosmosDBBuilder(SQLBuilder):
    dialect = 'CosmosDB'
    least_func_name = 'min'
    greatest_func_name = 'max'

    def __init__(builder, provider, ast):
        builder.json1_available = provider.json1_available
        SQLBuilder.__init__(builder, provider, ast)

    def SELECT_FOR_UPDATE(builder, nowait, skip_locked, *sections):
        assert not builder.indent
        return builder.SELECT(*sections)

    def DELETE(builder, alias, from_ast, where=None):  # see if ALIAS

        sections = []
        sections.append(['ALL', '*'])
        sections.append(from_ast)
        sections.append(where)

        delete = []

        delete.extend(['DELETE ', builder.SELECT(*sections)])
        return delete

    def UPDATE(builder, table_name, pairs, where=None):

        sections = []
        sections.append(['ALL', '*'])
        sections.append(['FROM',[None, None, table_name]])
        sections.append(where)

        updated = []
        updated.append('{')
        for name, param in pairs:
            if param[2].py_type in (str, datetime):
                updated.extend(['"%s":"' % name, builder(param), '"', ','])
            else:
                updated.extend(['"%s":' % name, builder(param), ','])

        updated[-1] = '}'
        updated = [' UPDATED '] + updated

        query_update = ['UPDATED '] + builder.SELECT(*sections) + updated

        return query_update

    def SELECT(builder, *sections):

        from_clause = ['FROM c ']
        select_clause = ['SELECT']
        where_clause = ['WHERE']

        for section in sections:
            clause = section[0]

            if clause == 'FROM':
                doc_type = section[1][2]
                where_clause.append(' c["doc_type"]="%s"' % doc_type)
            elif clause in ('ALL', 'DISTINCT'):  # include this attributes in the SELECT clause
                if section[1] == '*':
                    select_clause.append(' * ')
                    continue
                for index in range(1, len(section)):
                    attribute = section[index][2]
                    select_clause.append(' c["%s"] ?? null,' % attribute)
                    if index == len(section) - 1:
                        remove_last_comma = ''.join(list(select_clause[-1])[:-1])
                        select_clause.pop()
                        select_clause.append('%s ' % remove_last_comma)
            elif clause == 'AGGREGATES':
                for index in range(1, len(section)):
                    agg_fun = section[index][0]
                    attribute = section[index][2][2]
                    select_clause.append(' VALUE %s(c["%s"]) ?? null' % (agg_fun, attribute))
                    if index != len(section) - 1:
                        select_clause.append(', ')
                select_clause.append(' ')
            elif clause == "WHERE":
                for index in range(1, len(section)):
                    operator = section[index][0]
                    fact1 = section[index][1]
                    fact2 = section[index][2]
                    if (fact1[1] != 0) or (fact2[1] != 1):  # because of the 1 = 0 ping to the database

                        cond = 'c["%s"]'

                        if fact1[0] == 'JSON_VALUE':
                            attribute = fact1[1][2]
                            cond = cond % attribute
                            for json_field in fact1[2]:
                                cond += '["%s"]' % json_field[1]
                        else:  # if is COLUMN
                            attribute = fact1[2]
                            cond = cond % attribute

                        if operator == 'IN':
                            where_clause.append(' AND %s IN (' % cond)
                            for i, v in enumerate(fact2):
                                value = v[1]
                                if isinstance(value, datetime):
                                    where_clause.append('"%s",' % value.strftime('%Y-%m-%d %H:%M:%S.%f'))
                                elif isinstance(value, str):
                                    where_clause.append('"%s",' % value)
                                else:
                                    where_clause.append('%s,' % value)

                            last = where_clause.pop()
                            last = last.replace(last[-1], ')')
                            where_clause.append(last)
                        else:
                            where_clause.append(' AND %s%s' % (cond, builder.translate_operator(operator)))

                            value_type = fact2[0]
                            value = fact2[1]

                            if value_type == 'PARAM':
                                converter = fact2[2]
                                if converter.py_type in (str, datetime):
                                    where_clause.extend(['"', Param(builder.paramstyle, value, converter), '"'])
                                else:
                                    where_clause.append(Param(builder.paramstyle, value, converter))
                            elif value_type == 'VALUE':
                                if isinstance(value, (str, datetime)):
                                    where_clause.append('"%s"' % value)
                                else:
                                    where_clause.append(value)

        query = []
        query.extend([select_clause, from_clause, where_clause])

        return query

    def translate_operator(builder, operator):
        operator_dict = {
            'EQ': "=",
            'NE': "<>",
            'LT': "<",
            'LE': "<=",
            'GT': ">",
            'GE': ">="
        }

        return operator_dict.get(operator, None)

    def INSERT(builder, table_name, columns, values, returning=None):

        sections = []
        sections.append(['ALL', '*'])
        sections.append(['FROM', [None, None, table_name]])
        where = ['WHERE']

        insert = ['INSERT {"doc_type":"%s"' % table_name]

        for i, att in enumerate(columns):
            if att != '_self':
                to_add_where = ['EQ', ['COLUMN', 's', att], values[i]]
                where.append(to_add_where)
            insert.append(', "%s":' % att)
            param_key = values[i][1]
            converter = values[i][2]
            if converter.py_type in (None, bool, int, float, list, Decimal, dict, Json):
                insert.append(Param(builder.paramstyle, param_key, converter))
            else:
                insert.extend(['"', Param(builder.paramstyle, param_key, converter), '"'])

        insert.append('}')

        sections.append(where)
        query = builder.SELECT(*sections)

        insert.extend([' INSERT ', query])

        return insert

    def TODAY(builder):
        return "date('now', 'localtime')"

    def NOW(builder):
        return "datetime('now', 'localtime')"

    def YEAR(builder, expr):
        return 'cast(substr(', builder(expr), ', 1, 4) as integer)'

    def MONTH(builder, expr):
        return 'cast(substr(', builder(expr), ', 6, 2) as integer)'

    def DAY(builder, expr):
        return 'cast(substr(', builder(expr), ', 9, 2) as integer)'

    def HOUR(builder, expr):
        return 'cast(substr(', builder(expr), ', 12, 2) as integer)'

    def MINUTE(builder, expr):
        return 'cast(substr(', builder(expr), ', 15, 2) as integer)'

    def SECOND(builder, expr):
        return 'cast(substr(', builder(expr), ', 18, 2) as integer)'

    def datetime_add(builder, funcname, expr, td):
        assert isinstance(td, timedelta)
        modifiers = []
        seconds = td.seconds + td.days * 24 * 3600
        sign = '+' if seconds > 0 else '-'
        seconds = abs(seconds)
        if seconds >= (24 * 3600):
            days = seconds // (24 * 3600)
            modifiers.append(", '%s%d days'" % (sign, days))
            seconds -= days * 24 * 3600
        if seconds >= 3600:
            hours = seconds // 3600
            modifiers.append(", '%s%d hours'" % (sign, hours))
            seconds -= hours * 3600
        if seconds >= 60:
            minutes = seconds // 60
            modifiers.append(", '%s%d minutes'" % (sign, minutes))
            seconds -= minutes * 60
        if seconds:
            modifiers.append(", '%s%d seconds'" % (sign, seconds))
        if not modifiers: return builder(expr)
        return funcname, '(', builder(expr), modifiers, ')'

    def DATE_ADD(builder, expr, delta):
        if isinstance(delta, timedelta):
            return builder.datetime_add('date', expr, delta)
        return 'datetime(julianday(', builder(expr), ') + ', builder(delta), ')'

    def DATE_SUB(builder, expr, delta):
        if isinstance(delta, timedelta):
            return builder.datetime_add('date', expr, -delta)
        return 'datetime(julianday(', builder(expr), ') - ', builder(delta), ')'

    def DATETIME_ADD(builder, expr, delta):
        if isinstance(delta, timedelta):
            return builder.datetime_add('datetime', expr, delta)
        return 'datetime(julianday(', builder(expr), ') + ', builder(delta), ')'

    def DATETIME_SUB(builder, expr, delta):
        if isinstance(delta, timedelta):
            return builder.datetime_add('datetime', expr, -delta)
        return 'datetime(julianday(', builder(expr), ') - ', builder(delta), ')'

    def RANDOM(builder):
        return 'rand()'  # return '(random() / 9223372036854775807.0 + 1.0) / 2.0'
    PY_UPPER = make_unary_func('py_upper')
    PY_LOWER = make_unary_func('py_lower')

    def FLOAT_EQ(builder, a, b):
        a, b = builder(a), builder(b)
        return 'abs(', a, ' - ', b, ') / coalesce(nullif(max(abs(', a, '), abs(', b, ')), 0), 1) <= 1e-14'

    def FLOAT_NE(builder, a, b):
        a, b = builder(a), builder(b)
        return 'abs(', a, ' - ', b, ') / coalesce(nullif(max(abs(', a, '), abs(', b, ')), 0), 1) > 1e-14'

    def JSON_QUERY(builder, expr, path):
        fname = 'json_extract' if builder.json1_available else 'py_json_extract'
        path_sql, has_params, has_wildcards = builder.build_json_path(path)
        return 'py_json_unwrap(', fname, '(', builder(expr), ', null, ', path_sql, '))'
    json_value_type_mapping = {unicode: 'text', bool: 'integer', int: 'integer', float: 'real'}

    def JSON_VALUE(builder, expr, path, type):
        func_name = 'json_extract' if builder.json1_available else 'py_json_extract'
        path_sql, has_params, has_wildcards = builder.build_json_path(path)
        type_name = builder.json_value_type_mapping.get(type)
        result = func_name, '(', builder(expr), ', ', path_sql, ')'
        if type_name is not None: result = 'CAST(', result, ' as ', type_name, ')'
        return result

    def JSON_NONZERO(builder, expr):
        return builder(expr), ''' NOT IN ('null', 'false', '0', '""', '[]', '{}')'''

    def JSON_ARRAY_LENGTH(builder, value):
        func_name = 'json_array_length' if builder.json1_available else 'py_json_array_length'
        return func_name, '(', builder(value), ')'

    def JSON_CONTAINS(builder, expr, path, key):
        path_sql, has_params, has_wildcards = builder.build_json_path(path)
        return 'py_json_contains(', builder(expr), ', ', path_sql, ',  ', builder(key), ')'

    def ARRAY_INDEX(builder, col, index):
        return 'py_array_index(', builder(col), ', ', builder(index), ')'

    def ARRAY_CONTAINS(builder, key, not_in, col):
        return ('NOT ' if not_in else ''), 'py_array_contains(', builder(col), ', ', builder(key), ')'

    def ARRAY_SUBSET(builder, array1, not_in, array2):
        return ('NOT ' if not_in else ''), 'py_array_subset(', builder(array2), ', ', builder(array1), ')'

    def ARRAY_LENGTH(builder, array):
        return 'py_array_length(', builder(array), ')'

    def ARRAY_SLICE(builder, array, start, stop):
        return 'py_array_slice(', builder(array), ', ', \
               builder(start) if start else 'null', ',',\
               builder(stop) if stop else 'null', ')'

    def MAKE_ARRAY(builder, *items):
        return 'py_make_array(', join(', ', (builder(item) for item in items)), ')'


class CosmosDBIntConverter(dbapiprovider.IntConverter):
    def sql_type(converter):
        attr = converter.attr
        if attr is not None and attr.auto: return 'INTEGER'  # Only this type can have AUTOINCREMENT option
        return dbapiprovider.IntConverter.sql_type(converter)


class CosmosDBDecimalConverter(dbapiprovider.DecimalConverter):
    inf = Decimal('infinity')
    neg_inf = Decimal('-infinity')
    NaN = Decimal('NaN')

    def sql2py(converter, val):
        try: val = Decimal(str(val))
        except: return val
        exp = converter.exp
        if exp is not None: val = val.quantize(exp)
        return val

    def py2sql(converter, val):
        if type(val) is not Decimal: val = Decimal(val)
        exp = converter.exp
        if exp is not None:
            if val in (converter.inf, converter.neg_inf, converter.NaN):
                throw(ValueError, 'Cannot store %s Decimal value in database' % val)
            val = val.quantize(exp)
        return str(val)


class CosmosDBDateConverter(dbapiprovider.DateConverter):
    def sql2py(converter, val):
        try:
            time_tuple = strptime(val[:10], '%Y-%m-%d')
            return date(*time_tuple[:3])
        except: return val

    def py2sql(converter, val):
        return val.strftime('%Y-%m-%d')


class CosmosDBTimeConverter(dbapiprovider.TimeConverter):
    def sql2py(converter, val):
        try:
            if len(val) <= 8: dt = datetime.strptime(val, '%H:%M:%S')
            else: dt = datetime.strptime(val, '%H:%M:%S.%f')
            return dt.time()
        except: return val

    def py2sql(converter, val):
        return val.isoformat()


class CosmosDBTimedeltaConverter(dbapiprovider.TimedeltaConverter):
    def sql2py(converter, val):
        return timedelta(days=val)

    def py2sql(converter, val):
        return val.days + (val.seconds + val.microseconds / 1000000.0) / 86400.0


class CosmosDBDatetimeConverter(dbapiprovider.DatetimeConverter):
    def sql2py(converter, val):
        try:
            return timestamp2datetime(val)
        except:
            return val

    def py2sql(converter, val):
        return datetime2timestamp(val)

class CosmosDBStrConverter(dbapiprovider.StrConverter):
    def val2dbval(converter, val, obj=None):
        return val.replace('\\\\', '\\')


class CosmosDBJsonConverter(dbapiprovider.JsonConverter):
    json_kwargs = {'separators': (',', ':'), 'sort_keys': True, 'ensure_ascii': False}

    def val2dbval(converter, val, obj=None):
        return json.dumps(val)

    def dbval2val(converter, dbval, obj=None):
        if isinstance(dbval, (int, bool, float, type(None), dict)):
            return dbval
        val = json.loads(dbval)
        if obj is None:
            return val
        return TrackedValue.make(obj, converter.attr, val)


def dumps(items):
    return json.dumps(items, **CosmosDBJsonConverter.json_kwargs)


class CosmosDBArrayConverter(dbapiprovider.ArrayConverter):
    array_types = {
        int: ('int', CosmosDBIntConverter),
        unicode: ('text', dbapiprovider.StrConverter),
        float: ('real', dbapiprovider.RealConverter)
    }

    def dbval2val(converter, dbval, obj=None):
        if not dbval: return None
        items = json.loads(dbval)
        if obj is None:
            return items
        return TrackedArray(obj, converter.attr, items)

    def val2dbval(converter, val, obj=None):
        return dumps(val)


class LocalExceptions(localbase):
    def __init__(self):
        self.exc_info = None
        self.keep_traceback = False


local_exceptions = LocalExceptions()


def keep_exception(func):
    @wraps(func)
    def new_func(*args):
        local_exceptions.exc_info = None
        try:
            return func(*args)
        except Exception:
            local_exceptions.exc_info = sys.exc_info()
            if not local_exceptions.keep_traceback:
                local_exceptions.exc_info = local_exceptions.exc_info[:2] + (None,)
            raise
        finally:
            local_exceptions.keep_traceback = False
    return new_func


class CosmosDBProvider(DBAPIProvider):
    dialect = 'CosmoDB'
    paramstyle = 'cosmosformat'
    local_exceptions = local_exceptions
    max_name_len = 1024

    dbapi_module = cosmos_client
    dbschema_cls = SQLiteSchema
    translator_cls = CosmosDBTranslator
    sqlbuilder_cls = CosmosDBBuilder
    array_converter_cls = CosmosDBArrayConverter

    name_before_table = 'db_name'

    converter_classes = [
        (NoneType, dbapiprovider.NoneConverter),
        (bool, dbapiprovider.BoolConverter),
        (basestring, CosmosDBStrConverter),
        (int_types, CosmosDBIntConverter),
        (float, dbapiprovider.RealConverter),
        (Decimal, CosmosDBDecimalConverter),
        (datetime, CosmosDBDatetimeConverter),
        (date, CosmosDBDateConverter),
        (time, CosmosDBTimeConverter),
        (timedelta, CosmosDBTimedeltaConverter),
        (UUID, dbapiprovider.UuidConverter),
        (buffer, dbapiprovider.BlobConverter),
        (Json, CosmosDBJsonConverter)
    ]

    def __init__(provider, *args, **kwargs):
        DBAPIProvider.__init__(provider, *args, **kwargs)
        provider.pre_transaction_lock = Lock()
        provider.transaction_lock = Lock()

    def execute(provider, cursor, sql, arguments=None, returning_id=False):
        cursor.execute(sql, arguments)

    @wrap_dbapi_exceptions
    def commit(provider, connection, cache=None):
        # FIXME: There is no commit in doc databases
        pass

    @wrap_dbapi_exceptions
    def inspect_connection(provider, conn):
        DBAPIProvider.inspect_connection(provider, conn)
        provider.json1_available = provider.check_json1(conn)

    def restore_exception(provider):
        if provider.local_exceptions.exc_info is not None:
            try: reraise(*provider.local_exceptions.exc_info)
            finally: provider.local_exceptions.exc_info = None

    def acquire_lock(provider):
        # FIXME: There is no lock in database
        pass

    def release_lock(provider):
        # FIXME: There is no release lock in database
        pass

    @wrap_dbapi_exceptions
    def set_transaction_mode(provider, connection, cache):
        # FIXME: There is no transaction mode in database
        pass

    def commit(provider, connection, cache=None):
        in_transaction = cache is not None and cache.in_transaction
        try:
            DBAPIProvider.commit(provider, connection, cache)
        finally:
            if in_transaction:
                cache.in_transaction = False
                provider.release_lock()

    def rollback(provider, connection, cache=None):
        in_transaction = cache is not None and cache.in_transaction
        try:
            DBAPIProvider.rollback(provider, connection, cache)
        finally:
            if in_transaction:
                cache.in_transaction = False
                provider.release_lock()

    def drop(provider, connection, cache=None):
        in_transaction = cache is not None and cache.in_transaction
        try:
            DBAPIProvider.drop(provider, connection, cache)
        finally:
            if in_transaction:
                cache.in_transaction = False
                provider.release_lock()

    @wrap_dbapi_exceptions
    def release(provider, connection, cache=None):
        if cache is not None:
            db_session = cache.db_session
            if db_session is not None and db_session.ddl and cache.saved_fk_state:
                try:
                    cursor = connection.cursor()
                    sql = 'PRAGMA foreign_keys = true'
                    if core.local.debug: log_orm(sql)
                    cursor.execute(sql)
                except:
                    provider.pool.drop(connection)
                    raise
        DBAPIProvider.release(provider, connection, cache)

    def get_pool(provider, endpoint, primary_key, database_name, container_name, **kwargs):
        return CosmosDBPool(endpoint, primary_key, database_name, container_name, **kwargs)

    def table_exists(provider, connection, table_name, case_sensitive=True):
        return provider._exists(connection, table_name, None, case_sensitive)

    def index_exists(provider, connection, table_name, index_name, case_sensitive=True):
        return provider._exists(connection, table_name, index_name, case_sensitive)

    def _exists(provider, connection, table_name, index_name=None, case_sensitive=True):
        # TODO: Check if table/container exist and creates it
        pass
        # db_name, table_name = provider.split_table_name(table_name)
        #
        # if db_name is None: catalog_name = 'sqlite_master'
        # else: catalog_name = (db_name, 'sqlite_master')
        # catalog_name = provider.quote_name(catalog_name)
        #
        # cursor = connection.cursor()
        # if index_name is not None:
        #     sql = "SELECT name FROM %s WHERE type='index' AND name=?" % catalog_name
        #     if not case_sensitive: sql += ' COLLATE NOCASE'
        #     cursor.execute(sql, [ index_name ])
        # else:
        #     sql = "SELECT name FROM %s WHERE type='table' AND name=?" % catalog_name
        #     if not case_sensitive: sql += ' COLLATE NOCASE'
        #     cursor.execute(sql, [ table_name ])
        # row = cursor.fetchone()
        # return row[0] if row is not None else None

    def fk_exists(provider, connection, table_name, fk_name):
        assert False  # pragma: no cover

    def check_json1(provider, connection):
        return True


provider_cls = CosmosDBProvider


def _text_factory(s):
    return s.decode('utf8', 'replace')


def make_string_function(name, base_func):
    def func(value):
        if value is None:
            return None
        t = type(value)
        if t is not unicode:
            if t is buffer:
                value = hexlify(value).decode('ascii')
            else:
                value = unicode(value)
        result = base_func(value)
        return result
    func.__name__ = name
    return func


py_upper = make_string_function('py_upper', unicode.upper)
py_lower = make_string_function('py_lower', unicode.lower)


def py_json_unwrap(value):
    # [null,some-value] -> some-value
    if value is None:
        return None
    assert value.startswith('[null,'), value
    return value[6:-1]


path_cache = {}

json_path_re = re.compile(r'\[(-?\d+)\]|\.(?:(\w+)|"([^"]*)")', re.UNICODE)


def _parse_path(path):
    if path in path_cache:
        return path_cache[path]
    keys = None
    if isinstance(path, basestring) and path.startswith('$'):
        keys = []
        pos = 1
        path_len = len(path)
        while pos < path_len:
            match = json_path_re.match(path, pos)
            if match is not None:
                g1, g2, g3 = match.groups()
                keys.append(int(g1) if g1 else g2 or g3)
                pos = match.end()
            else:
                keys = None
                break
        else: keys = tuple(keys)
    path_cache[path] = keys
    return keys


def _traverse(obj, keys):
    if keys is None: return None
    list_or_dict = (list, dict)
    for key in keys:
        if type(obj) not in list_or_dict: return None
        try: obj = obj[key]
        except (KeyError, IndexError): return None
    return obj


def _extract(expr, *paths):
    expr = json.loads(expr) if isinstance(expr, basestring) else expr
    result = []
    for path in paths:
        keys = _parse_path(path)
        result.append(_traverse(expr, keys))
    return result[0] if len(paths) == 1 else result


def py_json_extract(expr, *paths):
    result = _extract(expr, *paths)
    if type(result) in (list, dict):
        result = json.dumps(result, **CosmosDBJsonConverter.json_kwargs)
    return result


def py_json_query(expr, path, with_wrapper):
    result = _extract(expr, path)
    if type(result) not in (list, dict):
        if not with_wrapper: return None
        result = [result]
    return json.dumps(result, **CosmosDBJsonConverter.json_kwargs)


def py_json_value(expr, path):
    result = _extract(expr, path)
    return result if type(result) not in (list, dict) else None


def py_json_contains(expr, path, key):
    expr = json.loads(expr) if isinstance(expr, basestring) else expr
    keys = _parse_path(path)
    expr = _traverse(expr, keys)
    return type(expr) in (list, dict) and key in expr


def py_json_nonzero(expr, path):
    expr = json.loads(expr) if isinstance(expr, basestring) else expr
    keys = _parse_path(path)
    expr = _traverse(expr, keys)
    return bool(expr)


def py_json_array_length(expr, path=None):
    expr = json.loads(expr) if isinstance(expr, basestring) else expr
    if path:
        keys = _parse_path(path)
        expr = _traverse(expr, keys)
    return len(expr) if type(expr) is list else 0


def wrap_array_func(func):
    @wraps(func)
    def new_func(array, *args):
        if array is None:
            return None
        array = json.loads(array)
        return func(array, *args)
    return new_func


@wrap_array_func
def py_array_index(array, index):
    try:
        return array[index]
    except IndexError:
        return None


@wrap_array_func
def py_array_contains(array, item):
    return item in array


@wrap_array_func
def py_array_subset(array, items):
    if items is None: return None
    items = json.loads(items)
    return set(items).issubset(set(array))


@wrap_array_func
def py_array_length(array):
    return len(array)


@wrap_array_func
def py_array_slice(array, start, stop):
    return dumps(array[start:stop])


def py_make_array(*items):
    return dumps(items)


class CosmosClientDatabase:
    def __init__(self, endpoint, primary_key, database_name, container_name):
        if endpoint is not None:
            self.client = cosmos_client.CosmosClient(
                url_connection=endpoint,
                auth={'masterKey': primary_key}
            )

            self.database_id = self.create_db_if_not_exists(database_name)
            self.container_id = self.create_container_if_not_exists(container_name)

    def create_db_if_not_exists(self, db_name):
        db_link = 'dbs/'+db_name
        try:
            self.client.ReadDatabase(db_link)
        except HTTPFailure:
            self.client.CreateDatabase({'id': db_name})

        return db_link

    def create_container_if_not_exists(self, container_name):
        container_link = self.database_id+'/colls/'+container_name
        try:
            self.client.ReadContainer(container_link)
        except HTTPFailure:
            self.client.CreateContainer(self.database_id, {'id': container_name})

        return container_link

    def delete_db(self):
        try:
            self.client.DeleteDatabase(self.database_id)
        except HTTPFailure:
            print("Something wrong in delete_db().")

    def get_container(self):
        try:
            return self.client.ReadContainer(self.container_id)
        except HTTPFailure:
            return None

    def get_container_id(self):
        return self.container_id

    def permissive_json_loads(self, text):
        while True:
            try:
                data = json.loads(text)
            except JSONDecodeError as exc:
                if exc.msg == 'Invalid \\escape':
                    text = text[:exc.pos] + '\\' + text[exc.pos:]
                else:
                    raise
            else:
                return data

    def insert_doc(self, doc, check):
        result = self.get_items(check, None)
        it = iter(result)
        first = next(it, None)

        if first is None:
            self.client.CreateItem(self.container_id, self.permissive_json_loads(doc))
        else:
            pass

    def update_doc(self, doc_link, doc):
        try:
            self.client.ReplaceItem(doc_link, doc)
        except HTTPFailure:
            print('something went wrong updating document.')

    def delete_doc(self, doc_link):
        try:
            self.client.DeleteItem(doc_link)
        except HTTPFailure:
            print('something went wrong updating document.')

    @staticmethod
    def generate_query(sql, args):
        parameters = []

        if args is None:
            return {'query': sql}

        for i in range(len(args)):
            param_dict = {
                'name': "@p{}".format(i + 1),
                'value': args[i]
            }
            parameters.append(param_dict)

        query = {
            'query': sql,
            'parameters': parameters
        }

        return query

    def get_items(self, sql, args):
        options = {}
        options['enableCrossPartitionQuery'] = True
        return self.client.QueryItems(self.container_id, self.generate_query(sql, args), options)


class CosmosDBCursor:
    def __init__(cursor, client):
        cursor.client = client
        cursor.sql = None
        cursor.arguments = None
        cursor.rowcount = 0
        cursor.description = []
        cursor.query_results = []

    def execute(cursor, sql, arguments):
        cursor.sql = sql
        cursor.arguments = arguments
        print(sql)
        print(arguments)

        if cursor.sql.startswith('INSERT'):
            cursor.insert(sql, arguments)
        elif cursor.sql.startswith('UPDATE'):
            cursor.update(sql, arguments)
        elif cursor.sql.startswith('DELETE'):
            cursor.delete(sql, arguments)

    def insert(cursor, sql, arguments):
        for i, p in enumerate(arguments, start=1):
            sql = sql.replace('@p{}'.format(i), str(p), 1)

        split = sql.split('INSERT ')
        doc = split[1]
        check = split[2]

        cursor.client.insert_doc(doc, check)

    def update(cursor, sql, arguments):
        for i, p in enumerate(arguments, start=1):
            sql = sql.replace('@p{}'.format(i), str(p), 1)

        split = sql.split('UPDATED ')
        query = split[1]
        update_info = json.loads(split[2])
        query_result = cursor.client.get_items(query, None)
        doc = iter(query_result).next()

        if doc is not None:
            doc_link = doc['_self']
            for key in update_info.keys():
                doc[key] = update_info[key]

            cursor.client.update_doc(doc_link, doc)
            cursor.rowcount = cursor.rowcount + 1

    def delete(cursor, sql, arguments):
        for i, p in enumerate(arguments, start=1):
            sql = sql.replace('@p{}'.format(i), str(p), 1)

        split = sql.split('DELETE ')
        query = split[1]
        query_result = cursor.client.get_items(query, None)
        doc = iter(query_result).next()

        if doc is not None:
            doc_link = doc['_self']
            cursor.client.delete_doc(doc_link)
            cursor.rowcount = cursor.rowcount + 1

    def fetchone(cursor):
        result = cursor.client.get_items(cursor.sql, cursor.arguments)
        return [tuple(item.values()) for item in result]

    def fetchmany(cursor, size=None):
        result = cursor.client.get_items(cursor.sql, cursor.arguments)
        return [tuple(item.values()) for item in result]

    def fetchall(cursor):
        result = cursor.client.get_items(cursor.sql, cursor.arguments)
        return [tuple(item.values()) for item in result]


class CosmosDBConnection:
    def __init__(connection, endpoint, primary_key, database_name, container, **kwargs):
        connection.endpoint = endpoint
        connection.primary_key = primary_key
        connection.database_name = database_name
        connection.container = container
        connection.kwargs = kwargs
        connection.client = None

    def create_client(connection):
        connection.client = CosmosClientDatabase(connection.endpoint, connection.primary_key, connection.database_name, connection.container)

    def commit(self):
        pass

    def cursor(connection):
        return CosmosDBCursor(connection.client)

    def rollback(connection):
        pass

    def release_lock(connection):
        pass


class CosmosDBPool(Pool):
    def __init__(pool, endpoint, primary_key, database_name, container_name, **kwargs):
        pool.endpoint = endpoint
        pool.primary_key = primary_key
        pool.database_name = database_name
        pool.container_name = container_name
        pool.kwargs = kwargs
        pool.con = None

    def open(pool, endpoint, primary_key, database_name, container_name):
        pool.endpoint = endpoint
        pool.primary_key = primary_key
        pool.database_name = database_name
        pool.container_name = container_name
        pool.connect()

    def connect(pool):
        if pool.con is None:
            is_new_connection = True
            pool.con = CosmosDBConnection(pool.endpoint, pool.primary_key, pool.database_name, pool.container_name)
            pool.con.create_client()
        else:
            is_new_connection = False

        return pool.con, is_new_connection

    def release(pool, con):
        pass

    def disconnect(pool):
        pass

    def drop(pool, con):
        pass
