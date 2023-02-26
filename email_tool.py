# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_tool.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 22:11

@Desc :
"""
from loguru import logger
from datetime import datetime
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QPlainTextEdit


class EmailTools:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui

    def show_message(self, title: str = '', text: str = '', info: str = ''):
        try:
            if title and text:
                QMessageBox.information(self.obj_ui, title, text, QMessageBox.Yes)
            if info:
                self.obj_ui.log_text.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {info}")
                self.obj_ui.log_text.moveCursor(QTextCursor.End)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")