#############################
###     mysql的连接配置    ###
#############################

import re
from abc import abstractmethod
from typing import Callable, List

import pandas as pd
import pymysql as pymysql
# mysql 数据库 连接配置
from pymysql.cursors import Cursor
from samutils.util.commonwrapper import catch_and_print_exception

from samutils.util.assisttool import formatter_line, list2dict

from samutils.util.logutil import get_default_logger, LoggerUtil

default_logger = get_default_logger()

extract_column_from_sql_re = re.compile("^select.+from", re.I)

EMPTY_SYMBOL = "_EMPTY_"
NULL_SYMBOL = "_NULL_"


class MysqlConnectionConfig():
    def __init__(self, host, user, pwd, db_name, port):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.pwd = pwd


DEFAULT_DB_CONNECTION_CONFIG = MysqlConnectionConfig(
    "localhost", "root", "sanmubird", "test", 3306)


def get_connection(config: MysqlConnectionConfig):
    db = pymysql.connect(config.host, config.user, config.pwd, config.db_name, port=config.port, charset='utf8')
    db.autocommit(True)
    return db


def get_default_connection():
    """
    这里 默认数据库 连接的是 测试库
    :return:
    """
    config = DEFAULT_DB_CONNECTION_CONFIG
    return get_connection(config)


#############################
###   对mysql的基本操作   ###
#############################


def get_query_sql(table_name: str
                  , column: list = None
                  , column_str: str = None
                  , where: str = None
                  , limit: int = None
                  , start: int = None
                  , distinct: bool = False
                  ):
    if not table_name:
        raise RuntimeWarning("要查询的表名 不能为空.")
    if column:
        if distinct:
            column.insert(0, "distinct")
        _column_str = ", ".join(column)
    elif column_str:
        if distinct:
            if "distinct" not in column_str:
                column_str = f"distinct {column_str}"
        _column_str = column_str
    else:
        if distinct:
            _column_str = "distinct *"
        else:
            _column_str = '*'

    sql_str_list = ["select", _column_str, "from", table_name]

    if where:
        sql_str_list.append("where")
        sql_str_list.append(where)
    if limit:
        if start:
            sql_str_list.append(f" limit {start}, {limit} ")
        else:
            sql_str_list.append("limit")
            sql_str_list.append(str(limit))

    return " ".join(sql_str_list)


def parse_query_result(query_result: list
                       , column: list = None
                       , result_type: str = "tuple"
                       , datetime_formatter: str = None
                       , result_formatter: Callable[[list, list], List[dict]] = None
                       ):
    if result_formatter:
        # 如果 自定义了 格式化方法 就不走 系统预设的结果格式化方法
        return result_formatter(query_result, column)
    else:
        new_query_result = []
        for res in query_result:
            new_res = formatter_line(res, datetime_formatter)
            if "tuple" == result_type:
                new_query_result.append(tuple(new_res))
            elif "list" == result_type:
                new_query_result.append(list(new_res))
            elif "dict" == result_type and column:
                res_dict = list2dict(column, new_res)
                new_query_result.append(res_dict)
            else:
                error_msg = f"不支持当前操作数 {result_type} 或 操作数为 dict 时, column 为 空"
                raise RuntimeWarning(error_msg)
        return new_query_result


@catch_and_print_exception
def delete(cursor: Cursor
           , table_name: str
           , where: str
           , is_only_print_sql: bool = False):
    if not where:
        error_msg = f"删除时 条件不能为空"
        raise RuntimeWarning(error_msg)
    delete_sql = f"delete from {table_name} where {where} "
    if is_only_print_sql:
        default_logger.info(f"使用的删除语句是：{delete_sql}")
    else:
        default_logger.debug(f"使用的删除语句是：{delete_sql}")
        try:
            num = cursor.execute(delete_sql)
            default_logger.info(f"delete 影响的行数是 {num}")
            return num
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"删除出错,使用的sql是: {delete_sql}")
            raise e


