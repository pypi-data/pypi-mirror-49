from typing import List, Callable

from elasticsearch import Elasticsearch, helpers
from samutils.util.commonwrapper import catch_and_print_exception

from samutils.util.logutil import LoggerUtil


class EsConnectionConfig(object):
    def __init__(self, es_index: str, doc_type: str, host: str = "localhost", port: int = 9200):
        self.es_index = es_index
        self.doc_type = doc_type
        self.client = Elasticsearch([f"{host}:{port}"], maxsize=25)


DEFAULT_ES_CONFIG = EsConnectionConfig(es_index="sca-tag-client", doc_type="client")


class Es(LoggerUtil):
    """ index update create delete """

    def __init__(self, es_config: EsConnectionConfig):
        super().__init__(name="es")
        self.index = es_config.es_index
        self.doc_type = es_config.doc_type
        self.client = es_config.client
        self.logger.info(f"当前要执行的 索引是 {self.index} , 类型是 {self.doc_type}")

    @catch_and_print_exception
    def batch_insert_or_update_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False,
                                       id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column], "_op_type": 'index',
                              "_source": data}
                if is_only_print_sql:
                    self.logger.info(f"将要执行的 批量 插入或更新 语句是: {new_action}")
                else:
                    action_list.append(new_action)
            if action_list:
                result = helpers.bulk(self.client, action_list)
                self.logger.info(f"批量执行的 插入或更新 的结果是: {result}")

    def batch_insert_or_update_es(self
                                  , result_list: List[dict]
                                  , is_only_print_sql: bool = False
                                  , batch_size: int = 5000
                                  , id_column: str = "id"
                                  ):
        """
        批量插入或更新es
        """
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_insert_or_update_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    self.logger.info(f"完成 第 {num} 个 ")
            else:
                self.batch_insert_or_update_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                self.logger.info(f"完成 第 {num} 个 ")
        else:
            self.logger.info("没有查询到符合条件的数据")

    @catch_and_print_exception
    def batch_part_update_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False, id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column],
                              "_op_type": 'update',
                              "doc": data}
                if is_only_print_sql:
                    self.logger.info(f"将要执行的 批量 部分更新 语句是: {new_action}")
                else:
                    action_list.append(new_action)
            if action_list:
                result = helpers.bulk(self.client, action_list)
                self.logger.info(f"批量执行的 批量 部分更新 的结果是: {result}")

    def batch_update_es(self
                        , result_list: List[dict]
                        , batch_size: int = 5000
                        , is_only_print_sql: bool = False
                        , id_column: str = "id"
                        ):
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_part_update_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    self.logger.info(f"完成 第 {num} 个 ")
            else:
                self.batch_part_update_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                self.logger.info(f"完成 第 {num} 个 ")
        else:
            self.logger.info("没有查询到符合条件的数据")

    @catch_and_print_exception
    def batch_insert_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False, id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                if data.get(id_column):
                    new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column],
                                  "_op_type": 'create',
                                  "_source": data}
                    if is_only_print_sql:
                        self.logger.info(f"将要执行的 批量 插入 语句是: {new_action}")
                    else:
                        action_list.append(new_action)
                else:
                    self.client.index(index=self.index, doc_type=self.doc_type, body=data)

            if action_list:
                result = helpers.bulk(self.client, action_list)
                self.logger.info(f"批量执行的 批量 插入 的结果是: {result}")

    def batch_insert_es(self
                        , result_list: List[dict]
                        , batch_size: int = 5000
                        , is_only_print_sql: bool = False
                        , id_column: str = "id"
                        ):
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_insert_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    self.logger.info(f"完成 第 {num} 个 ")
            else:
                self.batch_insert_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                self.logger.info(f"完成 第 {num} 个 ")
        else:
            self.logger.info("没有查询到符合条件的数据")

    @catch_and_print_exception
    def batch_delete_by_bulk(self, data_list: List[dict], is_only_print_sql: bool = False, id_column: str = "id"):
        action_list = []
        if data_list:
            for data in data_list:
                new_action = {"_index": self.index, "_type": self.doc_type, "_id": data[id_column],
                              "_op_type": 'delete'}
                if is_only_print_sql:
                    self.logger.info(f"将要执行的 删除 语句是: {new_action}")
                else:
                    action_list.append(new_action)
            if action_list:
                result = helpers.bulk(self.client, action_list)
                self.logger.info(f"批量执行的 删除 的结果是: {result}")

    def batch_delete_es(self
                        , result_list: List[dict]
                        , batch_size: int = 5000
                        , is_only_print_sql: bool = False
                        , id_column: str = "id"
                        ):
        num = 0
        temp_res_list = []
        if result_list:
            for result in result_list:
                num += 1
                temp_res_list.append(result)
                if num % batch_size == 0:
                    self.batch_delete_by_bulk(
                        temp_res_list
                        , is_only_print_sql=is_only_print_sql
                        , id_column=id_column
                    )
                    temp_res_list.clear()
                    self.logger.info(f"完成 第 {num} 个 ")
            else:
                self.batch_delete_by_bulk(
                    temp_res_list
                    , is_only_print_sql=is_only_print_sql
                    , id_column=id_column
                )
                temp_res_list.clear()
                self.logger.info(f"完成 第 {num} 个 ")
        else:
            self.logger.info("没有查询到符合条件的数据")

    def query_by_id(self, id_str):
        res = self.client.get(index=self.index, doc_type=self.doc_type, id=id_str)
        if res and res["hits"]["total"] > 0:
            return res["hits"]["hits"]

    def query_by_scroll(self, query_body: dict, handle_func: Callable[[List[dict]], object] = None):
        page = self.client.search(
            index=self.index,
            doc_type=self.doc_type,
            scroll='2m',
            size=10000,
            body=query_body)

        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        page_result = page['hits']['hits']
        result_list = [hits["_source"] for hits in page_result]
        if handle_func:
            handle_func(result_list)

        # Start scrolling
        while scroll_size > 0:
            self.logger.info("Scrolling...")
            page = self.client.scroll(scroll_id=sid, scroll='2m')
            sid = page['_scroll_id']
            page_result = page['hits']['hits']
            result_list = [hits["_source"] for hits in page_result]
            scroll_size = len(result_list)
            self.logger.info("scroll size: " + str(scroll_size))
            if handle_func:
                handle_func(result_list)
