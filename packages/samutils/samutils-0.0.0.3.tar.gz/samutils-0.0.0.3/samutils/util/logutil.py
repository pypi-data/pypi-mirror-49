import logging
import os

from samutils import default_dir_file_path, default_log_file_path

default_formatter = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"

default_date_fmt = "%Y-%m-%d %H:%M:%S"

_logger_level_dict = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "critical": logging.CRITICAL,
    "error": logging.ERROR
}


class LoggerUtil(object):
    def __init__(self, name: str = "temp", level: str = None):
        super().__init__()
        self.name = name
        # 创建一个logger
        self.logger = logging.getLogger(self.name)
        self.level = _logger_level_dict.get(level, logging.INFO)
        # logger的总开关，只有大于Debug的日志才能被logger对象处理
        self.logger.setLevel(self.level)
        # 加了一步 判断文件夹是否存在
        if not os.path.exists(default_dir_file_path):
            os.makedirs(default_dir_file_path)
        # 创建一个handler，用于写入日志文件
        file_handler = logging.FileHandler(default_log_file_path, mode='a', encoding="utf-8")
        file_handler.setLevel(logging.ERROR)  # 输出到file的log等级的开关
        # 创建该handler的formatter
        file_handler.setFormatter(
            logging.Formatter(
                fmt=default_formatter,
                datefmt=default_date_fmt)
        )
        # 添加handler到logger中
        self.logger.addHandler(file_handler)

        # 第三步，创建一个handler，用于输出到控制台
        console_handler = logging.StreamHandler()
        # 输出到控制台的log等级的开关
        console_handler.setLevel(logging.INFO)
        # 创建该handler的formatter
        console_handler.setFormatter(
            logging.Formatter(
                fmt=default_formatter,
                datefmt=default_date_fmt)
        )
        self.logger.addHandler(console_handler)


def get_default_logger():
    default_logger = logging.getLogger("default")
    default_logger.setLevel(logging.INFO)  # logger的总开关，只有大于Debug的日志才能被logger对象处理

    # 加了一步 判断文件夹是否存在
    if not os.path.exists(default_dir_file_path):
        os.makedirs(default_dir_file_path)
    # 第二步，创建一个handler，用于写入日志文件
    file_handler = logging.FileHandler(default_log_file_path, mode='w', encoding="utf-8")
    file_handler.setLevel(logging.ERROR)  # 输出到file的log等级的开关
    # 创建该handler的formatter
    file_handler.setFormatter(
        logging.Formatter(
            fmt=default_formatter,
            datefmt=default_date_fmt)
    )
    # 添加handler到logger中
    default_logger.addHandler(file_handler)

    # 第三步，创建一个handler，用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 输出到控制台的log等级的开关
    # 创建该handler的formatter
    console_handler.setFormatter(
        logging.Formatter(
            fmt=default_formatter,
            datefmt=default_date_fmt)
    )
    default_logger.addHandler(console_handler)
    return default_logger
