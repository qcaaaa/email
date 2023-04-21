# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_ui.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 21:47

@Desc :
"""

import os
from loguru import logger
from datetime import datetime
from PyQt5.QtWidgets import QTextEdit, QScrollBar
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidget, QStackedWidget
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView
from PyQt5.Qt import QTableWidgetItem
from constant import FIRST_TAB, FONT_WEIGHT, DIT_LIST, INT_LIMIT, DIT_DATABASE, \
    STATIC_PATH, GIT_URL, EXE_NAME, QSS_STYLE
from tools.email_tool import EmailTools
from tools.email_check import CheckTool
from tools.email_google import GoogleTool
from ota.otaupgrade import OtaUpgrade
from .base_ui import BaseButton
from version import VERSION


class EmailUi(QWidget):
    def __init__(self):
        super(EmailUi, self).__init__()
        self.setWindowIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'logo.png')))
        self.setObjectName('Email-Tool')
        self.resize(1400, 1000)
        self.setMaximumSize(1400, 1000)
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        new_left = (screen.width() - size.width()) / 2
        new_top = (screen.height() - size.height()) / 2
        self.move(int(new_left), int(new_top) if int(new_top) > 60 else 0)
        self.setWindowTitle('Email-Tool')
        self.email_tool = EmailTools(self)
        self.check_tool = CheckTool(self)
        self.google_tool = GoogleTool(self)
        self.ota_tool = OtaUpgrade(self, GIT_URL, VERSION, EXE_NAME)

        # ################# 增加控件 开始.......########################################
        self.add_button = BaseButton(self, (120, 20, 100, 30), os.path.join(STATIC_PATH, 'images', 'add.png'), '增加',
                                     QSS_STYLE, func=self.email_tool.add_table).btu
        # ################# 增加控件 结束.......########################################

        # ################# 导入联系人控件 开始.......########################################
        self.import_button = QPushButton(self)
        self.import_button.setGeometry(QtCore.QRect(240, 20, 100, 30))
        self.import_button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'import.png')))
        self.import_button.setToolTip('导入客户')
        self.import_button.setStyleSheet(QSS_STYLE)
        self.import_button.clicked.connect(self.email_tool.import_user)
        # ################# 导入联系人控件 结束.......########################################

        # ################# 发送邮件控件 开始.......########################################
        self.send_button = QPushButton(self)
        self.send_button.setGeometry(QtCore.QRect(360, 20, 100, 30))
        self.send_button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'email.png')))
        self.send_button.setToolTip('发送邮件')
        self.send_button.setStyleSheet(QSS_STYLE)
        # 最开始禁用
        self.send_button.setDisabled(True)
        self.send_button.clicked.connect(self.email_tool.select_account)
        # ################# 发送邮件控件 结束.......########################################

        # ################# 发送间隔控件 开始.......########################################
        self.sleep_label = QLabel(self)
        self.sleep_label.setGeometry(QtCore.QRect(480, 20, 80, 30))
        self.sleep_label.setText(QtCore.QCoreApplication.translate("Email-Tool", "发送间隔(s)"))
        self.sleep_edit = QLineEdit(self)
        self.sleep_edit.setGeometry(QtCore.QRect(565, 20, 80, 30))
        self.sleep_edit.setStyleSheet(QSS_STYLE)
        # 设置默认值
        self.sleep_edit.setPlaceholderText('20')
        # 设置只能输入数字
        self.sleep_edit.setValidator(QtGui.QIntValidator())
        # ################# 发送间隔控件 结束.......########################################

        # ################# 发送方式控件 开始.......########################################
        self.radio_button = QRadioButton("带网页", self)
        self.radio_button.setChecked(False)
        self.radio_button.setGeometry(665, 20, 60, 30)
        # ################# 发送方式控件 结束.......########################################

        # ################# 发送间隔控件 开始.......########################################
        self.interval_label = QLabel(self)
        self.interval_label.setGeometry(QtCore.QRect(745, 20, 50, 30))
        self.interval_label.setText(QtCore.QCoreApplication.translate("Email-Tool", "最大发送"))
        self.interval_edit = QLineEdit(self)
        self.interval_edit.setGeometry(QtCore.QRect(820, 20, 80, 30))
        self.interval_edit.setStyleSheet(QSS_STYLE)
        # 设置默认值
        self.interval_edit.setPlaceholderText('50')
        # 设置只能输入数字
        self.interval_edit.setValidator(QtGui.QIntValidator())
        # ################# 发送间隔控件 结束.......########################################

        # ################# 谷歌搜索控件 开始.......########################################
        self.google_button = QPushButton(self)
        self.google_button.setGeometry(QtCore.QRect(940, 20, 100, 30))
        self.google_button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'search.png')))
        self.google_button.setToolTip('谷歌搜索')
        self.google_button.setStyleSheet(QSS_STYLE)
        self.google_button.clicked.connect(self.google_tool.google_search)
        # ################# 谷歌搜索控件 结束.......########################################

        # ################# 邮箱账号检查控件 开始.......########################################
        self.check_button = QPushButton(self)
        self.check_button.setGeometry(QtCore.QRect(1060, 20, 100, 30))
        self.check_button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'check.png')))
        self.check_button.setToolTip('邮箱账号检测')
        self.check_button.setStyleSheet(QSS_STYLE)
        self.check_button.clicked.connect(self.check_tool.check_email)
        # ################# 邮箱账号检查控件 结束.......########################################

        # ################# 上传附件控件 开始.......########################################
        self.upload_button = QPushButton(self)
        self.upload_button.setGeometry(QtCore.QRect(1180, 20, 100, 30))
        self.upload_button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'fj.png')))
        self.upload_button.setToolTip('查看附件')
        self.upload_button.setStyleSheet(QSS_STYLE)
        self.upload_button.clicked.connect(self.email_tool.get_aly)
        # ################# 上传附件控件 结束.......########################################

        # ################# 刷新控件 开始.......########################################
        self.flush_button = QPushButton(self)
        self.flush_button.setGeometry(QtCore.QRect(1300, 20, 100, 30))
        self.flush_button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'flush.png')))
        self.flush_button.setToolTip('刷新')
        self.flush_button.setStyleSheet(QSS_STYLE)
        self.flush_button.clicked.connect(self.flush_table)
        # ################# 刷新控件 结束.......########################################

        # ################# 分页 开始....########################################
        self.page_up = QPushButton(self)
        self.page_up.setGeometry(QtCore.QRect(525, 760, 80, 30))
        self.page_up.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'up.png')))
        self.page_up.setToolTip('上一页')
        self.page_up.setObjectName('上一页')
        self.page_up.setDisabled(True)
        self.page_up.setStyleSheet(QSS_STYLE)
        self.page_up.clicked.connect(self.page_turning)

        self.page_text = QLabel(self)
        self.page_text.setGeometry(QtCore.QRect(625, 760, 40, 30))
        self.page_text.setAlignment(Qt.AlignCenter)
        self.page_text.setText(QtCore.QCoreApplication.translate("Email-Tool", "1/1"))

        self.page_down = QPushButton(self)
        self.page_down.setGeometry(QtCore.QRect(685, 760, 80, 30))
        self.page_down.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'next.png')))
        self.page_down.setToolTip('下一页')
        self.page_down.setObjectName('下一页')
        self.page_down.setDisabled(True)
        self.page_down.setStyleSheet(QSS_STYLE)
        self.page_down.clicked.connect(self.page_turning)

        self.page_text_2 = QLineEdit(self)
        self.page_text_2.textChanged.connect(self.text_changed)
        self.page_text_2.setGeometry(QtCore.QRect(785, 760, 70, 30))
        self.page_text_2.setStyleSheet(QSS_STYLE)

        self.page_skip = QPushButton(self)
        self.page_skip.setGeometry(QtCore.QRect(875, 760, 80, 30))
        self.page_skip.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'skip.png')))
        self.page_skip.setToolTip('跳转')
        self.page_skip.setObjectName('跳转')
        self.page_skip.setDisabled(True)
        self.page_skip.setStyleSheet(QSS_STYLE)
        self.page_skip.clicked.connect(self.page_turning)
        # ################# 分页 结束....########################################

        self.main_layout = QHBoxLayout(self)  # 窗口的整体布局
        # 上面留60 下面留250
        self.main_layout.setContentsMargins(0, 60, 0, 250)
        # 左侧选项列表
        self.left_widget = QListWidget()
        self.left_widget.setStyleSheet(QSS_STYLE)
        # 左侧绑定 点击事件
        self.left_widget.itemClicked.connect(self.display)
        self.main_layout.addWidget(self.left_widget)

        # 右侧
        self.right_widget = QStackedWidget()
        self.main_layout.addWidget(self.right_widget)

        # 滚动条
        text_scroll = QScrollBar()
        text_scroll.setStyleSheet(QSS_STYLE)

        # 下侧 日志框
        self.log_label = QLabel(self)
        self.log_label.setGeometry(QtCore.QRect(10, 760, 100, 35))
        self.log_label.setAlignment(Qt.AlignLeft)
        self.pix = QPixmap(os.path.join(STATIC_PATH, 'images', 'log.png'))
        self.log_label.setPixmap(self.pix)
        self.log_label.setToolTip('日志输出')

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # 只读
        self.log_text.setGeometry(QtCore.QRect(10, 800, 1380, 175))
        # 加载滚动条
        self.log_text.setVerticalScrollBar(text_scroll)

        # 版本
        self.ver_label = QLabel(self)
        self.ver_label.setGeometry(QtCore.QRect(10, 975, 270, 20))
        self.upd_btu = QPushButton(self)
        self.upd_btu.setGeometry(QtCore.QRect(280, 975, 80, 20))
        self.upd_btu.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'download.png')))
        self.upd_btu.setStyleSheet("QPushButton { border: none; color: blue;}")
        self.upd_btu.setDisabled(True)
        self.upd_btu.clicked.connect(self.ota_tool.show_page)
        self.ota_tool.set_ver()

        self.page = FIRST_TAB

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
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(FONT_WEIGHT)
        font.setKerning(True)

        for keys, values in DIT_LIST.items():
            self.item = QListWidgetItem(keys, self.left_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(30, 60))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
            int_len = len(values)
            # 渲染表格数据
            table = QTableWidget()
            table.setColumnCount(int_len)
            table.setRowCount(INT_LIMIT)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 铺满
            table.horizontalHeader().setSectionResizeMode(int_len - 1, QHeaderView.Interactive)  # 最后一列可调整
            table.setColumnWidth(0, 100)
            table.setHorizontalHeaderLabels(values)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止修改
            table.setAlternatingRowColors(True)  # 交替行颜色
            # 表格 tip 显示
            table.installEventFilter(self)
            table.setMouseTracking(True)
            table.itemEntered.connect(self.enter_item_slot)
            self.table[keys] = table
            self.right_widget.addWidget(table)
        # 首页自动刷新
        self.flush_table(True)

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
        """翻页操作"""
        sender = self.sender()
        int_pag = 0
        # 获取当前页数
        curr_pag, count_pag = self.page_text.text().split('/')
        if sender.objectName() == '上一页' and curr_pag.isdigit() and count_pag.isdigit():
            int_pag = int(curr_pag) - 1
        elif sender.objectName() == '下一页' and curr_pag.isdigit() and count_pag.isdigit():
            int_pag = int(curr_pag) + 1
        elif sender.objectName() == '跳转' and curr_pag.isdigit() and count_pag.isdigit():
            to_page = self.page_text_2.text()
            if to_page.isdigit() and 1 <= int(to_page) <= int(count_pag):
                int_pag = int(to_page)
                self.page_text_2.setText('')
        if int_pag > 0:
            dit_info = self.email_tool.get_info(DIT_DATABASE[self.page], int_start=int_pag)
            self.show_table(dit_info.get('lst_ret', []), self.page, curr_pag=int_pag, count_pag=dit_info.get('count', 0))
        self.show_message('', '', f'当前处于 {self.page}页面 第{int_pag}页')

    def text_changed(self, text):
        """跳转输入框 监听事件"""
        try:
            int_page = int(text)
            curr_pag, count_pag = self.page_text.text().split('/')
            if int_page == int(curr_pag):
                self.page_skip.setDisabled(True)
            elif 1 <= int_page <= int(count_pag):
                self.page_skip.setEnabled(True)
            else:
                self.page_skip.setDisabled(True)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
            self.page_skip.setDisabled(True)

    def display(self, item):
        """左侧主菜单点击事件"""
        try:
            str_items = str(item.text())
            if self.page != str_items:
                self.page = str_items  # 记住当前在哪个页面
                self.show_message('', '', f'切换到 {str_items}页面')
                # 填充表格
                dit_info = self.email_tool.get_info(DIT_DATABASE[self.page])
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
                        value = self.email_tool.email_dict.get(str(value), {}).get('name_cn')
                    item = QTableWidgetItem(str(value or ''))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    table.setItem(index_, index_j, item)  # 转换后可插入表格
                button = QPushButton()
                # 设置 objname 值为 该行数据库唯一索引
                button.setObjectName(str(dit_info['id']))
                button.setIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'del.png')))
                button.setToolTip('删除')
                button.clicked.connect(self.del_info)
                button.setStyleSheet(QSS_STYLE)
                self.dit_table_button.setdefault(str_table, []).append(button)
                table.setCellWidget(index_, int_len, button)
            # 更新页数
            self.page_text.setText(f'{curr_pag}/{count_pag}')
            if curr_pag > 1:
                self.page_up.setEnabled(True)
            else:
                self.page_up.setDisabled(True)
            if curr_pag < count_pag:
                self.page_down.setEnabled(True)
            else:
                self.page_down.setDisabled(True)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")

    def del_info(self):
        sender = self.sender()
        try:
            sender.setDisabled(True)
            db_id = int(sender.objectName())
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('确认')
            msg_box.setText('确认删除该条记录吗?')
            yes_button = msg_box.addButton('确认', QMessageBox.YesRole)
            no_button = msg_box.addButton('取消', QMessageBox.NoRole)
            msg_box.exec_()
            if msg_box.clickedButton() == yes_button:
                int_ret = self.email_tool.del_info(DIT_DATABASE[self.page], db_id)
                self.show_message('删除', f'删除成功' if int_ret else '删除失败')
                if int_ret == 1:
                    self.flush_table(True)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            sender.setEnabled(True)

    def flush_table(self, is_show: bool = False):
        dit_info = self.email_tool.get_info(DIT_DATABASE[self.page])
        self.show_table(dit_info.get('lst_ret', []), self.page, count_pag=dit_info.get('count', ''))
        if not is_show:
            self.show_message('刷新', '刷新当前页面成功')

    def show_message(self, title: str = '', text: str = '', info: str = ''):
        try:
            if title and text:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle(title)
                msg_box.setText(text)
                msg_box.addButton('确认', QMessageBox.YesRole)
                msg_box.exec_()
            if info:
                self.log_text.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {info}")
                self.log_text.moveCursor(QTextCursor.End)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