# @catch_and_print_exception
def query(cursor: Cursor
          , table_name: str = None
          , column: list = None
          , column_str: str = None
          , where: str = None
          , limit: int = None
          , start: int = None
          , sql: str = None
          , write_type: str = None
          , distinct: bool = False
          , datetime_formatter: str = None
          , is_only_print_sql: bool = False
          , result_formatter: Callable[[list], list] = None
          ):
    """
    :param sql:
    :param column_str:
    :param distinct:
    :param start:
    :param result_formatter: 查询结果格式化
    :param cursor:
    :param table_name: 要查询的表名
    :param column: 需要查询的列 可以允许是 name as client_name 这种形式
    :param where: 需要拼接好的字符串
    :param limit: 只提供limit
    :param write_type: 可以选择 返回的结果 支持 tuple list dict
    :param datetime_formatter: 对时间的格式化
    :param is_only_print_sql: 是否只打印不执行
    :return:
    """
    if not write_type:
        write_type = "tuple"
    if write_type not in ["dict", "list", "tuple"]:
        error_msg = f"不支持当前操作数 {write_type}"
        raise RuntimeWarning(error_msg)

    if sql:
        query_sql = sql.strip()
        column_match = re.match(extract_column_from_sql_re, query_sql)
        if column_match:
            # 这里的 [6:-5] 是 根据 select * from 这个sql 来的， 截取前后 就会 得到
            column_str = column_match.group()[6:-5].strip()
        else:
            msg = f"query_sql 可能不被支持, 请检查 {query_sql}"
            raise RuntimeError(msg)
    else:
        query_sql = get_query_sql(table_name, column=column, column_str=column_str, where=where, limit=limit,
                                  start=start, distinct=distinct)
    if is_only_print_sql:
        default_logger.info(f"使用的查询语句是：{query_sql}")
    else:
        try:
            cursor.execute(query_sql)
            query_result = cursor.fetchall()
            if query_result:
                if column:
                    _column = column
                elif column_str:
                    if "distinct" in column_str:
                        column_str = column_str.replace("distinct", "")
                    _column = []
                    for item in column_str.split(","):
                        column_str = item.strip()
                        if " as " in column_str:
                            _column.append(column_str.split(" as ")[1].strip())
                        elif " AS " in column_str:
                            _column.append(column_str.split(" AS ")[1].strip())
                        elif " As " in column_str:
                            _column.append(column_str.split(" As ")[1].strip())
                        elif " aS " in column_str:
                            _column.append(column_str.split(" aS ")[1].strip())
                        else:
                            _column.append(column_str)
                else:
                    _column = column
                return parse_query_result(query_result
                                          , column=_column
                                          , result_type=write_type
                                          , datetime_formatter=datetime_formatter
                                          , result_formatter=result_formatter
                                          )
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"查询出错,使用的sql是: {query_sql}")
            raise e


def _formatter_type(value):
    if isinstance(value, str):
        return f"'{value}'"
    else:
        return value


