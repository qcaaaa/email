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
from constant import FONT_SIZE, FIRST_TAB, FONT_WEIGHT, DIT_LIST, INT_LIMIT, DIT_DATABASE
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

        self.page = ''

        self.tool_tip = ''

        self.table = {}

        self.dit_table_button = {}

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
            # 渲染表格数据
            table = QTableWidget()
            table.setColumnCount(len(values))
            table.setRowCount(INT_LIMIT)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 铺满
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)  # 第一列可调整
            table.setColumnWidth(0, 40)
            table.setHorizontalHeaderLabels(values)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止修改
            table.setAlternatingRowColors(True)  # 交替行颜色
            # 表格 tip 显示
            table.installEventFilter(self)
            table.setMouseTracking(True)
            table.itemEntered.connect(self.enter_item_slot)
            self.table[keys] = table
            self.right_widget.addWidget(table)

    def enter_item_slot(self, item):
        # 获取鼠标指向
        self.tool_tip = item.text()

    def eventFilter(self, object, event):
        try:
            if event.type() == QEvent.ToolTip and self.tool_tip is not None:
                self.setToolTip(self.tool_tip)
            return QWidget.eventFilter(self, object, event)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

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
                # 填充表格
                dit_info = self.obj_tool.get_info(DIT_DATABASE[self.page])
                self.show_table(dit_info.get('lst_ret', []), str_items, count_pag=dit_info.get('count', ''))
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def show_table(self, lst_data: list, str_table: str, curr_pag: int = 1, count_pag: int = 1):
        """表格填充数据"""
        try:
            # 清空表格数据
            table = self.table[str_table]
            table.clearContents()  # 清空现有数据
            self.dit_table_button[str_table] = []  # 清空页面 按钮对象
            for index_, dit_info in enumerate(lst_data):
                int_len = len(dit_info)
                # 设置数据
                for index_j, value in enumerate(dit_info.values()):
                    if str_table == FIRST_TAB and index_j == 3:
                        value = self.obj_tool.email_dict.get(str(value), {}).get('name_cn')
                    item = QTableWidgetItem(str(value or ''))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    table.setItem(index_, index_j, item)  # 转换后可插入表格
                button = QPushButton()
                # 设置 objname 值为 该行数据库唯一索引
                button.setObjectName(str(dit_info['id']))
                button.setText(QtCore.QCoreApplication.translate("Telegram-Tool", '删除'))
                button.clicked.connect(self.del_info)
                self.dit_table_button.setdefault(str_table, []).append(button)
                table.setCellWidget(index_, int_len + 1, button)
            # 更新页数
            self.page_text.setText(f'{curr_pag}/{count_pag}')
            self.page_up.setDisabled(not curr_pag > 1)
            self.page_down.setDisabled(not curr_pag < count_pag)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")

    def del_info(self):
        pass