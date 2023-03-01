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
from loguru import logger
from PyQt5.QtWidgets import QApplication
from ui.email_ui import EmailUi


class MyTelegram:
    def __init__(self):
        pass

    def __call__(self):
        from constant import BASE_PATH
        logger.add(os.path.join(BASE_PATH, "log.log"), rotation="500MB", encoding="utf-8", enqueue=True, retention="10 days")


if __name__ == '__main__':
    obj_a = MyTelegram()
    obj_a()
    app = QApplication(sys.argv)
    main_wnd = EmailUi()
    main_wnd.show()
    sys.exit(app.exec_())