def get_update_sql(table_name: str, item_list: list, optional=None, condition: dict = None,
                   exclude_properties: list = None, update_key_prefix: str = None
                   , null_symbol: str = NULL_SYMBOL, empty_symbol: str = EMPTY_SYMBOL):
    """
    根据 表名称 对象 和 条件  生成操作数据库的语句
    :param null_symbol:
    :param empty_symbol:
    :param update_key_prefix:
    :param exclude_properties: 需要排除的属性  仅用于插入或更新时
    :param item_list: 批量操作的对象
    :param optional: 操作类型： 插入 批量插入 更新 批量更新 插入更新
    :param condition: 条件  更新模式下： {'a':'b', ' in 1':'a in (a,d,v)', ' in 2':'c in (1,2,3)'}
                            批量更新模式下： {'in':'updateKey'}
    :param table_name: 表名
    :return:
    """
    null_symbol = null_symbol if null_symbol else NULL_SYMBOL
    empty_symbol = empty_symbol if empty_symbol else EMPTY_SYMBOL
    if not table_name or not item_list:
        raise RuntimeWarning("表名 和 数据对象 不能为空")

    if not optional or "Insert" == optional:
        columns = []
        values = []
        for key, value in item_list[0].items():
            columns.append(key)
            if isinstance(value, str):
                if null_symbol == value:
                    values.append('null')
                elif empty_symbol == value:
                    values.append("''")
                else:
                    values.append(f"'{value}'")
            else:
                values.append(str(value))
        return f"insert into {table_name} ({', '.join(columns)}) values ({', '.join(values)})"

    elif "BatchInsert" == optional:
        columns = []
        values_list = []
        for key in item_list[0].keys():
            columns.append(key)
        for item in item_list:
            values = []
            for value in item.values():
                if isinstance(value, str):
                    if null_symbol == value:
                        values.append('null')
                    elif empty_symbol == value:
                        values.append("''")
                    else:
                        values.append(f"'{value}'")
                else:
                    values.append(str(value))
            else:
                values_list.append(f"({', '.join(values)})")
        return f"insert into {table_name} ({', '.join(columns)}) values {', '.join(values_list)}"

    elif "InsertOrUpdate" == optional:
        columns = []
        values = []
        condition_part_list = []
        for key, value in item_list[0].items():
            columns.append(key)
            if isinstance(value, str):
                if null_symbol == value:
                    values.append('null')
                elif empty_symbol == value:
                    values.append("''")
                else:
                    values.append(f"'{value}'")
                if (not exclude_properties) or (exclude_properties and key not in exclude_properties):
                    if null_symbol == value:
                        condition_part_list.append(f" {key} = null ")
                    elif empty_symbol == value:
                        condition_part_list.append(f"  {key} = '' ")
                    else:
                        condition_part_list.append(f" {key} = '{value}' ")
            else:
                values.append(str(value))
                if (not exclude_properties) or (exclude_properties and key not in exclude_properties):
                    condition_part_list.append(f" {key} = {value} ")
        return f"insert into {table_name} ({', '.join(columns)}) values ({', '.join(values)}) " \
               f"ON DUPLICATE KEY UPDATE {', '.join(condition_part_list)} "

    elif "Update" == optional:
        if condition:
            condition_keys = condition.keys()
            item = item_list[0]
            update_key = None
            in_key = None
            if "condition_str" in condition_keys:
                if update_key_prefix:
                    raise RuntimeWarning("单个更新操作模式下请注意, 当参数 condition 为{condition_str}时, update_key_prefix 只能为空。 ")
            elif "in" in condition_keys:
                in_key = condition.get('in')
                if update_key_prefix:
                    update_key = f"{update_key_prefix}{in_key}"
                    if update_key not in item.keys():
                        msg = f"有更新键前缀 {update_key_prefix} 和 更新键 {in_key}, 但无更新替换键 {update_key}。"
                        raise RuntimeError(msg)
            else:
                raise RuntimeWarning("单个更新操作模式下请注意, 当参数 condition 只能是: {condition_str:condition} 或 {in:clolumn} ")

            set_part_list = []
            for key, value in item.items():
                # 如果 有 update_key 则 set 需要用 update_key 而且 where 用  in_key
                if update_key and key == update_key:
                    key = in_key
                    value = item.get(update_key)
                else:
                    # 如果 只有 in_key 则 set 不需要用 in_key  而且 where 用 in_key
                    if in_key and key == in_key:
                        continue
                if isinstance(value, str):
                    if null_symbol == value:
                        set_part_list.append(f" {key} = null ")
                    elif empty_symbol == value:
                        set_part_list.append(f" {key} = '' ")
                    else:
                        set_part_list.append(f" {key} = '{value}' ")
                else:
                    set_part_list.append(f" {key} = {value} ")

            condition_part_list = []
            if "condition_str" in condition_keys:
                condition_part_list.append(f"{condition.get('condition_str')}")
            else:
                value = item.get(in_key)
                if isinstance(value, str):
                    if null_symbol == value:
                        condition_part_list.append(f" {in_key} = null ")
                    elif empty_symbol == value:
                        condition_part_list.append(f" {key} = '' ")
                    else:
                        condition_part_list.append(f" {in_key} = '{value}' ")
                else:
                    condition_part_list.append(f" {in_key} = {value} ")

            return f"update {table_name} set {', '.join(set_part_list)} where {' and '.join(condition_part_list)}"
        else:
            raise RuntimeWarning("更新操作模式下 condition 参数 不能为空")

    elif "BatchUpdate" == optional:
        if condition and len(condition) == 1 and condition.get("in", None):
            in_key = condition["in"]
            data_frame = pd.DataFrame(item_list, index=[item[in_key] for item in item_list])
            new_data_frame = data_frame.unstack()
            keys = item_list[0].keys()
            if update_key_prefix:
                update_key = f"{update_key_prefix}{in_key}"
                if update_key not in keys:
                    msg = f"有更新键前缀 {update_key_prefix} 和 更新键 {in_key}, 但无更新替换键 {update_key}。"
                    raise RuntimeError(msg)
            else:
                update_key = None

            batch_update_column_list = []
            condition_part_list = []
            update_key_modify_column_list = []
            for key in keys:
                series = new_data_frame[key]
                if key == in_key:
                    condition_part_list = [str(_formatter_type(o)) for o in series.values]
                else:
                    if update_key and key == update_key:
                        items = list(series.items())
                        single_update_column_list = [in_key, " = CASE ", in_key]
                        for k, v in items:
                            single_update_column_list.append(f" WHEN {_formatter_type(k)} THEN {_formatter_type(v)}")
                        else:
                            single_update_column_list.append(" END")
                            update_key_modify_column_list.append("".join(single_update_column_list))
                    else:
                        items = list(series.items())
                        single_update_column_list = [key, " = CASE ", in_key]
                        for k, v in items:
                            single_update_column_list.append(f" WHEN {_formatter_type(k)} THEN {_formatter_type(v)}")
                        else:
                            single_update_column_list.append(" END")
                            batch_update_column_list.append("".join(single_update_column_list))
            else:
                batch_update_column_list.extend(update_key_modify_column_list)

            return f"update {table_name} " \
                   f"set {', '.join(batch_update_column_list)} " \
                   f"where  {in_key} in ({', '.join(condition_part_list)})"

        elif "Count" == optional:
            pass
        else:
            raise RuntimeWarning("批量更新操作模式下 请注意 参数 condition 有且仅有一个元素 {'in':'updateKey'} ")

    else:
        raise RuntimeWarning(f"操作模式下 只能是 插入, 更新 , 批量插入 或者 插入更新 , 当前传入的操作模式是： {optional}")


