from typing import Tuple, Callable
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextEdit, QScrollBar
from PyQt5.QtWidgets import QMessageBox


class BaseButton:
    """QPushButton 基类"""

    def __init__(self, parent: object, tuple_size: Tuple[int, int, int, int] = None, str_img: str = '',
                 str_tip: str = '', file_style: str = '', str_name: str = '', func: Callable = None):
        """为 '' 表示不设置
        :param parent: 继承父类
        :param tuple_size: 按钮 放置位置、大小元组
        :param str_img: 图片
        :param str_tip: tip显示
        :param file_style: 加载样式  文件内容
        :param str_name: obj name
        :param func: 绑定事件
        """
        self.parent = parent
        self.tuple_size = tuple_size
        self.str_img = str_img
        self.str_tip = str_tip
        self.file_style = file_style
        self.str_name = str_name
        self.func = func

    @property
    def btu(self) -> QPushButton:
        obj_btu = QPushButton(self.parent)
        if self.tuple_size:
            obj_btu.setGeometry(QtCore.QRect(*self.tuple_size))
        if self.str_img:
            obj_btu.setIcon(QIcon(self.str_img))
        if self.str_tip:
            obj_btu.setToolTip(self.str_tip)
        if self.file_style:
            obj_btu.setStyleSheet(self.file_style)
        if self.str_name:
            obj_btu.setObjectName(self.str_name)
        if self.func:
            obj_btu.clicked.connect(self.func)
        return obj_btu
