import traceback
from datetime import datetime

from samutils.util.logutil import get_default_logger

default_logger = get_default_logger()


def _assert_param_non_null(*args, **kwargs):
    b1 = True
    if args:
        for a in args:
            if not a:
                b1 = False
                break
    b2 = True
    if kwargs:
        for m in kwargs:
            if not m:
                b2 = False
                break

    return b1 and b2


def param_null_not_execute(func):
    """
    判断 传入 的 参数 是否 为 空 ， 空 则 不执行 ，
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        if _assert_param_non_null(*args, **kwargs):
            return func(*args, **kwargs)
        else:
            msg = f"出现异常: 参数是 {args} {kwargs}, 有参数为空"
            raise RuntimeError(msg)

    return wrapper


def catch_and_print_exception(func):
    """
    捕获 或 打印 异常
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (Exception, RuntimeError, TypeError, NameError, AttributeError, Warning) as e:
            default_logger.error(f"出现异常: {e} 参数是 {args} {kwargs}")
            default_logger.error(traceback.print_exc())
            # exit()

    return wrapper


def deprecated(tips: str = None):
    """
    声明该方法 已经被废弃 将不会被执行
    :param tips: 提示的内容
    :param func:
    :return:
    """

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            if str:
                print(f"该方法已被弃用，将不会被执行。{tips}")

            raise RuntimeWarning(f"该方法已被弃用，将不会被执行。")

        return inner_wrapper

    return wrapper


def warning(tips: str = None):
    """
    声明该方法 已经被废弃 将不会被执行
    :param tips: 提示的内容
    :param func:
    :return:
    """
    if tips:
        msg = f"该方法还存在问题： {tips} ，使用时请注意."
    else:
        msg = f"该方法还存在问题，使用时请注意."

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print(msg)
            func(*args, **kwargs)

        return inner_wrapper

    return wrapper


def print_task_cost_time(func):
    """
    打印 任务耗时时间
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        print("程序开始执行，任务执行结束后，将输出任务执行时间...")
        start_time = datetime.now()
        func(*args, **kwargs)
        end_time = datetime.now()
        cost_time = (end_time - start_time).seconds
        # cost_time = (end_time - start_time).microseconds/1000
        print(f"执行完了, 此次任务, 耗时：{cost_time} 秒")

    return wrapper