@catch_and_print_exception
def insert(cursor: Cursor, table_name: str, item: dict, is_only_print_sql: bool = False):
    """
    [插入] 返回 id
    :param is_only_print_sql: 是否只打印 sql
    :param cursor:
    :param table_name:
    :param item:
    :return:
    """
    insert_sql = get_update_sql(table_name, [item])
    if is_only_print_sql:
        default_logger.info(f"使用的插入语句是：{insert_sql}")
    else:
        try:
            default_logger.debug(f"使用的插入语句是：{insert_sql}")
            num = cursor.execute(insert_sql)
            default_logger.info(f"insert 影响的行数是 {num}")
            return cursor.lastrowid
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"插入出错,使用的sql是: {insert_sql}")
            raise e


# @catch_and_print_exception
def batch_insert(cursor: Cursor, table_name: str, item_list: list, is_only_print_sql: bool = False):
    """
    [批量插入] 返回 影响行数
    :param is_only_print_sql: 是否只打印 sql
    :param cursor:
    :param table_name:
    :param item_list:
    :return:
    """
    batch_insert_sql = get_update_sql(table_name, item_list, optional="BatchInsert")
    if is_only_print_sql:
        default_logger.info(f"使用的批量插入语句是：{batch_insert_sql}")
    else:
        try:
            default_logger.debug(f"使用的批量插入语句是：{batch_insert_sql}")
            num = cursor.execute(batch_insert_sql)
            default_logger.info(f"batch_insert 影响的行数是 {num}")
            return num
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"批量插入出错,使用的sql是: {batch_insert_sql}")
            raise e


@catch_and_print_exception
def update(cursor: Cursor, table_name: str, item: dict, condition: dict, is_only_print_sql: bool = False,
           update_key_prefix: str = None):
    """
    [更新] 返回 id
    :param is_only_print_sql:是否只打印 sql
    :param cursor:
    :param table_name:
    :param item:
    :param condition: 条件 如果有in的话 将in的语句全部写到 key 中 value 写 '' 即可
    :return:
    """
    update_sql = get_update_sql(table_name, [item], optional="Update", condition=condition,
                                update_key_prefix=update_key_prefix)
    if is_only_print_sql:
        default_logger.info(f"使用的更新语句是：{update_sql}")
    else:
        try:
            default_logger.debug(f"使用的更新语句是：{update_sql}")
            num = cursor.execute(update_sql)
            default_logger.info(f"update 影响的行数是 {num}")
            return cursor.lastrowid
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"更新出错,使用的sql是: {update_sql}")
            raise e


# @catch_and_print_exception
def batch_update(cursor: Cursor, table_name: str, item_list: list, condition: dict, is_only_print_sql: bool = False,
                 update_key_prefix: str = None):
    """
    [更新] 返回 id
    :param update_key_prefix:
    :param is_only_print_sql:是否只打印 sql
    :param cursor:
    :param table_name:
    :param item_list:
    :param condition: 条件 如果有in的话 将in的语句全部写到 key 中 value 写 '' 即可
    :return:
    """
    batch_update_sql = get_update_sql(table_name, item_list, optional="BatchUpdate", condition=condition,
                                      update_key_prefix=update_key_prefix)
    if is_only_print_sql:
        default_logger.info(f"使用的批量更新语句是：{batch_update_sql}")
    else:
        try:
            default_logger.debug(f"使用的批量更新语句是：{batch_update_sql}")
            num = cursor.execute(batch_update_sql)
            default_logger.info(f"batch_update 影响的行数是 {num}")
            return num
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"批量更新出错,使用的sql是: {batch_update_sql}")
            raise e


