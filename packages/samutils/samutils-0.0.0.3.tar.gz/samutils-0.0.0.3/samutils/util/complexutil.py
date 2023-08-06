#############################
###  从mysql导出数据到文件 ###
#############################
import random
from abc import abstractmethod
from typing import List

from samutils.util.esutil import EsConnectionConfig, Es

from samutils.util.strutil import filter_symbol_4_word

from samutils import import_dir_path, import_csv_path

from samutils.util.fileutil import write_file_quick, read_file, get_file_path_list_by_dir_path, check_file, FileUtil

from samutils.util.mysqlutil import MySql, DEFAULT_DB_CONNECTION_CONFIG, MysqlConnectionConfig


class MySql2File(MySql):
    def __init__(self, config=DEFAULT_DB_CONNECTION_CONFIG):
        super().__init__(config=config)
        self.is_need_split_file = False
        self.file_type = "export_query_result"
        self.export_name = "csv"
        self.column = None
        self.batch_size = 10000

    def export_by_generator(self
                            , table_name: str
                            , where: str = None
                            , column: list = None
                            , column_str: str = None
                            , batch_size: int = 10000
                            , distinct: bool = False
                            , datetime_formatter: str = None
                            , is_fixed_start: bool = False
                            , file_type: str = "csv"
                            , export_name: str = "export_query_result"
                            , is_need_split_file: bool = False
                            ):
        self.batch_size = batch_size
        self.is_need_split_file = is_need_split_file
        self.file_type = file_type
        self.export_name = export_name
        self.column = column
        self.batch_handle_db_data_by_generator(table_name
                                               , where=where
                                               , column=column
                                               , column_str=column_str
                                               , batch_size=batch_size
                                               , distinct=distinct
                                               , datetime_formatter=datetime_formatter
                                               , is_fixed_start=is_fixed_start
                                               , handle_func=self.handle_query_result
                                               )

    def handle_query_result(self, one_generator_return_list):
        export_result = self.handle_one_generator_return_data(one_generator_return_list)
        self._export(self.batch_size, self.column, self.export_name, export_result, self.file_type,
                     self.is_need_split_file)

    def _export(self, batch_size: int = 10000, column: list = None, export_name: str = "export_query_result",
                export_result: list = None, file_type: str = "csv", is_need_split_file: bool = False):
        if export_result:
            if is_need_split_file:
                total_size = len(export_result)
                offset = 0
                next_offset = offset + batch_size
                while next_offset < total_size:
                    _export_result = export_result[offset: next_offset]
                    _export_name = f"{export_name}-({offset}-{next_offset})"
                    if column:
                        _export_result.insert(0, column)
                    write_file_quick(_export_result, _export_name, file_type=file_type)
                    offset = next_offset
                    next_offset += batch_size
                else:
                    _export_result = export_result[offset:  next_offset]
                    _export_name = f"{export_name}-({offset}-{total_size})"
                    if column:
                        _export_result.insert(0, column)
                    write_file_quick(_export_result, _export_name, file_type=file_type)
            else:
                if column:
                    export_result.insert(0, column)
                write_file_quick(export_result, export_name, file_type=file_type, write_type="append")
        else:
            self.logger.info(f"{export_name}, 查询结果为空")

    @abstractmethod
    def handle_one_generator_return_data(self, one_generator_return_list) -> list:
        """
        对查询结果进行处理
        """
        raise NotImplementedError


#############################
###  从文件导入数据到mysql ###
#############################


