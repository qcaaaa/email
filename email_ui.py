# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_ui.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 21:47

@Desc :
"""
from loguru import logger
from PyQt5.QtWidgets import QDialogButtonBox, QTextEdit
from PyQt5.QtWidgets import QListWidget, QStackedWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog, QFormLayout
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView
from PyQt5.Qt import QTableWidgetItem
from constant import FONT_SIZE, FIRST_TAB, FONT_WEIGHT, DIT_LIST
from email_tool import EmailTools


class EmailUi(QWidget):
    def __init__(self):
        super(EmailUi, self).__init__()
        self.setWindowIcon(QIcon('./images/logo.png'))
        self.setObjectName('Email-Tool')
        self.resize(1400, 1000)
        self.setMaximumSize(1400, 1000)
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop) if int(newTop) > 60 else 0)
        self.setWindowTitle('Email-Tool')
        self.obj_tool = EmailTools(self)

        with open('./css/QPushButtonQSS.qss', 'r', encoding='utf-8') as f:
            button_style = f.read()

        # ################# 分页 开始....########################################
        self.page_up = QPushButton(self)
        self.page_up.setGeometry(QtCore.QRect(525, 760, 80, 30))
        self.page_up.setText(QtCore.QCoreApplication.translate("Telegram-Tool", "上一页"))
        self.page_up.setDisabled(True)
        self.page_up.setStyleSheet(button_style)
        self.page_up.clicked.connect(self.page_turning)

        self.page_text = QLabel(self)
        self.page_text.setGeometry(QtCore.QRect(625, 760, 40, 30))
        self.page_text.setAlignment(Qt.AlignCenter)
        self.page_text.setText(QtCore.QCoreApplication.translate("Email-Tool", "1/1"))

        self.page_down = QPushButton(self)
        self.page_down.setGeometry(QtCore.QRect(685, 760, 80, 30))
        self.page_down.setText(QtCore.QCoreApplication.translate("Email-Tool", "下一页"))
        self.page_down.setDisabled(True)
        self.page_down.setStyleSheet(button_style)
        self.page_down.clicked.connect(self.page_turning)

        self.page_text_2 = QLineEdit(self)
        self.page_text_2.textChanged.connect(self.text_changed)
        self.page_text_2.setGeometry(QtCore.QRect(785, 760, 70, 30))

        self.page_skip = QPushButton(self)
        self.page_skip.setGeometry(QtCore.QRect(875, 760, 80, 30))
        self.page_skip.setText(QtCore.QCoreApplication.translate("Email-Tool", "跳转"))
        self.page_skip.setDisabled(True)
        self.page_skip.setStyleSheet(button_style)
        self.page_skip.clicked.connect(self.page_turning)
        # ################# 分页 结束....########################################

        with open('./css/QListWidgetQSS.qss', 'r', encoding='utf-8') as f:  # 导入QListWidget的qss样式
            list_style = f.read()

        self.main_layout = QHBoxLayout(self)  # 窗口的整体布局
        # 上面留60 下面留250
        self.main_layout.setContentsMargins(0, 60, 0, 250)
        # 左侧选项列表
        self.left_widget = QListWidget()
        self.left_widget.setStyleSheet(list_style)
        # 左侧绑定 点击事件
        self.left_widget.itemClicked.connect(self.display)
        self.main_layout.addWidget(self.left_widget)

        # 右侧
        self.right_widget = QStackedWidget()
        self.main_layout.addWidget(self.right_widget)

        # 下侧 日志框
        self.log_label = QLabel(self)
        self.log_label.setGeometry(QtCore.QRect(0, 1400, 100, 30))
        self.log_label.setAlignment(Qt.AlignLeft)
        self.log_label.setText(QtCore.QCoreApplication.translate("Email-Tool", "日志输出:"))
        self.log_label.setStyleSheet('color:red;font:bold 15px;')

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # 只读
        self.log_text.setGeometry(QtCore.QRect(0, 810, 690, 185))

        self.page = FIRST_TAB

        self._setup_ui()

    def _setup_ui(self):
        """加载界面ui"""
        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定

        self.left_widget.setFrameShape(QListWidget.NoFrame)  # 去掉边框

        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(FONT_SIZE)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(FONT_WEIGHT)
        font.setKerning(True)

        for keys, values in DIT_LIST.items():
            self.item = QListWidgetItem(keys, self.left_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(30, 60))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示

    def page_turning(self):
        pass

    def text_changed(self):
        pass

    def display(self, item):
        """左侧主菜单点击事件"""
        try:
            str_items = str(item.text())
            if self.page != str_items:
                self.page = str_items  # 记住当前在哪个页面
                self.obj_tool.show_message('', '', f'切换到 {str_items}页面')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")