@catch_and_print_exception
def insert_or_update(cursor: Cursor, table_name: str, item: dict, is_only_print_sql: bool = False,
                     exclude_properties: list = None):
    """
    [插入或更新] 返回 id
    :param exclude_properties:
    :param is_only_print_sql: 是否只打印 sql
    :param cursor:
    :param table_name:
    :param item:
    :return:
    """
    insert_or_update_sql = get_update_sql(table_name, [item], optional="InsertOrUpdate",
                                          exclude_properties=exclude_properties)
    if is_only_print_sql:
        default_logger.info(f"使用的插入更新语句是：{insert_or_update_sql}")
    else:
        try:
            default_logger.debug(f"使用的插入更新语句是：{insert_or_update_sql}")
            num = cursor.execute(insert_or_update_sql)
            default_logger.info(f"insert_or_update 影响的行数是 {num}")
            return cursor.lastrowid
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"插入更新出错,使用的sql是: {insert_or_update_sql}")
            raise e


def count(cursor, table_name, where, column: list = None, column_str: str = None, distinct: bool = False
          , is_only_print_sql: bool = False, start: int = None, limit: int = None):
    if distinct:
        if column:
            _column_str = f" count( distinct {','.join(column)} )"
        elif column_str:
            _column = []
            for item in column_str.split(","):
                __column_str = item.strip()
                if " as " in __column_str:
                    _column.append(__column_str.split(" as ")[0].strip())
                elif " AS " in __column_str:
                    _column.append(__column_str.split(" AS ")[0].strip())
                elif " As " in __column_str:
                    _column.append(__column_str.split(" As ")[0].strip())
                elif " aS " in __column_str:
                    _column.append(__column_str.split(" aS ")[0].strip())
                else:
                    _column.append(__column_str)
            if "distinct" in column_str:
                _column_str = f"count({','.join(_column)})"
            else:
                _column_str = f"count( distinct {','.join(_column)})"
        else:
            _column_str = " count(distinct * ) "
    else:
        _column_str = " count(1) "

    count_sql = get_query_sql(
        table_name, column_str=_column_str
        , distinct=distinct, where=where, start=start, limit=limit)
    if is_only_print_sql:
        default_logger.info(f"使用的统计语句是：{count_sql}")
    else:
        try:
            default_logger.debug(f"使用的统计语句是：{count_sql}")
            cursor.execute(count_sql)
            num = cursor.fetchone()[0]
            default_logger.debug(f" {count_sql} 统计的结果是 {num}")
            return num
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"统计出错,使用的sql是: {count_sql}")
            raise e