class File2MySql(MySql):
    """
    target:
    1: 实现 从文件夹或文件中 读取内容并更新到数据库
    2: 支持 excel 和 csv 文件的读取
    3: 支持 多种模式更新数据 如 插入更新 批量插入 批量更新 等
    """

    def __init__(self, table_name, import_table_column_list: list = None,
                 config: MysqlConnectionConfig = DEFAULT_DB_CONNECTION_CONFIG):
        super().__init__(config=config)
        self.table_name = table_name
        self.import_table_column_list = import_table_column_list
        self.max_random_count = 10

    @abstractmethod
    def transfer_list_2_dict(self, line: list) -> dict:
        raise NotImplementedError

    def assert_read_file_content_is_suitable(self, file_path) -> bool:
        return check_file(file_path, self.import_table_column_list)

    def batch_update_by_file(self
                             , read_file_path: str
                             , batch_size=100
                             , optional: str = None
                             , is_only_print_sql: bool = False
                             , exclude_properties: list = None
                             , start: int = None
                             , end: int = None
                             , condition: dict = None
                             , start_end_tuple_list: list = None
                             , is_skip_first_line: bool = False
                             , update_key_prefix: str = None
                             ):
        """
        批量更新数据库 通过单个文件
        :param update_key_prefix:
        :param is_skip_first_line:
        :param read_file_path:
        :param batch_size:
        :param optional:
        :param is_only_print_sql:
        :param exclude_properties:
        :param start:
        :param end:
        :param condition:
        :param start_end_tuple_list:
        :return:
        """
        self.logger.info(f"开始 读取文件 {read_file_path} 的 内容")
        if not self.assert_read_file_content_is_suitable(read_file_path):
            msg = f"文件: {read_file_path} 读取到的内容与程序处理能力不匹配"
            raise RuntimeError(msg)
        # 如果有文件表头 则必定跳过首行
        is_skip_first_line = True if self.import_table_column_list else is_skip_first_line
        lines = read_file(read_file_path, is_skip_first_line=is_skip_first_line)
        self.logger.info(f"文件 {read_file_path} 读取 完成 , 将开始对文件进行 预处理 ...")
        item_list = []
        for line in lines:
            # 对 读到的文件进行预处理
            if line[0] is None:
                # 跳过空行
                self.logger.info(f"因为第一个单元格没有内容, 跳过该行: {line}")
                continue
            line = [str(column) for column in line]
            item = self.transfer_list_2_dict(line)
            if isinstance(item, dict):
                item_list.append(item)

        self.logger.info(f"对 文件 {read_file_path} 预处理完成, 符合条件的有 {len(item_list)} 条数据, 将要对文件进行更新至数据库操作... ")
        self.batch_update_by_item_list(item_list, self.table_name, batch_size=batch_size, optional=optional,
                                       is_only_print_sql=is_only_print_sql, exclude_properties=exclude_properties,
                                       start=start, end=end, condition=condition, update_key_prefix=update_key_prefix,
                                       start_end_tuple_list=start_end_tuple_list)
        self.logger.info(f" 完成 {read_file_path}")

    def batch_update_by_dir(self
                            , read_dir_path: str = import_dir_path
                            , start: int = None
                            , end: int = None
                            , batch_size=100
                            , optional: str = "BatchInsert"
                            , is_only_print_sql: bool = False
                            , condition: dict = None
                            , exclude_properties: list = None
                            , is_skip_first_line: bool = False
                            , update_key_prefix: str = None
                            ):
        """
        批量更新数据库 通过文件夹
        :param update_key_prefix:
        :param is_skip_first_line:
        :param read_dir_path:
        :param start:
        :param end:
        :param batch_size:
        :param optional:
        :param is_only_print_sql:
        :param exclude_properties:
        :param condition:
        :return:
        """
        if optional not in ["BatchInsert", "InsertOrUpdate", "BatchUpdate"]:
            error_msg = f"参数错误: 当前操作: {optional} 不支持"
            raise RuntimeError(error_msg)
        if not batch_size or batch_size < 0:
            error_msg = f"参数错误: batch_size : 必须大于0, 当前值为 {batch_size}"
            raise RuntimeError(error_msg)

        read_file_path_list = get_file_path_list_by_dir_path(read_dir_path)
        if read_file_path_list:
            max_size = len(read_file_path_list)
            self.logger.info(f"当前文件夹 {read_dir_path} 共有 {max_size} 个文件")
            if not start:
                start = 0
            if not end:
                end = 0 if end == 0 else max_size
            end = end if max_size >= end else max_size
            self.logger.info(f"本次处理 第 {start} 个 至 第 {end} 个 文件")

            for i in range(max_size):
                if start <= i <= end:
                    read_file_path = read_file_path_list[i]
                    self.batch_update_by_file(
                        read_file_path
                        , batch_size=batch_size
                        , optional=optional
                        , is_only_print_sql=is_only_print_sql
                        , exclude_properties=exclude_properties
                        , condition=condition
                        , is_skip_first_line=is_skip_first_line
                        , update_key_prefix=update_key_prefix
                    )

        else:
            raise RuntimeWarning("该文件夹是空文件夹")


#############################
### 校验mysql和文件是否一致 ###
#############################

