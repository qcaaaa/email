# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : main.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 21:47

@Desc :
"""
import sys
import os
import psutil
import traceback

from loguru import logger
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication

from ui.main_ui import EmailUi


def handleException(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        return sys.__excepthook__(exc_type, exc_value, exc_traceback)
    exception = str("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    dialog = QtWidgets.QDialog()
    # close对其进行删除操作
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    msg = QtWidgets.QMessageBox(dialog)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(exception)
    msg.setWindowTitle("系统异常提示")
    msg.setDetailedText(exception)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

    msg.exec_()


class MyTool:
    def __init__(self):
        from constant import LOG_PATH, EMAIL_CHECK_PATH, EMAIL_SEARCH_PATH, EXE_NAME

        self.user_line = None
        self.pwd_line = None
        self.login_btu = None

        self.close_program(EXE_NAME)

        for str_path in [LOG_PATH, EMAIL_CHECK_PATH, EMAIL_SEARCH_PATH]:
            try:
                if not os.path.isdir(str_path):
                    os.mkdir(str_path, 777)
            except:
                pass

        log_path = os.path.join(LOG_PATH, "log.log")

        if os.path.isfile(log_path) and os.path.getsize(log_path) > 500 * 1024 * 1024:
            try:
                os.remove(log_path)
            except:
                pass

        logger.add(log_path, rotation="500MB", encoding="utf-8", enqueue=True, retention="10 days")

        # 自定义异常
        sys.excepthook = handleException

    @staticmethod
    def close_program(exec_name: str):
        """关闭软件"""
        for proc in psutil.process_iter():
            try:
                # 检查进程名称是否匹配
                if proc.name() == exec_name:
                    sys.exit(0)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


if __name__ == '__main__':
    obj_init = MyTool()
    app = QApplication([])
    obj_a = EmailUi()
    sys.exit(app.exec_())