class MySql(LoggerUtil):

    def __init__(self, config: MysqlConnectionConfig = None):
        super().__init__(name="DbUtil", level="info")
        if config:
            self.db = get_connection(config)
        else:
            self.db = get_default_connection()
        self.cursor = self.db.cursor()
        self.current_start = 0
        self.current_end = 0
        self.start_end_tuple_list = None
        self.operate_record = {}
        self.db_name = self.db.db.decode(encoding='utf-8')

    def __del__(self):
        # 操作入库
        self.logger.info(f"操作记录如下: {self.operate_record}")
        self.cursor.close()
        self.db.close()
        self.logger.info("释放了数据库连接")

    def _update_table_operate_record(self, table_name: str, operate_type: str, num: int):
        table_operate_dict = self.operate_record.get(table_name, None)
        if table_operate_dict:
            operate_record_item = table_operate_dict.get(operate_type, None)
            if operate_record_item:
                table_operate_dict[operate_type] += num
            else:
                table_operate_dict[operate_type] = num
        else:
            self.operate_record[table_name] = {operate_type: num}

    def _init_current_start_and_end(self, start: int = None, end: int = None,
                                    start_end_tuple_list: list = None, max_size: int = None):
        """
        初始化 起止数
        :param start:
        :param end:
        :param start_end_tuple_list:
        :param max_size:
        :return:
        """
        if start_end_tuple_list:
            start_end_tuple_list.reverse()
            self.start_end_tuple_list = start_end_tuple_list
        if not self.start_end_tuple_list:
            self.current_start = start if start else 0
            self.current_end = end if end else max_size
        else:
            self._set_next_start_and_end()

    def _set_next_start_and_end(self):
        """
        设置 下一个 起止数
        :return:
        """
        if self.start_end_tuple_list:
            t = self.start_end_tuple_list.pop()
            self.current_start = t[0]
            self.current_end = t[1]

    def _assert_is_between_start_and_end(self, num: int) -> bool:
        """
        判断是否在起止范围内
        :param num:
        :return:
        """
        if num < self.current_start:
            return False
        elif self.current_start <= num < self.current_end:
            return True
        elif num == self.current_end:
            self._set_next_start_and_end()
            return True
        else:
            return False

    def query(self, table_name: str = None, column: list = None, column_str: str = None, limit: int = None,
              where: str = None, sql: str = None, result_type: str = None, datetime_formatter: str = None,
              result_formatter=None, is_only_print_sql: bool = False, distinct: bool = False, start: int = None):
        """
        查询
        :param sql:
        :param column_str:
        :param distinct:
        :param start: 起始值
        :param result_formatter:
        :param datetime_formatter:
        :param table_name:
        :param column:
        :param limit:
        :param where: 允许 为None ,
        :param result_type: 控制 返回结果 ["dict", "list", "tuple"]
        :param is_only_print_sql:
        :return:
        """
        return query(self.cursor, table_name, column=column, column_str=column_str, sql=sql,
                     write_type=result_type, where=where, limit=limit, start=start, distinct=distinct
                     , datetime_formatter=datetime_formatter, is_only_print_sql=is_only_print_sql
                     , result_formatter=result_formatter)

    def _batch_update(self, item_list: list, table_name: str, optional: str = "BatchInsert",
                      is_only_print_sql: bool = False, exclude_properties: list = None, condition: dict = None
                      , update_key_prefix: str = None):
        """
        批量更新
        :param item_list:
        :param table_name:
        :param optional:
        :param is_only_print_sql:
        :param exclude_properties:
        :param condition:
        :return:
        """
        if item_list:
            if "BatchInsert" == optional:
                try:
                    num = batch_insert(self.cursor, table_name, item_list, is_only_print_sql=is_only_print_sql)
                    if num:
                        self._update_table_operate_record(table_name, "BatchInsert", num)
                        self.logger.info(f"批量插入的个数是: {num} 个")
                except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
                    self.logger.error(f"批量插入出现异常,  异常如下:\n  {e} \n 将采用逐条插入或更新的方式插入或更新数据. ")
                    for item in item_list:
                        if item:
                            sid = insert_or_update(self.cursor, table_name, item, is_only_print_sql=is_only_print_sql,
                                                   exclude_properties=exclude_properties)
                            if sid:
                                self._update_table_operate_record(table_name, "InsertOrUpdate", 1)
                                self.logger.info(f"插入或更新影响的id是: {sid}")
                item_list.clear()
            elif "InsertOrUpdate" == optional:
                for item in item_list:
                    if item:
                        sid = insert_or_update(self.cursor, table_name, item, is_only_print_sql=is_only_print_sql,
                                               exclude_properties=exclude_properties)
                        if sid:
                            self._update_table_operate_record(table_name, "InsertOrUpdate", 1)
                            self.logger.info(f"插入或更新影响的id是: {sid}")
                else:
                    item_list.clear()
            elif "BatchUpdate" == optional and condition:
                try:
                    num = batch_update(self.cursor, table_name, item_list, condition,
                                       is_only_print_sql=is_only_print_sql, update_key_prefix=update_key_prefix)
                    if num:
                        self._update_table_operate_record(table_name, "BatchUpdate", num)
                        self.logger.info(f"批量更新影响的行数是: {num} 个")
                except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
                    self.logger.error(f"批量更新出现异常,  异常如下: \n  {e} \n 将采用逐条更新的方式更新数据.")
                    for item in item_list:
                        if item:
                            sid = update(self.cursor, table_name, item, condition,
                                         is_only_print_sql=is_only_print_sql)
                            if sid:
                                self._update_table_operate_record(table_name, "Update", 1)
                                self.logger.info(f"单个更新影响的id是: {sid} ")
                item_list.clear()
            elif "Update" == optional and condition:
                for item in item_list:
                    if item:
                        sid = update(self.cursor, table_name, item, condition,
                                     is_only_print_sql=is_only_print_sql, update_key_prefix=update_key_prefix)
                        if sid:
                            self._update_table_operate_record(table_name, "Update", 1)
                            self.logger.info(f"单个更新影响的id是: {sid} ")
                else:
                    item_list.clear()
            elif "Insert" == optional:
                for item in item_list:
                    if item:
                        sid = insert(self.cursor, table_name, item, is_only_print_sql=is_only_print_sql)
                        if sid:
                            self._update_table_operate_record(table_name, "Insert", 1)
                            self.logger.info(f"插入的id是: {sid}")
                else:
                    item_list.clear()
            else:
                self.logger.info(
                    f" 传入的参数 如下: item_list: {item_list}, table_name: {table_name}, option: {optional}, "
                    f"is_only_print_sql: {is_only_print_sql}, exclude_properties: {exclude_properties}, "
                    f"condition: {condition}, 当前操作: {optional} 不支持 "
                )
                item_list.clear()

    def batch_update_by_item_list(self, item_list: list, table_name: str, batch_size=100, optional: str = None
                                  , is_only_print_sql: bool = False, exclude_properties: list = None
                                  , start: int = None, end: int = None, condition: dict = None
                                  , start_end_tuple_list: list = None, update_key_prefix: str = None):
        """
        批量更新数据库 通过单个文件
        :param update_key_prefix:
        :param item_list:
        :param table_name:
        :param batch_size:
        :param optional:
        :param is_only_print_sql:
        :param exclude_properties:
        :param start:
        :param end:
        :param condition: 仅在更新时 使用
        :param start_end_tuple_list:
        :return:
        """
        # 初始化 起止数
        self._init_current_start_and_end(start, end, start_end_tuple_list, len(item_list))

        temp_item_list = []
        num = 0
        for item in item_list:
            num += 1
            if self._assert_is_between_start_and_end(num):
                temp_item_list.append(item)

                if num % batch_size == 0:
                    self._batch_update(temp_item_list, table_name, optional=optional,
                                       is_only_print_sql=is_only_print_sql,
                                       exclude_properties=exclude_properties, condition=condition,
                                       update_key_prefix=update_key_prefix)
                    self.logger.info(f"完成了 第 {num} 个")

        else:
            if temp_item_list:
                self._batch_update(temp_item_list, table_name, optional=optional,
                                   is_only_print_sql=is_only_print_sql,
                                   exclude_properties=exclude_properties, condition=condition,
                                   update_key_prefix=update_key_prefix)
            if self.current_end > num:
                self.logger.info(f"完成了 第 {num} 个,  共 {num} 个 ")
            else:
                self.logger.info(f"完成了 第 {self.current_end} 个, 共 {num} 个 ")

    def delete(self, table_name, where: str, is_only_print_sql: bool = False):
        num = delete(self.cursor, table_name, where, is_only_print_sql=is_only_print_sql)
        if num:
            self._update_table_operate_record(table_name, "Delete", 1)
            self.logger.info(f"删除 {num} 条记录")
        return num

    def count(self, table_name, where: str = None, is_only_print_sql: bool = False, column: list = None,
              column_str: str = None, distinct: bool = False):
        return count(self.cursor, table_name, where, column=column, column_str=column_str,
                     distinct=distinct, is_only_print_sql=is_only_print_sql)

    def query_by_sql(self, query_sql: str):
        return self.execute(sql=query_sql, is_need_return=True, is_query=True)

    @catch_and_print_exception
    def execute(self, sql: str, is_need_return: bool = False,
                result_formatter_func: Callable[[list], object] = None,
                is_query: bool = False):
        res = self.cursor.execute(sql)
        if not is_need_return:
            self.logger.info(f"执行sql: {sql} \n 的结果是: {res}")
        else:
            if is_query:
                result = self.cursor.fetchall()
                if result_formatter_func:
                    return result_formatter_func(result)
                else:
                    return result
            else:
                return res

    @staticmethod
    def if_none_then_empty(s: str):
        if '' == s:
            return EMPTY_SYMBOL
        else:
            return s

    @staticmethod
    def if_none_then_null(s: str):
        if '' == s:
            return NULL_SYMBOL
        else:
            return s

    def get_db_data_by_generator(self
                                 , table_name
                                 , where: str = None
                                 , column: list = None
                                 , column_str: str = None
                                 , batch_size: int = 10000
                                 , result_type: str = "list"
                                 , distinct: bool = False
                                 , datetime_formatter: str = None
                                 , result_formatter=None
                                 , is_only_print_sql: bool = False
                                 , is_fixed_start: bool = False
                                 , is_need_check: bool = True
                                 ):
        if where and "status" in where:
            if not is_fixed_start:
                if is_need_check:
                    msg = "查询语句中使用了状态条件，但是没有查询固定开始位置"
                    self.logger.warn(msg)
        elif is_fixed_start:
            if is_need_check:
                msg = "查询语句中固定了开始位置，但是查询条件中没有状态筛选条件"
                self.logger.warn(msg)

        total_count = self.count(table_name, where=where, column=column, column_str=column_str, distinct=distinct)
        self.logger.info(f"从数据库中查询到 共有 {total_count} 条数据要处理")
        max_count = total_count - 1 + batch_size
        _start = 0
        _end = _start + batch_size
        while _end <= max_count:
            # is_fixed_start == True 这种情况 适用于 被查询结果 可能允许被修改的情况
            if is_fixed_start:
                __start = 0
            else:
                __start = _start
            yield self.query(
                table_name
                , where=where
                , column=column
                , column_str=column_str
                , start=__start
                , limit=batch_size
                , result_type=result_type
                , distinct=distinct
                , datetime_formatter=datetime_formatter
                , result_formatter=result_formatter
                , is_only_print_sql=is_only_print_sql
            )
            _start += batch_size
            _end += batch_size

    def batch_handle_db_data_by_generator(self
                                          , table_name: str
                                          , handle_func: Callable[[List[dict]], object]
                                          , where: str = None
                                          , column: list = None
                                          , column_str: str = None
                                          , batch_size: int = 10000
                                          , distinct: bool = False
                                          , datetime_formatter: str = None
                                          , result_type: str = "list"
                                          , is_fixed_start: bool = False
                                          , is_need_check: bool = True
                                          ):
        if handle_func is None:
            raise RuntimeError("处理方法不能为空")
        loop = self.get_db_data_by_generator(
            table_name, where=where, column=column, column_str=column_str, batch_size=batch_size,
            distinct=distinct, result_type=result_type, is_fixed_start=is_fixed_start
            , datetime_formatter=datetime_formatter, is_need_check=is_need_check
        )
        while True:
            try:
                one_generator_return_list = next(loop)
                handle_func(one_generator_return_list)
            except StopIteration:
                break