class BaseAccordantCheck(MySql):
    """
    target: 检查是否一致
    读取的内容会组装成字典, key: 就是查询的 where 条件; value: 可以是 item 新item 的 keys 是查询的 验证的内容是 item 的 内容
    """

    def __init(self, config=DEFAULT_DB_CONNECTION_CONFIG):
        super().__init__(config=config)

    def do_check(self, table_name: str, need_check_item_list: list, batch_size: int = 500,
                 optional: str = "str") -> tuple:
        """ 检查 """
        accordance_result_list = []
        inconsistent_result_list = []
        temp_source_list = []
        for i, source in enumerate(need_check_item_list):
            temp_source_list.append(source)
            if i > 0 and i % batch_size == 0:
                query_result_list = self.do_query(table_name, temp_source_list, optional=optional)
                temp_inconsistent_list, temp_accordance_list = self.compare(temp_source_list, query_result_list)
                if temp_inconsistent_list:
                    inconsistent_result_list.extend(temp_inconsistent_list)
                if temp_accordance_list:
                    accordance_result_list.extend(temp_accordance_list)
                temp_source_list.clear()
        else:
            query_result_list = self.do_query(table_name, temp_source_list, optional=optional)
            temp_inconsistent_list, temp_accordance_list = self.compare(temp_source_list, query_result_list)
            if temp_inconsistent_list:
                inconsistent_result_list.extend(temp_inconsistent_list)
            if temp_accordance_list:
                accordance_result_list.extend(temp_accordance_list)
            temp_source_list.clear()
        return accordance_result_list, inconsistent_result_list

    def do_query(self, table_name: str, item_list: list, optional: str = "str") -> list:
        if "str" == optional:
            return self.query_by_str(table_name, item_list)
        elif "int" == optional:
            return self.query_by_int(table_name, item_list)
        else:
            msg = f"暂 仅支持 char 或 int , 不支持 {optional}"
            raise RuntimeError(msg)

    def query_by_int(self, table_name: str, item_list: list) -> list:
        column_list = []
        where_value_list = []

        random_index = random.randint(0, len(item_list) - 1)
        random_item = item_list[random_index]
        key_list = list(random_item.keys())
        for i, key in enumerate(key_list):
            column_list.append(f"{key}")
            if i == 0:
                where_key_str = f"{key}"

        for item in item_list:
            value_list = list(item.values())
            for i, value in enumerate(value_list):
                if i == 0:
                    where_value_list.append(f"{value}")

        pre_item_list_str = ",".join(where_value_list)
        where_str = f" {where_key_str} in ({pre_item_list_str}) "
        query_result_list = self.query(
            table_name
            , column=column_list
            , where=where_str
            , result_type="dict"
        )
        return [{k: str(v) for k, v in item.items()} for item in query_result_list]

    def query_by_str(self, table_name: str, item_list: list) -> list:
        column_list = []
        where_value_list = []

        random_index = random.randint(0, len(item_list))
        random_item = item_list[random_index]
        key_list = list(random_item.keys())
        for i, key in enumerate(key_list):
            column_list.append(f"{key}")
            if i == 0:
                where_key_str = f"{key}"

        for item in item_list:
            value_list = list(item.values())
            for i, value in enumerate(value_list):
                if i == 0:
                    where_value_list.append(f"'{value}'")

        pre_item_list_str = ",".join(where_value_list)
        where_str = f" {where_key_str} in ({pre_item_list_str}) "
        query_result_list = self.query(
            table_name
            , column=column_list
            , where=where_str
            , result_type="dict"
        )
        return [{k: str(v) for k, v in item.items()} for item in query_result_list]

    @staticmethod
    def compare(item_list: list, query_result_list: list) -> tuple:
        accordance_result_list = []
        inconsistent_result_list = []
        if query_result_list:
            for item in item_list:
                if item in query_result_list:
                    accordance_result_list.append(item)
                else:
                    inconsistent_result_list.append(item)

            return inconsistent_result_list, accordance_result_list
        else:
            inconsistent_result_list = item_list
            return inconsistent_result_list, accordance_result_list


