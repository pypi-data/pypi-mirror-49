import re

base_filter_start_symbol_re = re.compile("^[`‘’'。.·？?！!，,、/\\\；;：:“ ”\"─\-…—)_]+")

base_filter_end_symbol_re = re.compile("[`‘’'。.·？?！!，,、/\\\；;：:“ ”\"─\-…—(_]+$")

base_filter_global_symbol_re = re.compile(
    "[ \t\n\r·.\s♀♂↑↓←→@!~#$%^&*¤☆★△▲□■○●◎⊙◇◆◤◢◣◥※卐ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ]")

base_convert_left_bracket_re = re.compile("[【[{《〈﹤“「『〖﹄﹂｢]+")

base_convert_right_bracket_re = re.compile("[】\]}》〉﹥”」』〗﹃﹁｣]")

base_convert_zero_re = re.compile("[ＯO〇０○]+")

base_extract_bracket_re = re.compile("\([^)]*\)|（[^）]*）+")

filter_symbol_re_save_space_re = re.compile('[\\\/、,，·。.\'`"*‘’＊?~#@$☆△★▲■:XⅠⅩⅡⅣ※]+$|[\\"]+')


def str_full_width_to_half_width(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def str_half_width_to_full_width(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring


def pre_handle_str(s: str, filter_re=base_filter_global_symbol_re):
    # 全角转换为半角
    new_str = str_full_width_to_half_width(s).strip()
    # 过滤掉特殊符号
    return re.sub(filter_re, "", new_str).strip()


def pre_handle_line(line: list, filter_re=base_filter_global_symbol_re):
    '''
    全角转半角 且 过滤了特殊符号
    :param filter_re:
    :param line:
    :return:
    '''
    return [pre_handle_str(str(s), filter_re=filter_re) if s else None for s in line]


def pre_handle_str_save_space(s: str):
    return pre_handle_str(s, filter_re=filter_symbol_re_save_space_re)


def filter_symbol(original_name: str, is_need_filter_start_end: bool = False) -> str:
    """
    过滤 符号
    1: 全局过滤掉 特殊符号
    2: 过滤掉 开头的符号
    3: 过滤掉 结尾的符号
    :param is_need_filter_start_end:
    :param original_name:
    :return:
    """
    name_processed = re.sub(base_filter_global_symbol_re, "", original_name)
    if is_need_filter_start_end:
        name_processed = re.sub(base_filter_start_symbol_re, "", name_processed)
        name_processed = re.sub(base_filter_end_symbol_re, "", name_processed)
    return name_processed


def formatter_symbol(original_name: str) -> str:
    """
    格式化 符号
    主要 将符号格式化为 ()0
    :param original_name:
    :return:
    """
    name_processed = re.sub(base_convert_left_bracket_re, "(", original_name)
    name_processed = re.sub(base_convert_right_bracket_re, ")", name_processed)
    name_processed = re.sub(base_convert_zero_re, "0", name_processed)
    return name_processed


def filter_symbol_4_word(s: str, is_need_formatter: bool = False):
    ss = str(s)
    # 全角转半角
    ss = str_full_width_to_half_width(ss)
    # 格式化符号
    if is_need_formatter:
        ss = formatter_symbol(ss)
    # 过滤特殊符号
    ss = filter_symbol(ss)
    return ss


def filter_symbol_4_line_with_exclude(line: list, exclude_index_list: list) -> list:
    if exclude_index_list:
        new_line = []
        for i, s in enumerate(line):
            if i in exclude_index_list:
                new_line.append(str(s))
            else:
                # 格式化成 字符串
                ss = filter_symbol_4_word(s)
                new_line.append(ss)
        return new_line
    else:
        return filter_symbol_4_line(line)


def filter_symbol_4_line(line: list) -> list:
    new_line = []
    for s in line:
        ss = filter_symbol_4_word(s)
        new_line.append(ss)
    return new_line
