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
import base64
import win32com.client
from loguru import logger
from json import load, dump, dumps, loads
from gmssl.sm4 import CryptSM4, SM4_DECRYPT, SM4_ENCRYPT

AES_KEY = b'\x8a\x05\xc5\xce\xbb;[\xa6\xcf\xac[t\x11o\xdf\xe0'


def sub_html(str_html: str) -> str:
    try:
        import re
        str_html = '\n'.join(re.findall('<p .*</p>', str_html))
    except Exception as err:
        logger.error(f'截取html失败: {err.__traceback__.tb_lineno}: {err}')
    return str_html


def word_2_html(str_file: str) -> str:
    """word文件转html"""
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
    dit_info = {}
    try:
        from constant import CONFIG_PATH

        with open(os.path.join(CONFIG_PATH, str_file), 'r', encoding='utf-8') as f:
            dit_info = load(f)  # type: dict
        if str_file == 'config.json' and dit_info:
            dit_info.update({
                'AccessKey_ID': decrypt_str(dit_info.get('AccessKey_ID', '')),
                'AccessKey_Secret': decrypt_str(dit_info.get('AccessKey_Secret', '')),
                'user': decrypt_str(dit_info.get('user', '')),
                'pwd': decrypt_str(dit_info.get('pwd', '')),
            })
    except Exception as err_msg:
        logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
    return dit_info


def dump_file(dit_conf: dict, str_file: str = 'email.json') -> int:
    int_ret = 0
    try:
        from constant import CONFIG_PATH

        if str_file == 'config.json':
            dit_conf.update({
                'AccessKey_ID': encrypt_str(dit_conf.get('AccessKey_ID', '')),
                'AccessKey_Secret': encrypt_str(dit_conf.get('AccessKey_Secret', '')),
                'user': encrypt_str(dit_conf.get('user', '')),
                'pwd': encrypt_str(dit_conf.get('pwd', '')),
            })
        with open(os.path.join(CONFIG_PATH, str_file), 'w', encoding='utf-8') as f:
            dump(dit_conf, f, indent=4)
        int_ret = 1
    except Exception as err_msg:
        logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
    return int_ret


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


def encrypt_str(str_data):
    """
    :param str_data:
    :return:
    """
    str_ret = ""
    try:
        if isinstance(str_data, list) or isinstance(str_data, dict):
            str_data = dumps(str_data, separators=(',', ':'))
        else:
            str_data = str(str_data)

        str_data = base64.b64encode(str_data.encode('utf8'))

        obj_tmp = CryptSM4()
        obj_tmp.set_key(AES_KEY, SM4_ENCRYPT)

        str_tmp = obj_tmp.crypt_ecb(str_data)
        str_ret = base64.b64encode(str_tmp).decode()
    except Exception as err_msg:
        logger.error(err_msg)
    return str_ret


def decrypt_str(str_data: str, is_json_loads: bool = False):
    """
    :param str_data:
    :param is_json_loads:
    :return:
    """
    try:
        str_data = base64.b64decode(str_data.encode(encoding="utf-8"))

        obj_tmp = CryptSM4()
        obj_tmp.set_key(AES_KEY, SM4_DECRYPT)

        str_ret = base64.b64decode(obj_tmp.crypt_ecb(str_data)).decode()

        if is_json_loads:
            str_ret = loads(str_ret)
    except Exception as err_msg:
        str_ret = {} if is_json_loads else ''
        logger.error(f"{err_msg.__traceback__.tb_lineno}|{err_msg}")
    return str_ret