class AccordantCheckByFile(BaseAccordantCheck):
    """
    通过 文件来校验 文件内容和数据库中的内容是否一致
    """

    def __init__(self, config=DEFAULT_DB_CONNECTION_CONFIG):
        super().__init__(config=config)

    @abstractmethod
    def pre_handle_read_lines(self, lines: list) -> list:
        """ 对读取到的内容进行预处理 """
        raise NotImplementedError

    def check_by_file(self, table_name: str
                      , import_table_column_list: list
                      , batch_size: int = 500
                      , is_need_pre_formatter: bool = False
                      , pre_formatter_index: int = 0
                      , export_file_name_suffix: str = None
                      , optional: str = "str"):
        if not check_file(import_csv_path, import_table_column_list):
            msg = f"文件检查没有通过"
            raise RuntimeError(msg)
        lines = read_file(import_csv_path, is_skip_first_line=False)
        lines = self.pre_handle_read_lines(lines)
        columns = lines.pop(0)
        columns = [col.lower() for col in columns]
        item_list = []
        if is_need_pre_formatter:
            for line in lines:
                item = {}
                for i, col in enumerate(columns):
                    if i == pre_formatter_index:
                        item[col] = filter_symbol_4_word(line[i])
                    else:
                        item[col] = line[i]
                item_list.append(item)
        else:
            for line in lines:
                item = {}
                for i, col in enumerate(columns):
                    item[col] = line[i]
                item_list.append(item)
        accordance_result_list, inconsistent_result_list = self.do_check(table_name, item_list, batch_size,
                                                                         optional=optional)
        export_accordance_list = [list(item.values()) for item in accordance_result_list]
        write_file_quick(export_accordance_list, export_file_name="一致", prefix=table_name,
                         suffix=export_file_name_suffix)
        export_inconsistent_list = [list(item.values()) for item in inconsistent_result_list]
        write_file_quick(export_inconsistent_list, export_file_name="不一致", prefix=table_name,
                         suffix=export_file_name_suffix)
        self.logger.info(f"校验 {export_file_name_suffix} 任务完成")


#############################
###文件数据在mysql中是否存在###
#############################

class BaseExistCheck(MySql):
    """
    检查数据库中是否存在
    """

    def __init(self):
        super().__init__(config=DEFAULT_DB_CONNECTION_CONFIG)

    def do_check(self, table_name: str, column_str: str, need_check_list: list, batch_size: int = 500,
                 optional: str = "str") -> tuple:
        absent_result_list = []
        present_result_list = []
        temp_source_list = []
        for i, source in enumerate(need_check_list):
            temp_source_list.append(source)
            if i > 0 and i % batch_size == 0:
                temp_absent_list, temp_present_list = self.do_query(table_name, column_str, temp_source_list,
                                                                    optional=optional)
                if temp_absent_list:
                    absent_result_list.extend(temp_absent_list)
                if temp_present_list:
                    present_result_list.extend(temp_present_list)
                temp_source_list.clear()
        else:
            temp_absent_list, temp_present_list = self.do_query(table_name, column_str, temp_source_list,
                                                                optional=optional)
            if temp_absent_list:
                absent_result_list.extend(temp_absent_list)
            if temp_present_list:
                present_result_list.extend(temp_present_list)
            temp_source_list.clear()
        return absent_result_list, present_result_list

    def do_query(self, table_name: str, column_str: str, item_list: list, optional: str = "str") -> tuple:
        if "str" == optional:
            return self.query_by_str(table_name, column_str, item_list)
        elif "int" == optional:
            return self.query_by_int(table_name, column_str, item_list)
        else:
            msg = f"暂 仅支持 char 或 int , 不支持 {optional}"
            raise RuntimeError(msg)

    def query_by_int(self, table_name: str, column_str: str, item_list: list) -> tuple:
        pre_item_list_str = ",".join(item_list)
        where_str = f" {column_str} in ({pre_item_list_str}) "
        query_result_list = self.query(
            table_name
            , column_str=f" distinct {column_str} "
            , where=where_str
            , result_type="list"
        )
        item_list = [int(item) for item in item_list]
        return self.compare(item_list, query_result_list)

    def query_by_str(self, table_name: str, column_str: str, item_list: list) -> tuple:

        pre_item_list_str = "','".join(item_list)
        where_str = f" {column_str} in ('{pre_item_list_str}') "
        query_result_list = self.query(
            table_name
            , column_str=f" distinct {column_str} "
            , where=where_str
            , result_type="list"
        )
        return self.compare(item_list, query_result_list)

    @staticmethod
    def compare(item_list: list, query_list: list) -> tuple:
        present_result_list = []
        absent_result_list = []
        if query_list:
            query_result_list = [query[0] for query in query_list]
            if len(query_result_list) == len(item_list):
                present_result_list = query_result_list
                return absent_result_list, present_result_list
            else:
                for i in item_list:
                    if i in query_result_list:
                        present_result_list.append(i)
                    else:
                        absent_result_list.append(i)

                return absent_result_list, present_result_list
        else:
            absent_result_list = item_list
            return absent_result_list, present_result_list


