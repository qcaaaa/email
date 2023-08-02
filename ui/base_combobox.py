
from loguru import logger
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QComboBox, QListWidget, QListWidgetItem
from typing import Tuple


class BaseComboBox(QtWidgets.QWidget):
    def __init__(self, parent, tuple_size: Tuple[int, ...] = None, lst_data: list = None,
                 file_style: str = '', is_clear: bool = True):
        """
        :param parent: 继承父类
        :param tuple_size: 放置位置、大小元组
        :param lst_data:  数据源
        :param file_style: 加载样式
        :param is_clear: 是否清空初始值
        """
        super().__init__(parent)
        self.parent = parent
        self.tuple_size = tuple_size
        self.lst_data = lst_data
        self.file_style = file_style
        self.is_clear = is_clear
        self.comboBox = QComboBox(self.parent)
        self.lineEdit = QLineEdit()
        self.listWidget = QListWidget(self.parent)
        self.listWidget.setStyleSheet(self.file_style)
        self.listWidget.itemClicked.connect(self.updateLineEdit)
        if self.lst_data:
            self.allItem = self.set_data('全选')

    def set_data(self, str_data: str):
        item = QListWidgetItem(self.listWidget)
        item.setText(str_data)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        return item

    @property
    def box(self) -> QComboBox:

        if self.tuple_size:
            self.comboBox.setGeometry(QtCore.QRect(*self.tuple_size))
        if self.lineEdit:
            self.comboBox.setLineEdit(self.lineEdit)
        if self.file_style:
            self.comboBox.setStyleSheet(self.file_style)

        for i in self.lst_data:
            self.set_data(i)

        if self.lst_data:
            self.comboBox.setModel(self.listWidget.model())
            self.comboBox.setView(self.listWidget)

            if self.is_clear:
                self.lineEdit.clear()
        return self.comboBox

    def updateLineEdit(self, item):
        lst_data = []
        try:
            state = item.checkState()
            if item.text() == '全选':
                for i in range(self.listWidget.count()):
                    self.listWidget.item(i).setCheckState(state)
                    if state and i != 0:
                        lst_data.append(self.listWidget.item(i).text())
                self.lineEdit.setText(",".join(lst_data))
            else:
                curr_text = self.lineEdit.text()
                if state:
                    self.lineEdit.setText(f'{curr_text},{item.text()}' if curr_text else item.text())
                else:
                    self.lineEdit.setText(','.join(set(curr_text.split(',')) - {item.text()}))
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

