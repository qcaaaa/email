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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from loguru import logger
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit

from ui.base_ui import BaseButton, BaseLabel, BaseLineEdit
from ui.email_ui import EmailUi


class MyTelegram(QMainWindow):
    def __init__(self):
        super(MyTelegram, self).__init__()
        from constant import LOG_PATH, EMAIL_CHECK_PATH, EMAIL_SEARCH_PATH

        self.user_line = None
        self.pwd_line = None
        self.login_btu = None

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

        self.setup_ui()

    def setup_ui(self):

        from constant import STATIC_PATH

        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'login.png')))
        self.setObjectName('win')
        self.resize(400, 130)
        self.setStyleSheet('#win{border-image:url(./static/images/bj.png);}')

        user_label = BaseLabel(self, (100, 24, 20, 15), str_img=os.path.join(STATIC_PATH, 'images', 'user.png'),
                               str_tip='用户名').label

        self.user_line = BaseLineEdit(self, (150, 20, 120, 20)).lineedit

        pwd_label = BaseLabel(self, (100, 54, 20, 15), str_img=os.path.join(STATIC_PATH, 'images', 'pwd.png'),
                              str_tip='密码').label

        self.pwd_line = BaseLineEdit(self, (150, 50, 120, 20)).lineedit
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.pwd_line.textChanged.connect(self.text_changed)

        self.login_btu = BaseButton(self, (200, 90, 75, 23), func=self.login, str_text='登录').btu
        self.login_btu.setDisabled(True)
        self.login_btu.setShortcut(Qt.Key_Return)  # 绑定快捷键

        quit_btu = BaseButton(self, (100, 90, 75, 23), func=self.close, str_text='取消').btu

    def text_changed(self, text):
        if text and self.user_line.text():
            self.login_btu.setEnabled(True)
        else:
            self.login_btu.setDisabled(True)

    def login(self):
        if self.user_line.text() == 'admin' and self.pwd_line.text() == 'admin':
            main_wnd = EmailUi()
            main_wnd.show()
            self.close()
        else:
            QMessageBox.warning(self, '错误', '账号或者密码不对！', QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication([])
    obj_a = MyTelegram()
    obj_a.show()
    sys.exit(app.exec_())
