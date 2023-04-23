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
                 str_tip: str = '', file_style: str = '', str_name: str = '', func: Callable = None, str_text: str = ''):
        """为 '' 表示不设置
        :param parent: 继承父类
        :param tuple_size: 按钮 放置位置、大小元组
        :param str_img: 图片
        :param str_tip: tip显示
        :param file_style: 加载样式  文件内容
        :param str_name: obj name
        :param func: 绑定事件
        :param str_text: 按钮内容
        """
        self.parent = parent
        self.tuple_size = tuple_size
        self.str_img = str_img
        self.str_tip = str_tip
        self.file_style = file_style
        self.str_name = str_name
        self.func = func
        self.str_text = str_text

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
        if self.str_text:
            obj_btu.setText(self.str_text)
        if self.func:
            obj_btu.clicked.connect(self.func)
        return obj_btu


class BaseLabel:
    """label 基类"""

    def __init__(self, parent: object, tuple_size: Tuple[int, int, int, int] = None, str_img: str = '',
                 str_text: str = '', str_tip: str = '', str_name: str = ''):
        """为 '' 表示不设置
        :param parent: 继承父类
        :param tuple_size: label 放置位置、大小元组
        :param str_img: 图片
        :param str_text: 文字内容
        :param str_tip: tip显示
        :param str_name: obj name
        """
        self.parent = parent
        self.tuple_size = tuple_size
        self.str_img = str_img
        self.str_text = str_text
        self.str_tip = str_tip
        self.str_name = str_name

    @property
    def label(self) -> QLabel:
        obj_lab = QLabel(self.parent)
        if self.tuple_size:
            obj_lab.setGeometry(QtCore.QRect(*self.tuple_size))
        if self.str_text:
            obj_lab.setText(self.str_text)
        if self.str_tip:
            obj_lab.setToolTip(self.str_tip)
        if self.str_img:
            pix = QPixmap(self.str_img)
            obj_lab.setPixmap(pix)
        if self.str_name:
            obj_lab.setObjectName(self.str_name)
        return obj_lab


class BaseLineEdit:
    """QLineEdit 基类"""

    def __init__(self, parent: object, tuple_size: Tuple[int, int, int, int] = None, file_style: str = '',
                 str_default: str = '', str_name: str = ''):
        """
        :param parent: 继承父类
        :param tuple_size: LineEdit 放置位置、大小元组
        :param file_style: 加载样式
        :param str_default: 默认值
        :param str_name: obj name
        """
        self.parent = parent
        self.tuple_size = tuple_size
        self.file_style = file_style
        self.str_default = str_default
        self.str_name = str_name

    @property
    def lineedit(self) -> QLineEdit:
        obj_line = QLineEdit(self.parent)
        if self.tuple_size:
            obj_line.setGeometry(QtCore.QRect(*self.tuple_size))
        if self.file_style:
            obj_line.setStyleSheet(self.file_style)
        if self.str_name:
            obj_line.setObjectName(self.str_name)
        if self.str_default:
            obj_line.setPlaceholderText(self.str_default)
        return obj_line