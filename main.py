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
        from constant import LOG_PATH, EMAIL_CHECK_PATH, EMAIL_SEARCH_PATH

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


if __name__ == '__main__':
    obj_a = MyTelegram()
    app = QApplication(sys.argv)
    main_wnd = EmailUi()
    main_wnd.show()
    sys.exit(app.exec_())
