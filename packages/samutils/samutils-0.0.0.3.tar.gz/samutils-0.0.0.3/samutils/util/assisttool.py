import datetime
from typing import Union


def list2dict(column: list, result: list) -> dict:
    if not column or not result:
        raise RuntimeWarning("传入的参数不能为空")
    res_dict = {}
    for i, col in enumerate(column):
        if " : " in col:
            arr = col.split(" : ")
            pre_col_name = arr[0].strip()
            col_type = arr[1].strip()
        else:
            pre_col_name = col
            col_type = None
        if " as " in pre_col_name:
            col_name = pre_col_name.split(" as ")[1].strip()
        else:
            col_name = pre_col_name
        if col_type:
            if "int" == col_type:
                res_dict[col_name] = int(result[i]) if result[i] else 0
            elif "str" == col_type:
                res_dict[col_name] = str(result[i]) if result[i] else ''
            elif "float" == col_type:
                res_dict[col_name] = float(result[i]) if result[i] else 0.0
            else:
                res_dict[col_name] = result[i]
        else:
            res_dict[col_name] = result[i]
    return res_dict


#############################
###   日期时间辅助工具     ###
#############################


def formatter_datetime_2_iso8601(t: Union[datetime.date, datetime.time, datetime.datetime]):
    """
    格式化 日期时间 为 iso8601 格式字符串
    :param t:
    :return:
    """
    return t.isoformat()


def formatter_datetime_2_str(t: Union[datetime.date, datetime.time, datetime.datetime]):
    """
    根据不同的日期时间类型 格式化成常见的格式字符串
    :param t:
    :return:
    """
    if isinstance(t, datetime.datetime):
        return t.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(t, datetime.time):
        return t.strftime('%H:%M:%S')
    elif isinstance(t, datetime.date):
        return t.strftime("%Y-%m-%d")


def formatter_datetime_2_timestamp(t: Union[datetime.date, datetime.time, datetime.datetime], unit: str):
    """
    将日期或时间格式化成时间戳
    :param t:
    :param unit:
    :return:
    """
    if "second" == unit:
        if t:
            if isinstance(t, datetime.date):
                return datetime.datetime(t.year, t.month, t.day).timestamp()
            else:
                return int(t.timestamp())
        else:
            return None
    elif "millisecond" == unit:
        if t:
            try:
                if isinstance(t, datetime.date):
                    return int(datetime.datetime.fromordinal(t.toordinal()).timestamp() * 1000)
                else:
                    return int(t.timestamp() * 1000)
            except OSError:
                print(f"出问题的时间是 {t}")
                return None
        else:
            return None
    else:
        raise RuntimeWarning("暂只支持 转换为 秒 或 毫秒")


def formatter_datetime(res, datetime_formatter: str = "datetime", unit: str = "millisecond"):
    """
    按照指定格式 格式化时间
    :param res:
    :param datetime_formatter:
    :param unit:
    :return:
    """
    if isinstance(res, datetime.date) \
            or isinstance(res, datetime.time) \
            or isinstance(res, datetime.datetime):

        if datetime_formatter not in ["datetime", "iso8601", "str", "long"]:
            error_msg = f"不支持当前时间格式化类型 {datetime_formatter}, 仅支持 'datetime', 'iso8601', 'str', 'long'"
            raise RuntimeWarning(error_msg)
        if "datetime" == datetime_formatter:
            return res
        elif "iso8601" == datetime_formatter:
            return formatter_datetime_2_iso8601(res)
        elif "str" == datetime_formatter:
            return formatter_datetime_2_str(res)
        elif "long" == datetime_formatter:
            return formatter_datetime_2_timestamp(res, unit)
        else:
            return res
    else:
        return res


def formatter_line(result: list, datetime_formatter: str = None):
    new_result_list = []
    for res in result:
        new_res = formatter_datetime(res, datetime_formatter)
        new_result_list.append(new_res)
    return new_result_list
