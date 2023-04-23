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

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from loguru import logger
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QMessageBox

from ui.base_ui import BaseButton
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
        self.resize(400, 130)
        # self.setStyleSheet("background-image:url(Background.jpg)")
        user_label = QLabel(self)
        user_label.setGeometry(QtCore.QRect(200, 24, 20, 15))
        user_label.setTextFormat(QtCore.Qt.AutoText)
        user_pix = QPixmap(os.path.join(STATIC_PATH, 'images', 'user.png'))
        user_label.setPixmap(user_pix)
        user_label.setToolTip('用户名')
        self.user_line = QLineEdit(self)
        self.user_line.setGeometry(QtCore.QRect(250, 20, 100, 20))
        pwd_label = QLabel(self)
        pwd_label.setGeometry(QtCore.QRect(200, 54, 20, 15))
        pwd_label.setTextFormat(QtCore.Qt.AutoText)
        pwd_pix = QPixmap(os.path.join(STATIC_PATH, 'images', 'pwd.png'))
        pwd_label.setPixmap(pwd_pix)
        pwd_label.setToolTip('密码')
        self.pwd_line = QLineEdit(self)
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.pwd_line.setGeometry(QtCore.QRect(250, 50, 100, 20))
        self.pwd_line.textChanged.connect(self.text_changed)

        self.login_btu = BaseButton(self, (290, 90, 75, 23), func=self.login).btu
        self.login_btu.setText('登录')
        self.login_btu.setDisabled(True)

        quit_btu = BaseButton(self, (190, 90, 75, 23), func=self.close).btu
        quit_btu.setText('取消')

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
            try:
                QMessageBox.warning(self, '错误', '账号或者密码不对！', QMessageBox.Yes)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    app = QApplication([])
    obj_a = MyTelegram()
    obj_a.show()
    sys.exit(app.exec_())