class ExistCheckByFile(BaseExistCheck):
    """
    通过文件检查数据库中是否存在文件中的内容
    """

    def __init__(self):
        super().__init__()

    def check_by_file(self, table_name: str, column_str: str, batch_size: int = 500
                      , is_need_pre_formatter: bool = False, target_index: int = 0
                      , export_file_name_suffix: str = None, optional: str = "str"):
        lines = read_file(import_csv_path, is_skip_first_line=False)
        if is_need_pre_formatter:
            item_list = [filter_symbol_4_word(line[target_index]) for line in lines]
        else:
            item_list = [line[target_index] for line in lines]
        new_item_list = list(set(item_list))
        original = len(item_list)
        distinct = len(new_item_list)
        absent_result_list, present_result_list = self.do_check(table_name, column_str, new_item_list, batch_size,
                                                                optional=optional)
        export_absent_list = [[check] for check in absent_result_list]
        write_file_quick(export_absent_list, export_file_name="缺少", prefix=table_name, suffix=export_file_name_suffix)
        export_present_list = [[check] for check in present_result_list]
        write_file_quick(export_present_list, export_file_name="存在", prefix=table_name,
                         suffix=export_file_name_suffix)
        self.logger.info(f"原来有: {original} 条, 去重后有: {distinct} 条")


#############################
###    Es数据导出到文件    ###
#############################
class Es2File(Es):

    def __init__(self, es_config: EsConnectionConfig, export_file_name: str = "从es中导出"):
        super().__init__(es_config=es_config)
        self.export_file_name = export_file_name

    @abstractmethod
    def handle_export_data_list(self, item_list: List[dict]) -> list:
        pass

    def export_file(self, item_list: List[dict]):
        line_list = self.handle_export_data_list(item_list)
        write_file_quick(line_list, export_file_name=self.export_file_name, write_type="append")

    def export_es_data_2_file(self, query_body: dict):
        self.query_by_scroll(query_body=query_body, handle_func=self.export_file)


#############################
###   Es数据导出到mysql    ###
#############################
class Es2MySql(object):

    def __init__(self, es_config: EsConnectionConfig, db_config: MysqlConnectionConfig):
        super().__init__()
        self.es = Es(es_config)
        self.mysql = MySql(db_config)
        self.start_end_tuple_list = None
        self.update_key_prefix = None
        self.condition = None
        self.end = None
        self.start = None
        self.exclude_properties = None
        self.is_only_print_sql = None
        self.optional = None
        self.batch_size = None
        self.table_name = None

    @abstractmethod
    def handle_export_data_list(self, item_list: List[dict]) -> List[dict]:
        pass

    def import_mysql(self, item_list: List[dict]):
        handle_item_list = self.handle_export_data_list(item_list)
        self.mysql.batch_update_by_item_list(handle_item_list, self.table_name, batch_size=self.batch_size,
                                             optional=self.optional,
                                             is_only_print_sql=self.is_only_print_sql,
                                             exclude_properties=self.exclude_properties,
                                             start=self.start, end=self.end, condition=self.condition,
                                             update_key_prefix=self.update_key_prefix,
                                             start_end_tuple_list=self.start_end_tuple_list)

    def export_es_data_2_mysql(self
                               , query_body: dict
                               , table_name: str
                               , batch_size=100
                               , optional: str = None
                               , is_only_print_sql: bool = False
                               , exclude_properties: list = None
                               , start: int = None
                               , end: int = None
                               , condition: dict = None
                               , start_end_tuple_list: list = None
                               , update_key_prefix: str = None
                               ):
        self.start_end_tuple_list = start_end_tuple_list
        self.update_key_prefix = update_key_prefix
        self.condition = condition
        self.end = end
        self.start = start
        self.exclude_properties = exclude_properties
        self.is_only_print_sql = is_only_print_sql
        self.optional = optional
        self.batch_size = batch_size
        self.table_name = table_name
        self.es.query_by_scroll(query_body=query_body, handle_func=self.import_mysql)


#############################
###   mysql数据同步到Es    ###
#############################

