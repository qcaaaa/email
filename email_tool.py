# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_tool.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 22:11

@Desc :
"""
import os
from json import load
from loguru import logger
from datetime import datetime
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QPlainTextEdit

from sql_db import MySql
from constant import INT_LIMIT, BASE_PATH


class EmailTools:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui
        self.email_dict = self.load_file()

    @staticmethod
    def get_info(table: str, where: str = '', int_start: int = 1, int_limit: int = INT_LIMIT):
        """获取数据库信息"""
        with MySql() as obj_sql:
            dit_info = obj_sql.select_sql(table, int_start=int_start, int_limit=int_limit)
        return dit_info

    @staticmethod
    def del_info(table: str, int_id: int) -> int:
        """删除数据库信息"""
        with MySql() as obj_sql:
            int_ret = obj_sql.del_sql(table, int_id)
        return int_ret

    @staticmethod
    def load_file():
        dit_info = {}
        try:
            with open(os.path.join(BASE_PATH, 'email.json'), 'r', encoding='utf-8') as f:
                dit_info = load(f)
        except Exception as err_msg:
            logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
        return dit_info

    def show_message(self, title: str = '', text: str = '', info: str = ''):
        try:
            if title and text:
                QMessageBox.information(self.obj_ui, title, text, QMessageBox.Yes)
            if info:
                self.obj_ui.log_text.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {info}")
                self.obj_ui.log_text.moveCursor(QTextCursor.End)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")