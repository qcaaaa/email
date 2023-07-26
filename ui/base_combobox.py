from PyQt5 import QtWidgets, QtCore


class CheckableComboBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.setWindowTitle('Checkable Combo Box')

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(50, 50, 150, 30))

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(50, 50, 150, 30))
        self.comboBox.setLineEdit(self.lineEdit)

        self.listWidget = QtWidgets.QListWidget(self)

        self.allItem = QtWidgets.QListWidgetItem(self.listWidget)
        self.allItem.setText("全部")
        self.allItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        self.allItem.setCheckState(QtCore.Qt.Unchecked)

        for i in range(10):
            item = QtWidgets.QListWidgetItem(self.listWidget)
            item.setText(f"Item {i}")
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

        self.listWidget.itemClicked.connect(self.updateLineEdit)

        self.comboBox.setModel(self.listWidget.model())
        self.comboBox.setView(self.listWidget)

        self.lineEdit.clear()

    def updateLineEdit(self, item):
        if item == self.allItem:
            state = self.allItem.checkState()
            for i in range(1, self.listWidget.count()):
                self.listWidget.item(i).setCheckState(state)

        checkedItems = []
        for i in range(1, self.listWidget.count()):
            if self.listWidget.item(i).checkState() == QtCore.Qt.Checked:
                checkedItems.append(self.listWidget.item(i).text())
        self.lineEdit.setText(", ".join(checkedItems))
