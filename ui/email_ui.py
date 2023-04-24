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
import threading
from loguru import logger
from sql.sql_db import MySql
from datetime import datetime
from PyQt5.QtWidgets import QTextEdit, QScrollBar
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QListWidget, QStackedWidget
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView
from PyQt5.Qt import QTableWidgetItem
from constant import FIRST_TAB, FONT_WEIGHT, DIT_LIST, INT_LIMIT, DIT_DATABASE, \
    STATIC_PATH, GIT_URL, EXE_NAME, QSS_STYLE
from tools.email_tool import EmailTools
from tools.email_check import CheckTool
from tools.email_google import GoogleTool
from ota.otaupgrade import OtaUpgrade
from ui.base_ui import BaseButton, BaseLabel, BaseLineEdit
from version import VERSION


class BaseClass(MySql):

    def __init__(self):
        super(BaseClass).__init__()
        self.email_tool = EmailTools(self)
        self.check_tool = CheckTool(self)
        self.google_tool = GoogleTool(self)
        self.ota_tool = OtaUpgrade(GIT_URL, EXE_NAME)
        

class EmailUi(QWidget, BaseClass):
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

        # ################# 增加控件 开始.......########################################
        self.add_button = BaseButton(self, (120, 20, 40, 30), os.path.join(STATIC_PATH, 'images', 'add.png'), '增加',
                                     QSS_STYLE, func=self.email_tool.add_table).btu
        # ################# 增加控件 结束.......########################################

        # ################# 发送邮件控件 开始.......########################################
        self.send_button = BaseButton(self, (170, 20, 40, 30), os.path.join(STATIC_PATH, 'images', 'email.png'),
                                      '发送邮件', QSS_STYLE, func=self.email_tool.select_user).btu
        # ################# 发送邮件控件 结束.......########################################

        # ################# 谷歌搜索控件 开始.......########################################
        self.google_button = BaseButton(self, (220, 20, 40, 30), os.path.join(STATIC_PATH, 'images', 'search.png'),
                                        '谷歌搜索', QSS_STYLE, func=self.google_tool.google_search).btu
        # ################# 谷歌搜索控件 结束.......########################################

        # ################# 邮箱账号检查控件 开始.......########################################
        self.check_button = BaseButton(self, (270, 20, 40, 30), os.path.join(STATIC_PATH, 'images', 'check.png'),
                                       '邮箱账号检测', QSS_STYLE, func=self.check_tool.check_email).btu
        # ################# 邮箱账号检查控件 结束.......########################################

        # ################# 上传附件控件 开始.......########################################
        self.upload_button = BaseButton(self, (320, 20, 40, 30), os.path.join(STATIC_PATH, 'images', 'fj.png'),
                                        '查看附件', QSS_STYLE, func=self.email_tool.get_aly).btu
        # ################# 上传附件控件 结束.......########################################

        # ################# 刷新控件 开始.......########################################
        self.flush_button = BaseButton(self, (370, 20, 40, 30), os.path.join(STATIC_PATH, 'images', 'flush.png'),
                                       '刷新', QSS_STYLE, func=self.flush_table).btu
        # ################# 刷新控件 结束.......########################################

        # ################# 分页 开始....########################################
        self.page_up = BaseButton(self, (525, 760, 80, 30), os.path.join(STATIC_PATH, 'images', 'up.png'),
                                  '上一页', QSS_STYLE, func=self.page_turning, str_name='上一页').btu
        self.page_up.setDisabled(True)

        self.page_text = BaseLabel(self, (625, 760, 40, 30), str_text="1/1").label
        self.page_text.setAlignment(Qt.AlignCenter)

        self.page_down = BaseButton(self, (685, 760, 80, 30), os.path.join(STATIC_PATH, 'images', 'next.png'),
                                    '下一页', QSS_STYLE, func=self.page_turning, str_name='下一页').btu
        self.page_down.setDisabled(True)

        self.page_text_2 = BaseLineEdit(self, (785, 760, 70, 30), QSS_STYLE).lineedit
        self.page_text_2.textChanged.connect(self.text_changed)

        self.page_skip = BaseButton(self, (875, 760, 80, 30), os.path.join(STATIC_PATH, 'images', 'skip.png'),
                                    '跳转', QSS_STYLE, func=self.page_turning, str_name='跳转').btu
        self.page_skip.setDisabled(True)
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
        self.log_label = BaseLabel(self, (10, 760, 100, 35), str_img=os.path.join(STATIC_PATH, 'images', 'log.png'),
                                   str_tip='日志输出').label
        self.log_label.setAlignment(Qt.AlignLeft)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # 只读
        self.log_text.setGeometry(QtCore.QRect(10, 800, 1380, 175))
        # 加载滚动条
        self.log_text.setVerticalScrollBar(text_scroll)

        # 版本
        self.ver_label = BaseLabel(self, (10, 975, 270, 20)).label

        self.upd_btu = BaseButton(self, (280, 975, 80, 20), os.path.join(STATIC_PATH, 'images', 'download.png'),
                                  file_style=QSS_STYLE, str_name='upd_btu', func=self.ota_tool.show_page).btu
        self.upd_btu.setDisabled(True)

        self.page = FIRST_TAB

        self.tool_tip = ''

        self.table = None  # type: QTableWidget

        self.dit_table_button = {}

        self._setup_ui()

    def _setup_ui(self):
        """加载界面ui"""

        # 获取版本
        self.set_ver()

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

        for keys in DIT_LIST.keys():
            self.item = QListWidgetItem(keys, self.left_widget)  # 左侧选项的添加
            self.item.setSizeHint(QSize(30, 60))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
        # 首页自动刷新
        self.flush_table(True)

    def enter_item_slot(self, item):
        # 获取鼠标指向
        self.tool_tip = item.text()

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.ToolTip and self.tool_tip is not None:
                self.setToolTip(self.tool_tip)
            return QWidget.eventFilter(self, obj, event)
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
            dit_info = self.select_sql(DIT_DATABASE[self.page], int_start=int_pag)
            self.show_table(dit_info.get('lst_ret', []), self.page, curr_pag=int_pag, count_pag=dit_info.get('count', 0))

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
                # 填充表格
                dit_info = self.select_sql(DIT_DATABASE[self.page])
                self.show_table(dit_info.get('lst_ret', []), str_items, count_pag=dit_info.get('count', ''))
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def show_table(self, lst_data: list, str_table: str, curr_pag: int = 1, count_pag: int = 1):
        """表格填充数据"""
        try:
            self.dit_table_button.clear()  # 清空页面 按钮对象
            # 清空表格数据
            if self.table:
                self.table.clearContents()  # 清空现有数据
            else:
                self.table = QTableWidget()
                self.right_widget.addWidget(self.table)
            int_len = len(DIT_LIST[str_table])
            # 渲染表格数据
            self.table.setColumnCount(int_len)
            self.table.setRowCount(INT_LIMIT)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 铺满
            self.table.horizontalHeader().setSectionResizeMode(int_len - 1, QHeaderView.Interactive)  # 最后一列可调整
            self.table.setColumnWidth(0, 100)
            self.table.setHorizontalHeaderLabels(DIT_LIST[str_table])
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止修改
            self.table.setAlternatingRowColors(True)  # 交替行颜色
            # 表格 tip 显示
            self.table.installEventFilter(self)
            self.table.setMouseTracking(True)
            self.table.itemEntered.connect(self.enter_item_slot)
            for index_, dit_info in enumerate(lst_data):
                int_len = len(dit_info)
                # 设置数据
                for index_j, value in enumerate(dit_info.values()):
                    if str_table == FIRST_TAB and index_j == 3:
                        value = self.email_tool.email_dict.get(str(value), {}).get('name_cn')
                    item = QTableWidgetItem(str(value or ''))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table.setItem(index_, index_j, item)  # 转换后可插入表格
                # 设置 objname 值为 该行数据库唯一索引
                button = BaseButton(None, str_img=os.path.join(STATIC_PATH, 'images', 'del.png'), str_tip='删除',
                                    str_name=str(dit_info['id']), func=self.del_info, file_style=QSS_STYLE).btu
                self.dit_table_button.setdefault(str_table, []).append(button)
                self.table.setCellWidget(index_, int_len, button)
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
                int_ret = self.del_sql(DIT_DATABASE[self.page], db_id)
                self.show_message('删除', f'删除成功' if int_ret else '删除失败')
                if int_ret == 1:
                    self.flush_table(True)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            sender.setEnabled(True)

    def flush_table(self, is_show: bool = False):
        dit_info = self.select_sql(DIT_DATABASE[self.page])
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

    def set_ver(self):

        def __do():
            str_ver = self.ota_tool.get_ver()
            str_title = f'软件当前版本: {VERSION} 最新版本: {str_ver}'
            self.ver_label.setText(str_title)
            if VERSION.count('.') == str_ver.count('.') == 3:
                lst_new_ver = [int(i) for i in str_ver.lower().replace('v', '').split('.')]
                lst_old_ver = [int(i) for i in VERSION.lower().replace('v', '').split('.')]

                for index_ in range(4):
                    if lst_new_ver[index_] > lst_old_ver[index_]:
                        self.upd_btu.setText('立即查看')
                        self.upd_btu.setEnabled(True)
                        break
        try:

            threading.Thread(target=__do).start()
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return
