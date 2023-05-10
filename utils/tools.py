# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : tools.py

@Email: yypqcaa@163.com

@Date : 2023/4/17 21:57

@Desc :
"""

import os
from json import load
import win32com.client
from loguru import logger


def sub_html(str_html: str) -> str:
    try:
        import re
        str_html = '\n'.join(re.findall('<p .*</p>', str_html))
    except Exception as err:
        logger.error(f'截取html失败: {err.__traceback__.tb_lineno}: {err}')
    return str_html


def word_2_html(str_file: str) -> str:
    """word文件转html"""
    word = None
    doc = None
    str_html = ''
    try:
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = 0  # 后台运行
        word.DisplayAlerts = 0  # 不显示，不警告
        doc = word.Documents.Open(str_file)
        doc.SaveAs(f"{str_file}.html", 10)
        with open(f"{str_file}.html", 'r') as f:
            str_html = f.read()
        if doc:
            doc.Close()
        if word:
            word.Quit()
    except Exception as e:
        logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
    finally:
        try:
            os.remove(f"{str_file}.html")
        except:
            pass
        return str_html


def load_file(str_file: str = 'email.json'):
    from constant import CONFIG_PATH

    dit_info = {}
    try:
        with open(os.path.join(CONFIG_PATH, str_file), 'r', encoding='utf-8') as f:
            dit_info = load(f)
    except Exception as err_msg:
        logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
    return dit_info


def get_qss_style():
    from constant import STATIC_PATH

    file_style = ''
    try:
        with open(os.path.join(STATIC_PATH, 'css', 'QSS.qss'), 'r', encoding='utf-8') as f:
            file_style = f.read()
    except Exception as err_msg:
        logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
    return file_style


def str_2_int(str_num: str, int_def: int = -1):
    try:
        int_num = int(str_num)
    except:
        int_num = int_def
    return int_num
