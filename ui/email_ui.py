# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_ui.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 21:47

@Desc :
"""

import threading
from pathlib import Path
from loguru import logger
from datetime import datetime
from PyQt5.QtWidgets import QTextEdit, QToolBar, QWidget, QDialog, QGridLayout, QDialogButtonBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QListWidget
from constant import DIT_LIST, DIT_DATABASE, STATIC_PATH, GIT_URL, EXE_NAME, QSS_STYLE
from utils.tools import str_2_int
from tools.email_tool import EmailTools
from tools.email_check import CheckTool
from tools.email_google import GoogleTool
from ota.otaupgrade import OtaUpgrade
from ui.base_ui import BaseButton, BaseLabel, BaseLineEdit, BaseAction, BaseBar, BaseComboBox
from ui.setting_ui import BaseSetting
from ui.base_table import BaseTab
from ui.base_combobox import BaseComboBox as ComboBox
from version import VERSION


class BaseClass:

    def __init__(self):
        super(BaseClass).__init__()
        self.email_tool = EmailTools(self)
        self.check_tool = CheckTool(self)
        self.google_tool = GoogleTool(self)
        self.setting_tool = BaseSetting(self)
        self.ota_tool = OtaUpgrade(GIT_URL, EXE_NAME)
        self.str_ver = ''


class EmailUi(QMainWindow, BaseClass):
    def __init__(self):
        super(EmailUi, self).__init__()
        self.setWindowIcon(QIcon(Path.joinpath(STATIC_PATH, 'images', 'logo.png').__str__()))
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

        # 工具栏 不可移动
        toolbar = QToolBar()
        toolbar.setFixedHeight(30)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # ################# 状态栏 开始.......########################################
        self.statusBar().showMessage("正在检查版本信息...")
        # ################# 状态栏 结束.......########################################

        # ################# 增加控件 开始.......########################################
        self.add_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'add.png').__str__(), '增加',
                                     func=self.email_tool.add_table).action
        toolbar.addAction(self.add_button)
        # ################# 增加控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 删除控件 开始.......########################################
        self.del_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'del.png').__str__(), str_tip='删除',
                                     func=self.del_info, file_style=QSS_STYLE).action
        self.del_button.setDisabled(True)
        toolbar.addAction(self.del_button)
        # ################# 删除控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 发送邮件控件 开始.......########################################
        self.send_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'email.png').__str__(), '发送邮件',
                                      func=self.email_tool.select_user).action
        toolbar.addAction(self.send_button)
        # ################# 发送邮件控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 谷歌搜索控件 开始.......########################################
        self.google_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'search.png').__str__(), '谷歌搜索',
                                        func=self.google_tool.google_search).action
        toolbar.addAction(self.google_button)
        # ################# 谷歌搜索控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 邮箱账号检查控件 开始.......########################################
        self.check_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'check.png').__str__(), '邮箱账号检测',
                                       func=self.check_tool.check_email).action
        toolbar.addAction(self.check_button)
        # ################# 邮箱账号检查控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 上传附件控件 开始.......########################################
        self.upload_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'fj.png').__str__(), '查看附件',
                                        func=self.email_tool.get_aly).action
        toolbar.addAction(self.upload_button)
        # ################# 上传附件控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 刷新控件 开始.......########################################
        self.flush_button = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'flush.png').__str__(), '刷新',
                                       func=self.flush_table).action
        toolbar.addAction(self.flush_button)
        # ################# 刷新控件 结束.......########################################

        toolbar.addSeparator()  # 分隔符

        # ################# 检查更新控件 开始.......########################################
        self.ver_btu = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'ver.png').__str__(), '检查更新',
                                  func=self.check_ver).action
        toolbar.addAction(self.ver_btu)
        # ################# 检查更新控件 结束.......########################################

        # ################# 设置更新控件 开始.......########################################
        self.set_btu = BaseAction(self, Path.joinpath(STATIC_PATH, 'images', 'setting.png').__str__(), '设置',
                                  func=self.setting_tool.load_frame).action
        toolbar.addAction(self.set_btu)
        # ################# 设置更新控件 结束.......########################################

        # ################# 状态栏 结束.......########################################

        # 左侧选项列表
        self.left_widget = QListWidget()
        self.left_widget.setStyleSheet(QSS_STYLE)
        # 左侧绑定 点击事件
        self.left_widget.itemClicked.connect(self.display)

        # 右侧
        self.table = QTableWidget()  # type: QTableWidget

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ################# 分页 开始....########################################
        self.page_up = BaseButton(central_widget, (525, 720, 80, 30), Path.joinpath(STATIC_PATH, 'images', 'up.png').__str__(),
                                  '上一页', QSS_STYLE, func=self.page_turning, str_name='上一页').btu

        self.page_text = BaseLabel(central_widget, (625, 720, 40, 30), str_text="1/1").label
        self.page_text.setAlignment(Qt.AlignCenter)

        self.page_down = BaseButton(central_widget, (685, 720, 80, 30), Path.joinpath(STATIC_PATH, 'images', 'next.png').__str__(),
                                    '下一页', QSS_STYLE, func=self.page_turning, str_name='下一页').btu

        self.page_text_2 = BaseLineEdit(central_widget, (785, 720, 70, 30), QSS_STYLE).lineedit
        self.page_text_2.textChanged.connect(self.text_changed)

        self.page_skip = BaseButton(central_widget, (875, 720, 80, 30), Path.joinpath(STATIC_PATH, 'images', 'skip.png').__str__(),
                                    '跳转', QSS_STYLE, func=self.page_turning, str_name='跳转').btu
        self.page_skip.setDisabled(True)

        self.page_num = BaseComboBox(central_widget, QSS_STYLE, lst_data=['20', '30', '50'], is_readonly=False,
                                     tuple_size=(975, 720, 80, 30), func=self.on_combo_box_changed).box
        validator = QIntValidator()
        validator.setRange(1, 300)
        self.page_num.setValidator(validator)
        # ################# 分页 结束....########################################

        # 窗口的整体布局
        main_layout = QHBoxLayout(central_widget)
        # # 下面留250
        main_layout.setContentsMargins(0, 0, 0, 250)
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.table)

        # 下侧 日志框
        self.log_label = BaseLabel(self, (10, 760, 100, 35), str_img=Path.joinpath(STATIC_PATH, 'images', 'log.png').__str__(),
                                   str_tip='日志输出').label
        self.log_label.setAlignment(Qt.AlignLeft)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # 只读
        self.log_text.setGeometry(QtCore.QRect(10, 800, 1380, 175))
        # 加载滚动条
        self.log_text.setVerticalScrollBar(BaseBar(QSS_STYLE).bar)

        self.page = ''  # 页面

        self.tool_tip = ''

        self.select_table = set()  # 当前页面选中的单选框数据库唯一标识

        self._setup_ui()

        self.show()

    def _setup_ui(self):
        """加载界面ui"""

        # 获取版本
        self.set_ver()

        self.left_widget.setFrameShape(QListWidget.NoFrame)  # 去掉边框
        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for index_, keys in enumerate(DIT_LIST.keys()):
            if index_ == 0:
                self.page = keys
            item = QListWidgetItem(keys, self.left_widget)  # 左侧选项的添加
            item.setSizeHint(QSize(30, 60))
            item.setTextAlignment(Qt.AlignCenter)  # 居中显示
            # 菜单改了 图片名称也得改
            item.setIcon(QIcon(Path(STATIC_PATH, 'images', f'{keys}.png').__str__()))
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
            dit_info = self.email_tool.get_info(DIT_DATABASE[self.page], int_start=int_pag)
            self.show_table(dit_info.get('lst_ret', []), self.page, curr_pag=int_pag,
                            count_pag=dit_info.get('count', 0))

    def text_changed(self, text):
        """跳转输入框 监听事件"""
        try:
            int_page = str_2_int(text)
            if int_page > 0:
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
                # 每次切换页面 断开之前的 表头点击事件
                self.table.horizontalHeader().sectionClicked.disconnect()
                # 填充表格
                dit_info = self.email_tool.get_info(DIT_DATABASE[self.page])
                self.show_table(dit_info.get('lst_ret', []), str_items, count_pag=dit_info.get('count', ''))
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def show_table(self, lst_data: list, str_table: str, curr_pag: int = 1, count_pag: int = 1):
        """表格填充数据"""
        try:
            obj_table = BaseTab(self.table, str_table, parent=self)
            # 邮箱类型
            if str_table == '账号配置':
                dit_email = {dit_e['index']: dit_e['name_cn'] for dit_e in self.email_tool.email_list}
                for dit_user in lst_data:
                    dit_user['str_type'] = dit_email.get(dit_user['str_type'], '未知')

            obj_table.show_table(lst_data)

            # tip 显示
            self.table.installEventFilter(self)
            self.table.setMouseTracking(True)
            self.table.itemEntered.connect(self.enter_item_slot)

            # 双击事件
            self.table.itemDoubleClicked.connect(self.update_table)

            # 获取一下单选框
            self.select_table = obj_table.select_table
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

    def on_all_checkbox_changed(self, logical_index):
        """表格全选
        :param logical_index: 列索引
        :return:
        """
        is_clear = False
        lst_radio = []
        try:
            if logical_index == 0:
                lst_radio = [self.table.cellWidget(i, 0) for i in range(self.table.rowCount())]
                # 已经全选
                if 0 < len(lst_radio) == len(self.select_table):
                    is_clear = True
                for obj_radio in lst_radio:
                    obj_radio.setChecked(not is_clear)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            if logical_index == 0:
                if is_clear:
                    self.select_table.clear()
                else:
                    self.select_table = {str_2_int(obj_radio.objectName()) for obj_radio in lst_radio}
                if self.select_table:
                    self.del_button.setEnabled(True)
                else:
                    self.del_button.setDisabled(True)
        return

    def on_checkbox_changed(self, state):
        """表格内容单选"""
        try:
            int_id = str_2_int(self.sender().objectName())
            if int_id >= 0 and state:
                self.select_table.add(int_id)
            elif int_id >= 0 and not state:
                self.select_table.remove(int_id)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            if self.select_table:
                self.del_button.setEnabled(True)
            else:
                self.del_button.setDisabled(True)
        return

    def on_combo_box_changed(self, page_num):
        try:
            curr_row = str_2_int(self.table.rowCount())
            page_num = str_2_int(page_num)
            if curr_row > 0 and page_num > 0:
                self.flush_table(True)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return

    def del_info(self):
        int_succ = 0
        int_len = len(self.select_table)
        try:
            if int_len:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('确认')
                msg_box.setText(f'确认删除{len(self.select_table)}条记录吗?')
                yes_button = msg_box.addButton('确认', QMessageBox.YesRole)
                no_button = msg_box.addButton('取消', QMessageBox.NoRole)
                msg_box.exec_()
                if msg_box.clickedButton() == yes_button:
                    for int_id in self.select_table:
                        int_ret = self.email_tool.del_info(DIT_DATABASE[self.page], int_id)
                        if int_ret == 1:
                            int_succ += 1
                    if int_succ == int_len:
                        self.show_message('删除', f'{int_succ}条记录被删除')
                    elif 0 < int_succ < int_len:
                        self.show_message('删除', f'{int_succ}条记录删除成功,{int_len - int_succ}条记录删除失败')
                    else:
                        self.show_message('删除', f'删除失败')
            else:
                self.show_message('删除', '未选择数据')
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--:{e}")
        else:
            self.flush_table(True)
        finally:
            self.del_button.setDisabled(True)

    def flush_table(self, is_show: bool = False):
        dit_info = self.email_tool.get_info(DIT_DATABASE[self.page])
        self.show_table(dit_info.get('lst_ret', []), self.page, count_pag=dit_info.get('count', ''))
        if not is_show:
            self.show_message('刷新', '刷新当前页面成功')

    def update_table(self, item=None):
        try:
            int_column = str_2_int(item.column(), -1)
            int_row = str_2_int(item.row(), -1)
            # 真实表头多了个 全选
            en_table_header = DIT_LIST[self.page].get('en', [])
            if int_column != -1 and int_row != -1 and en_table_header[int_column - 1] == 'language':
                dialog = QDialog(self)  # 自定义一个dialog
                dialog.setWindowTitle('修改产品信息')
                dialog.resize(300, 100)
                grid = QGridLayout()
                lang_label = BaseLabel(dialog, str_text='产品').label
                grid.addWidget(lang_label, 1, 0)
                lang_box = ComboBox(dialog, lst_data=self.email_tool.get_language(), file_style=QSS_STYLE).box
                grid.addWidget(lang_box, 1, 2, 1, 2)

                button = QDialogButtonBox(QDialogButtonBox.Ok)
                button.clicked.connect(dialog.accept)
                grid.addWidget(button, 2, 3)

                dialog.setLayout(grid)
                dialog.show()
                if dialog.exec() == QDialog.Accepted:
                    curr_text = lang_box.currentText().strip()
                    if curr_text:
                        int_id = str_2_int(self.table.item(int_row, 1).text(), -1)
                        int_ret = self.email_tool.upd_info(DIT_DATABASE[self.page], int_id, curr_text)
                        if int_ret == 1:
                            self.flush_table(True)
                            self.show_message('成功', '修改成功')
                        else:
                            self.show_message('失败', '修改失败')
                    else:
                        self.show_message('错误', '不可为空')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return

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
            self.str_ver = self.ota_tool.get_ver()
            str_title = f'软件当前版本: {VERSION} 最新版本: {self.str_ver}'
            # 版本
            self.statusBar().showMessage(str_title)

        try:

            threading.Thread(target=__do).start()
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return

    def check_ver(self):
        is_update = False
        try:
            if VERSION.count('.') == self.str_ver.count('.') == 3:
                lst_new_ver = [int(i) for i in self.str_ver.lower().replace('v', '').split('.')]
                lst_old_ver = [int(i) for i in VERSION.lower().replace('v', '').split('.')]

                for index_ in range(4):
                    if lst_new_ver[index_] > lst_old_ver[index_]:
                        is_update = True
                        break
        except Exception as err_msg:
            logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
        finally:
            if not is_update:
                self.show_message('升级', '已是最新版本！')
            else:
                self.ota_tool.show_page()
        return