class MySql2MySql(MySql):
    def __init__(self, config=DEFAULT_DB_CONNECTION_CONFIG):
        super().__init__(config=config)

    def handle_by_generator(self
                            , table_name: str
                            , where: str = None
                            , column: list = None
                            , column_str: str = None
                            , batch_size: int = 10000
                            , distinct: bool = False
                            , datetime_formatter: str = None
                            , is_fixed_start: bool = False
                            ):
        self.batch_handle_db_data_by_generator(table_name
                                               , where=where
                                               , column=column
                                               , column_str=column_str
                                               , batch_size=batch_size
                                               , distinct=distinct
                                               , datetime_formatter=datetime_formatter
                                               , is_fixed_start=is_fixed_start
                                               , handle_func=self.handle_one_generator_return_data
                                               )

    @abstractmethod
    def handle_one_generator_return_data(self, one_generator_return_list):
        """ 处理一批次的查询结果 """
        raise NotImplementedError


if __name__ == "__main__":
    table = "aa"
    d = {
        "A": "a",
        "B": 1,
        "C": 0.1,
        "D": False,
        "_pk_A": 'A'
    }
    d2 = {
        "A": "aa",
        "B": 11,
        "C": 0.11,
        "D": True,
        "_pk_A": 'AA'
    }
    c = {
        "A": "c",
        "D": False
    }
    cc = MySql()
    sql1 = get_update_sql(table, [d, d2], optional="Update",
                          condition={"in": "A"}, update_key_prefix="_pk_")
    print(sql1)
    # sql2 = get_update_sql(table, [d, d2], optional="BatchUpdate", condition={"in": "A"}, update_key_prefix="_pk_")
    # print(sql2)
    # sql3 = get_query_sql("table_v1", where="a = b", start=1, limit=10)
    # print(sql3)
    # sql4 = get_query_sql("sca_client_v5", start=1, limit=10)
    # print(sql4)
    # sql5 = get_query_sql("sca_client_v5", limit=10)
    # print(sql5)
    # sql = get_query_sql(
    #     "qcc_address",
    #     column=["sid", "uuid", "name", "status", "legal_repr", "addr", "email", "bussiness_scope", "phone",
    #             "phone_more"],
    #     where="update_time >= '2019-02-16' and create_client_status = 0")
    # result: list, column: list, option: str
    # result = [(1, 2, 3), (4, 5, 6)]
    # new_result = parse_query_result(result, column=["a  as  aa ", "b", "c"], option="dict")
    # print(new_result)