class MySql2Es(object):
    def __init__(self, es_config: EsConnectionConfig, db_config: MysqlConnectionConfig):
        super().__init__()
        self.es = Es(es_config)
        self.mysql = MySql(db_config)
        self.id_column = "id"
        self.batch_size = 10000
        self.is_only_print_sql = False
        self.optional = "Update"

    def sync_from_mysql_2_es(self
                             , table_name: str
                             , where: str = None
                             , column: list = None
                             , column_str: str = None
                             , batch_size: int = 10000
                             , distinct: bool = False
                             , datetime_formatter: str = None
                             , is_fixed_start: bool = False
                             , optional: str = "Update"
                             , id_column: str = "id"
                             , is_only_print_sql: bool = False
                             ):
        self.optional = optional
        self.id_column = id_column
        self.batch_size = batch_size
        self.is_only_print_sql = is_only_print_sql
        self.mysql.batch_handle_db_data_by_generator(table_name
                                                     , where=where
                                                     , column=column
                                                     , column_str=column_str
                                                     , batch_size=batch_size
                                                     , distinct=distinct
                                                     , datetime_formatter=datetime_formatter
                                                     , is_fixed_start=is_fixed_start
                                                     , handle_func=self.handle_query_result
                                                     )

    def handle_query_result(self, one_generator_return_list):
        result_list_init = self.pre_handle_db_query_result_list(one_generator_return_list)
        result_list = [item for item in result_list_init if item]
        if "Update" == self.optional:
            self.es.batch_update_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        elif "Insert" == self.optional:
            self.es.batch_insert_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        elif "InsertOrUpdate" == self.optional:
            self.es.batch_insert_or_update_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        elif "Delete" == self.optional:
            self.es.batch_delete_es(
                result_list
                , is_only_print_sql=self.is_only_print_sql
                , batch_size=self.batch_size
                , id_column=self.id_column
            )
        else:
            msg = f"只支持[Update, Delete, Insert, InsertOrUpdate]操作, 不支持当前操作{self.optional}"
            raise RuntimeError(msg)

    @abstractmethod
    def pre_handle_db_query_result_list(self, pre_result_list: List[dict]) -> List[dict]:
        raise NotImplementedError


#############################
###    文件数据同步到Es    ###
#############################

class File2Es(FileUtil):

    def __init__(self, es_config: EsConnectionConfig, base_dir_path: str = import_dir_path,
                 import_table_column_list: list = None):
        super().__init__(base_dir_path=base_dir_path, import_table_column_list=import_table_column_list)
        self.es = Es(es_config)
        self.id_column = "id"
        self.batch_size = 10000
        self.is_only_print_sql = False
        self.optional = "Update"

    @abstractmethod
    def pre_handle_file_read_result_list(self, pre_result_list: List[dict]) -> List[dict]:
        pass

    def sync_by_dir(self
                    , batch_size: int = 5000
                    , optional: str = "Update"
                    , is_only_print_sql: bool = True
                    , id_column: str = "id"
                    ):
        self.optional = optional
        self.id_column = id_column
        self.batch_size = batch_size
        self.is_only_print_sql = is_only_print_sql
        self.handle_dir()

    def handle_file(self, file_path):
        pre_result_list = self.file_read(file_path)
        if pre_result_list:
            self.logger.info(f"读取 文件 完成 共 {len(pre_result_list)} 条")
            result_list = self.pre_handle_file_read_result_list(pre_result_list)
            if result_list:
                self.logger.info(f"对从 文件 中读取的结果预处理完成 共 {len(pre_result_list)} 条需要更新到Es中")
                if "Update" == self.optional:
                    self.es.batch_update_es(
                        result_list
                        , is_only_print_sql=self.is_only_print_sql
                        , batch_size=self.batch_size
                        , id_column=self.id_column
                    )
                elif "Insert" == self.optional:
                    self.es.batch_insert_es(
                        result_list
                        , is_only_print_sql=self.is_only_print_sql
                        , batch_size=self.batch_size
                        , id_column=self.id_column
                    )
                elif "InsertOrUpdate" == self.optional:
                    self.es.batch_insert_or_update_es(
                        result_list
                        , is_only_print_sql=self.is_only_print_sql
                        , batch_size=self.batch_size
                        , id_column=self.id_column
                    )
                elif "Delete" == self.optional:
                    self.es.batch_delete_es(
                        result_list
                        , is_only_print_sql=self.is_only_print_sql
                        , batch_size=self.batch_size
                        , id_column=self.id_column
                    )
                else:
                    msg = f"只支持[Update, Delete, Insert, InsertOrUpdate]操作, 不支持当前操作{self.optional}"
                    raise RuntimeError(msg)
        else:
            self.logger.info(f"读取 文件 完成, 但没有获取到需要处理的数据.")
