from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QComboBox
from typing import Tuple


class BaseComboBox:
    def __init__(self, parent, tuple_size: Tuple[int, ...] = None, lst_data: list = None,
                 file_style: str = '', is_clear: bool = True):
        """
        :param parent: 继承父类
        :param tuple_size: 放置位置、大小元组
        :param lst_data:  数据源
        :param file_style: 加载样式
        :param is_clear: 是否清空初始值
        """
        self.parent = parent
        self.tuple_size = tuple_size
        self.lst_data = lst_data
        self.file_style = file_style
        self.is_clear = is_clear
        self.comboBox = QComboBox(self.parent)
        self.lineEdit = QtWidgets.QLineEdit(self.parent)
        self.listWidget = QtWidgets.QListWidget(self.parent)
        if self.lst_data:
            self.allItem = QtWidgets.QListWidgetItem(self.listWidget)
            self.allItem.setText("全选")
            self.allItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.allItem.setCheckState(QtCore.Qt.Unchecked)

    @property
    def box(self) -> QComboBox:

        if self.tuple_size:
            self.comboBox.setGeometry(QtCore.QRect(*self.tuple_size))
        if self.lineEdit:
            self.comboBox.setLineEdit(self.lineEdit)
        if self.file_style:
            self.comboBox.setStyleSheet(self.file_style)

        for i in self.lst_data:
            item = QtWidgets.QListWidgetItem(self.listWidget)
            item.setText(i)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

        self.listWidget.itemClicked.connect(self.updateLineEdit)

        self.comboBox.setModel(self.listWidget.model())
        self.comboBox.setView(self.listWidget)

        if self.is_clear:
            self.lineEdit.clear()
        return self.comboBox

    def updateLineEdit(self, item):
        print('xx')
        if item == self.allItem:
            state = self.allItem.checkState()
            for i in range(1, self.listWidget.count()):
                self.listWidget.item(i).setCheckState(state)

        checkedItems = []
        for i in range(1, self.listWidget.count()):
            if self.listWidget.item(i).checkState() == QtCore.Qt.Checked:
                checkedItems.append(self.listWidget.item(i).text())
        self.lineEdit.setText(", ".join(checkedItems))
