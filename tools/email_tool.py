# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_tool.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 22:11

@Desc :
"""

import os
import time
import smtplib
import threading
from PyQt5 import QtGui
from tools.aly_s3 import AlyS3
from sql.sql_db import MySql
from loguru import logger
from random import choice
from functools import partial
from itertools import product
from email.header import Header
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.tools import sub_html, word_2_html, load_file, str_2_int
from constant import DIT_DATABASE, FILTER_TABLE, FILTER_LANG, QSS_STYLE, STATIC_PATH, MAST_SELECT_TABLE, \
    DEAR_FONT
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox, \
    QTextEdit, QFileDialog, QCheckBox, QGridLayout, QRadioButton
from ui.base_ui import BaseButton, BaseLabel, BaseLineEdit, BaseBar, BaseComboBox


class EmailTools:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui
        self.email_list = load_file()
        self.to_list = []
        self.str_page = ''  # 当前在那个选择页
        self.dit_v = {
            'user': {'key': 'name', 'len': 5, 'lst': [], 'cn': '账号'},
            'body': {'key': 'str_body', 'len': 1, 'lst': [], 'cn': '内容'},
            'title': {'key': 'str_title', 'len': 3, 'lst': [], 'cn': '标题'},
            'info': {'key': 'url', 'len': 2, 'lst': [], 'cn': '附件'},
            'end': {'key': 'name', 'len': 5, 'lst': [], 'cn': '结尾'},
            'info_lang': {'key': 'language', 'len': 1, 'lst': [], 'cn': '附件语种'},
            'body_lang': {'key': 'language', 'len': 1, 'lst': [], 'cn': '正文语种'},
            'title_lang': {'key': 'language', 'len': 1, 'lst': [], 'cn': '标题语种'},
        }
        self.dialog = None  # 下一步之前的页面 用于下一步后 关闭上一个页面
        self.button = None  # 每个页面的下一步按钮
        self.send_mun = 50  # 一个账号一次发50封
        self.sleep_mun = 20  # 发送间隔
        self.send_model = False  # 发送模式(不带网页)
        self.dear_font = DEAR_FONT[0]  # Dear 行字体
        self.lang = None

    def __login(self, str_user: str, str_pwd: str, str_type: str):
        try:
            dit_config = load_file()
            str_server, int_port = dit_config[str_type]['server'], dit_config[str_type]['port']
            obj_smtp = smtplib.SMTP(str_server, port=int_port, local_hostname='localhost')
            obj_smtp.login(str_user, str_pwd)
        except Exception as err:
            self.obj_ui.show_message('', '', f"{err.__traceback__.tb_lineno}: {err}")
            obj_smtp = None
        return obj_smtp

    def get_info(self, table: str, where: str = '', int_start: int = 1, int_limit: int = None):
        """获取数据库信息"""
        int_limit = int_limit or int(self.obj_ui.page_num.currentText())
        with MySql() as obj_sql:
            dit_info = obj_sql.select_sql(table, int_start=int_start, int_limit=int_limit)
        return dit_info

    @staticmethod
    def del_info(table: str, int_id: int) -> int:
        """删除数据库信息"""
        with MySql() as obj_sql:
            int_ret = obj_sql.del_sql(table, int_id)
        return int_ret

    @staticmethod
    def add_info(table: str, lst_data: list):
        """增加数据库信息"""
        with MySql() as obj_sql:
            int_ret = obj_sql.add_sql(table, lst_data)
        return int_ret

    @staticmethod
    def __get_language(str_type: str):
        with MySql() as obj_sql:
            lst_info = obj_sql.get_language(str_type)
        return lst_info

    def __add_user(self):
        dialog = QDialog(self.obj_ui)  # 自定义一个dialog
        dialog.setWindowTitle('增加邮箱账号')
        dialog.resize(300, 100)
        grid = QGridLayout()
        grid.setSpacing(10)

        user_label = BaseLabel(dialog, str_text='邮箱账号').label
        grid.addWidget(user_label, 1, 0)
        user_input = BaseLineEdit(dialog, file_style=QSS_STYLE).lineedit
        grid.addWidget(user_input, 1, 1, 1, 2)

        pwd_label = BaseLabel(dialog, str_text='邮箱密码').label
        grid.addWidget(pwd_label, 2, 0)
        pwd_input = BaseLineEdit(dialog, file_style=QSS_STYLE).lineedit
        grid.addWidget(pwd_input, 2, 1, 1, 2)

        serve_label = BaseLabel(dialog, str_text='邮箱服务器').label
        grid.addWidget(serve_label, 3, 0)
        serve_box = BaseComboBox(dialog, file_style=QSS_STYLE, lst_data=[dit_c['name_cn'] for dit_c in self.email_list]).box
        grid.addWidget(serve_box, 3, 1, 1, 2)

        lang_label = BaseLabel(dialog, str_text='邮箱语种').label
        grid.addWidget(lang_label, 4, 0)
        lang_input = BaseLineEdit(dialog, file_style=QSS_STYLE).lineedit
        grid.addWidget(lang_input, 4, 1, 1, 2)

        button = QDialogButtonBox(QDialogButtonBox.Ok)
        button.clicked.connect(dialog.accept)
        grid.addWidget(button, 5, 3)

        dialog.setLayout(grid)
        dialog.show()
        if dialog.exec() == QDialog.Accepted:
            lst_e = [dit_e for dit_e in self.email_list if dit_e['name_cn'] == serve_box.currentText().strip()]
            str_1, str_2, str_3 = user_input.text().strip(), pwd_input.text().strip(), lang_input.text().strip()
            if all([str_1, str_2, lst_e, str_3]):
                return self.add_info(DIT_DATABASE[self.obj_ui.page], [str_1, str_2, int(lst_e[0]['index']), str_3])
            return -1

    def __add_title(self):
        """批量增加邮件标题"""
        int_ret = 0
        try:

            def __import_file():
                try:
                    text_title.clear()
                    str_file, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取邮件标题文件', os.getcwd(), 'Text File(*.txt)')
                    if os.path.isfile(str_file):
                        with open(str_file, 'r', encoding='utf-8') as f:
                            str_data = f.read()
                            if str_data:
                                text_title.append(str_data)
                    else:
                        self.obj_ui.show_message('错误', '未选择文件')
                except Exception as e:
                    logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

            def __body_change():
                if text_title.toPlainText():
                    button.setEnabled(True)
                else:
                    button.setDisabled(True)

            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle('增加邮件标题')
            dialog.resize(500, 300)

            grid = QGridLayout()
            grid.setSpacing(10)

            title_label = BaseLabel(dialog, str_text='标题文件').label
            grid.addWidget(title_label, 1, 0)

            title_btu = BaseButton(dialog, str_text='选择文件', func=__import_file).btu
            grid.addWidget(title_btu, 1, 1)

            title_lst_label = BaseLabel(dialog, str_text='标题列表').label
            grid.addWidget(title_lst_label, 2, 0)

            text_title = QTextEdit(dialog)
            text_title.textChanged.connect(__body_change)
            text_title.setVerticalScrollBar(BaseBar(QSS_STYLE).bar)
            grid.addWidget(text_title, 2, 1, 5, 3)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.clicked.connect(dialog.accept)
            button.setDisabled(True)
            grid.addWidget(button, 7, 3)

            dialog.setLayout(grid)

            dialog.show()
            if dialog.exec() == QDialog.Accepted:
                for str_t in text_title.toPlainText().split('\n'):
                    if str_t.strip() and ' ' in str_t:
                        self.add_info(DIT_DATABASE[self.obj_ui.page], [i.strip() for i in str_t.rsplit(maxsplit=1)])
                int_ret = 1
            else:
                int_ret = -2
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        return int_ret

    def __add_body(self):
        """添加邮件正文"""
        int_ret = 0
        try:

            def __import_file():
                try:
                    body_title.clear()
                    # doc文件名包含中文处理
                    options = QFileDialog.Options()
                    options |= QFileDialog.DontUseNativeDialog
                    str_file, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取邮件正文文件', os.getcwd(), 'Text File(*.docx)', options=options)
                    if os.path.isfile(str_file):
                        result = word_2_html(str_file)
                        if result:
                            body_title.setHtml(result)
                        else:
                            self.obj_ui.show_message('错误', 'Word未获取到内容')
                    else:
                        self.obj_ui.show_message('错误', '未选择文件')
                except Exception as e:
                    logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

            def __body_change():
                if body_title.toHtml():
                    button.setEnabled(True)
                else:
                    button.setDisabled(True)

            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle('增加邮件正文')
            dialog.resize(500, 300)

            grid = QGridLayout()
            grid.setSpacing(10)

            body_label = BaseLabel(dialog, str_text='正文文件').label
            grid.addWidget(body_label, 1, 0)

            body_btu = BaseButton(dialog, str_text='选择文件', func=__import_file).btu
            grid.addWidget(body_btu, 1, 1)

            body_lst_label = BaseLabel(dialog, str_text='正文内容').label
            grid.addWidget(body_lst_label, 2, 0)

            body_title = QTextEdit(dialog)
            body_title.setVerticalScrollBar(BaseBar(QSS_STYLE).bar)
            body_title.textChanged.connect(__body_change)
            grid.addWidget(body_title, 2, 1, 6, 5)

            box_label = BaseLabel(dialog, str_text='模板语种').label
            grid.addWidget(box_label, 8, 0)

            str_box = BaseComboBox(dialog, QSS_STYLE, False, self.__get_language('body')).box
            grid.addWidget(str_box, 8, 1)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.clicked.connect(dialog.accept)
            grid.addWidget(button, 9, 5)
            button.setDisabled(True)

            dialog.setLayout(grid)
            dialog.show()
            if dialog.exec() == QDialog.Accepted:
                str_2, str_3 = sub_html(body_title.toHtml()), str_box.currentText().strip()
                if all([str_2, str_3]):
                    int_ret = self.add_info(DIT_DATABASE[self.obj_ui.page], [str_2, str_3])
                else:
                    int_ret = -1
            else:
                int_ret = -2
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        return int_ret

    def __add_info(self):
        """增加邮件附件"""
        int_ret = 0
        try:

            def __upload_aly():
                """上传文件至阿里云"""
                title = 'Text File(*.pdf);;JPG File(*.jpg);;PNG File(*.png)'
                str_file, _ = QFileDialog.getOpenFileName(self.obj_ui, '选择本地附件上传', os.getcwd(), title)
                if os.path.isfile(str_file):
                    dit_config = load_file('config.json')
                    obj_s3 = AlyS3(dit_config['AccessKey_ID'], dit_config['AccessKey_Secret'], dit_config['bucket'],
                                   dit_config['url'])
                    self.obj_ui.show_message('', '', 'Aly OSS 连接成功')
                    if obj_s3:
                        try:
                            if obj_s3.push_file(str_file) == 1:
                                str_url = f"https://{dit_config['bucket']}.{dit_config['url'][8:]}/{os.path.split(str_file)[-1]}"
                                self.obj_ui.show_message('', '', f'附件{str_file} 上传成功, 保存地址: {str_url}')
                                if file_path and str_url:
                                    file_path.setText(str_url)
                        except Exception as e:
                            self.obj_ui.show_message('', '', f"{e.__traceback__.tb_lineno}:{e}")
                    else:
                        self.obj_ui.show_message('错误提示', '上阿里云OSS连接失败,请检查配置', '上阿里云OSS连接失败,请检查配置')
                else:
                    self.obj_ui.show_message('错误', '未选择文件')

            dialog = QDialog(self.obj_ui)  # 自定义一个dialog
            dialog.setWindowTitle('增加邮件附件')
            dialog.resize(600, 100)

            grid = QGridLayout()
            grid.setSpacing(10)

            push_label = BaseLabel(dialog, str_text="本地上传").label
            grid.addWidget(push_label, 1, 0)

            push_button = BaseButton(dialog, str_text='选择本地文件', func=__upload_aly).btu
            grid.addWidget(push_button, 1, 1)

            file_label = BaseLabel(dialog, str_text='现有附件S3地址').label
            grid.addWidget(file_label, 2, 0)

            file_path = BaseLineEdit(dialog, file_style=QSS_STYLE).lineedit
            grid.addWidget(file_path, 2, 1, 1, 3)

            box_label = BaseLabel(dialog, str_text='附件语种').label
            grid.addWidget(box_label, 3, 0)

            str_box = BaseComboBox(dialog, QSS_STYLE, False, self.__get_language('info')).box
            grid.addWidget(str_box, 3, 1)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.clicked.connect(dialog.accept)
            grid.addWidget(button, 4, 3)

            dialog.setLayout(grid)
            dialog.show()
            if dialog.exec() == QDialog.Accepted:
                str_1, str_2 = file_path.text().strip(), str_box.currentText().strip()
                if all([str_1, str_2]):
                    int_ret = self.add_info(DIT_DATABASE[self.obj_ui.page], [str_1, str_2])
                else:
                    int_ret = -1
            else:
                int_ret = -2
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        return int_ret

    def __add_end(self):
        """增加邮件结尾"""
        int_ret = 0
        try:

            def __body_change():
                if end_line.text() and (end_title.toPlainText().strip() or url_line.text().strip()):
                    button.setEnabled(True)
                else:
                    button.setDisabled(True)

            dialog = QDialog(self.obj_ui)  # 自定义一个dialog
            dialog.setWindowTitle('增加邮件结尾')
            dialog.resize(600, 300)

            grid = QGridLayout()
            grid.setSpacing(10)

            end_label = BaseLabel(dialog, str_text='模板名称').label
            grid.addWidget(end_label, 1, 0)

            end_line = BaseLineEdit(dialog, file_style=QSS_STYLE).lineedit
            end_line.textChanged.connect(__body_change)
            grid.addWidget(end_line, 1, 1, 1, 2)

            end_label_1 = BaseLabel(dialog, str_text='结尾内容').label
            grid.addWidget(end_label_1, 2, 0)

            end_title = QTextEdit(dialog)
            end_title.textChanged.connect(__body_change)
            end_title.setVerticalScrollBar(BaseBar(QSS_STYLE).bar)
            grid.addWidget(end_title, 2, 1, 6, 3)

            url_label = BaseLabel(dialog, str_text='图片地址').label
            grid.addWidget(url_label, 8, 0)

            url_line = BaseLineEdit(dialog, file_style=QSS_STYLE).lineedit
            url_line.textChanged.connect(__body_change)
            grid.addWidget(url_line, 8, 1, 1, 3)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.setDisabled(True)
            grid.addWidget(button, 9, 3)
            button.clicked.connect(dialog.accept)

            dialog.setLayout(grid)
            dialog.show()
            if dialog.exec() == QDialog.Accepted:
                str_1, str_2, str_3 = end_line.text(), sub_html(end_title.toHtml()), url_line.text().strip()
                if any([str_1, str_2, str_3]):
                    int_ret = self.add_info(DIT_DATABASE[self.obj_ui.page], [str_1, str_2, str_3])
                else:
                    int_ret = -1
            else:
                int_ret = -2
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        return int_ret

    def add_table(self):
        """增加页面
        """
        int_ret = 0
        try:
            self.obj_ui.add_button.setDisabled(True)
            # 当前页面
            str_page = self.obj_ui.page
            if str_page == '账号配置':
                int_ret = self.__add_user()
            elif str_page == '邮件标题':
                int_ret = self.__add_title()
            elif str_page == '邮件正文':
                int_ret = self.__add_body()
            elif str_page == '邮件附件':
                int_ret = self.__add_info()
            elif str_page == '邮件结尾':
                int_ret = self.__add_end()
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            self.obj_ui.add_button.setEnabled(True)
            if int_ret == 1:
                self.obj_ui.show_message('成功', '添加成功')
                self.obj_ui.flush_table(True)
            elif int_ret == -1:
                self.obj_ui.show_message('错误', '未正确填写')
            elif int_ret == 0:
                self.obj_ui.show_message('失败', '添加失败, 检查是否重复数据')

    def get_aly(self):
        dit_config = load_file('config.json')
        obj_s3 = AlyS3(dit_config['AccessKey_ID'], dit_config['AccessKey_Secret'], dit_config['bucket'], dit_config['url'])
        self.obj_ui.show_message('', '', 'Aly OSS 连接成功')
        if obj_s3:
            lst_file = obj_s3.get_file()
            if lst_file:
                dialog = QDialog(self.obj_ui)  # 自定义一个dialog
                form_layout = QFormLayout(dialog)  # 配置layout
                dialog.setWindowTitle('查看阿里云S3附件列表')
                dialog.resize(800, 400)
                str_txt = QTextEdit(self.obj_ui)
                str_txt.setVerticalScrollBar(BaseBar(QSS_STYLE).bar)
                str_txt.setReadOnly(True)
                str_txt.setText('\n'.join([dit_file['url'] for dit_file in lst_file]))
                form_layout.addRow('附件列表:', str_txt)
                dialog.show()
            else:
                self.obj_ui.show_message('提示', '阿里云S3无文件或获取失败')
        else:
            self.obj_ui.show_message('错误提示', '上阿里云OSS连接失败,请检查配置', '上阿里云OSS连接失败,请检查配置')

    def __on_checkbox_changed(self, dit_value: dict, state):
        lst_c = []
        try:
            checkbox = self.obj_ui.sender()
            str_user = checkbox.text()
            dit_info = self.dit_v[self.str_page]
            lst_c = dit_info['lst']
            if checkbox.isChecked():
                self.obj_ui.show_message('', '', f'{dit_info["cn"]}:{str_user}已选择')
                lst_c.append(dit_value)
            else:
                self.obj_ui.show_message('', '', f'{dit_info["cn"]}:{str_user}取消选择')
                lst_c.remove(dit_value)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            # 账号,模板 页面的下一步按钮禁用/启用
            if self.str_page in MAST_SELECT_TABLE:
                if lst_c and self.button:
                    self.button.setEnabled(True)
                elif not lst_c and self.button:
                    self.button.setDisabled(True)

    def __on_all_checkbox_changed(self, lst_checkbox, state):
        """全选
        :param lst_checkbox:
        :param state:
        :return:
        """
        try:
            dit_info = self.dit_v[self.str_page]
            if not state:
                dit_info['lst'].clear()
            for dit_value in lst_checkbox:
                dit_value['obj'].setCheckState(2 if state else 0)
                if state:
                    dit_info['lst'].append(dit_value['value'])
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            if self.str_page in MAST_SELECT_TABLE:
                self.button.setEnabled(state)

    def __show_dialog(self, table: str, func):
        dialog = None
        try:

            def __select_lang():
                dialog.resize(300, 100)
                lst_lang = ['全部']
                if table == 'info_lang':
                    lst_lang.extend(self.__get_language('info'))
                elif table == 'body_lang':
                    lst_lang.extend(self.__get_language('body'))
                else:
                    lst_lang.extend(self.__get_language('title'))
                self.lang = BaseComboBox(dialog, QSS_STYLE, lst_data=lst_lang).box
                grad.addWidget(self.lang, 1, 0)
                grad.addWidget(self.button, 1, 1)

            def __select_option():
                dialog.resize(600, 300)
                lst_user = self.get_info(table, int_start=-1).get('lst_ret', [])
                if table in FILTER_TABLE and self.lang:
                    str_lang = self.lang.currentText()
                    if str_lang and str_lang != '全部':
                        lst_user = [dit_info for dit_info in lst_user if dit_info['language'] == str_lang]

                lst_all = []
                # 标题和正文 多了个 全选
                int_row = 1 if str_len > 1 else 2
                int_col = 1 if table in ['body', 'title'] and int_row == 1 else 0
                for item in lst_user:
                    str_t = str(item[str_key])
                    checkbox = QCheckBox(str_t if len(str_t) <= 400 else str_t[:400])
                    checkbox.setStyleSheet("height: 30px")
                    checkbox.clicked.connect(partial(self.__on_checkbox_changed, item))
                    lst_all.append({'obj': checkbox, 'value': item})
                    grad.addWidget(checkbox, int_row, int_col)
                    int_col = int_col + 1 if int_col < str_len - 1 else 0
                    int_row = int_row + 1 if int_col == 0 else int_row
                    grad.addWidget(checkbox, int_row, int_col)
                if table in ['body', 'title'] and lst_all:
                    checkbox = QCheckBox('全选')
                    checkbox.setStyleSheet("height: 30px")
                    checkbox.clicked.connect(partial(self.__on_all_checkbox_changed, lst_all))
                    grad.addWidget(checkbox, 1, 0)
                grad.addWidget(self.button, int_row + 1, str_len)

            str_key, str_len, str_title = self.dit_v[table]['key'], self.dit_v[table]['len'], self.dit_v[table]['cn']
            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle(f'选择{str_title}')
            grad = QGridLayout()
            grad.setSpacing(3)

            self.button = BaseButton(dialog, str_tip='下一步', func=func, tuple_size=(60, 30),
                                     str_img=os.path.join(STATIC_PATH, 'images', 'next.png')).btu

            if table in FILTER_LANG:
                __select_lang()
            else:
                __select_option()
            dialog.setLayout(grad)

            # 账号,模板 按钮最开始禁用
            if table in MAST_SELECT_TABLE:
                self.button.setDisabled(True)
            self.str_page = table
            dialog.show()
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}--{table}")
        return dialog

    def select_user(self):
        """导入用户以及选择配置"""
        try:

            def __import_user():
                """导入客户"""
                try:
                    text_user.clear()
                    file_name, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取文件', os.getcwd(), 'Text File(*.txt)')
                    if os.path.isfile(file_name):
                        with open(file_name, 'r', encoding='utf-8') as f:
                            for str_line in f.readlines():
                                lst_line = [i for i in str_line.strip().rsplit(maxsplit=1) if i.strip()]
                                if len(lst_line) == 2 and '@' in lst_line[1]:
                                    self.to_list.append({'firm': lst_line[0], 'email': lst_line[1]})
                        if not self.to_list:
                            self.obj_ui.show_message('错误提示', '收件人文件格式错误', '收件人文件格式错误')
                        else:
                            self.obj_ui.show_message('提示', '上传收件人文件成功',
                                                     f'上传收件人文件成功, 此次导入收件人: {len(self.to_list)}个')
                            text_user.append('\n'.join([f"{dit_u['firm']}--{dit_u['email']}" for dit_u in self.to_list]))
                    else:
                        self.obj_ui.show_message('错误提示', '收件人文件不存在', '收件人文件不存在')
                except Exception as e:
                    logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
                finally:
                    if self.to_list:
                        button.setEnabled(True)

            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle('导入用户以及设置基本配置')
            dialog.resize(500, 300)

            grid = QGridLayout()
            grid.setSpacing(10)

            label_user_1 = BaseLabel(dialog, str_text='导入联系人').label
            grid.addWidget(label_user_1, 1, 0)

            btu_user = BaseButton(dialog, str_text='导入联系人', func=__import_user).btu
            grid.addWidget(btu_user, 1, 1)

            dear_label = BaseLabel(dialog, str_text='Dear字体').label
            grid.addWidget(dear_label, 1, 2)

            dear_box = BaseComboBox(dialog, file_style=QSS_STYLE, lst_data=DEAR_FONT).box
            grid.addWidget(dear_box, 1, 3, 1, 1)

            label_user_2 = BaseLabel(dialog, str_text='联系人列表').label
            grid.addWidget(label_user_2, 2, 0)

            text_user = QTextEdit(dialog)
            text_user.setReadOnly(True)
            text_user.setVerticalScrollBar(BaseBar(QSS_STYLE).bar)
            grid.addWidget(text_user, 2, 1, 3, 5)

            label_interval = BaseLabel(dialog, str_text='最大发送').label
            grid.addWidget(label_interval, 5, 0)

            interval_edit = BaseLineEdit(dialog, file_style=QSS_STYLE, str_default=str(self.send_mun)).lineedit
            interval_edit.setValidator(QtGui.QIntValidator())
            grid.addWidget(interval_edit, 5, 1)

            label_sleep = BaseLabel(dialog, str_text='发送间隔(s)').label
            grid.addWidget(label_sleep, 5, 2)

            sleep_edit = BaseLineEdit(dialog, file_style=QSS_STYLE, str_default=str(self.sleep_mun)).lineedit
            sleep_edit.setValidator(QtGui.QIntValidator())
            grid.addWidget(sleep_edit, 5, 3)

            radio_button = QRadioButton("带网页", dialog)
            radio_button.setChecked(False)
            grid.addWidget(radio_button, 5, 4)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.clicked.connect(dialog.accept)
            button.setDisabled(True)
            grid.addWidget(button, 6, 4)

            dialog.setLayout(grid)

            dialog.show()

            if dialog.exec() == QDialog.Accepted:
                # 会记录上次使用的值(软件不重启的情况下)
                self.send_mun = str_2_int(interval_edit.text(), self.send_mun)
                self.sleep_mun = str_2_int(sleep_edit.text(), self.sleep_mun)
                self.send_model = radio_button.isChecked()
                self.dear_font = dear_box.currentText()
                dialog.close()
                self.select_account()
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        return

    def select_account(self):
        """选择账号"""
        try:
            if self.to_list:
                # 每次第一个页面先还原一下数据
                for value in self.dit_v.values():
                    value['lst'] = []
                self.dialog = self.__show_dialog(DIT_DATABASE['账号配置'], self.select_title_language)
            else:
                self.obj_ui.show_message('提示', '先导入收件人')
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_title_language(self):
        """选择标题语种
        :return:
        """
        try:
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog('title_lang', self.select_title)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_title(self):
        """选择标题
        :return:
        """
        try:
            # 先关闭上一个的
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog(DIT_DATABASE['邮件标题'], self.select_template_language)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_template_language(self):
        """选择模板语种
        :return:
        """
        try:
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog('body_lang', self.select_templates)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_templates(self):
        """选择邮件内容"""
        try:
            # 先关闭上一个的
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog(DIT_DATABASE['邮件正文'], self.select_info_language)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_info_language(self):
        """选择附件语种
        :return:
        """
        try:
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog('info_lang', self.select_file)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_file(self):
        """选择邮件附件"""
        try:
            # 先关闭上一个的
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog(DIT_DATABASE['邮件附件'], self.select_end)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_end(self):
        """选择邮件结尾"""
        try:
            # 先关闭上一个的
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog(DIT_DATABASE['邮件结尾'], self.send_email)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def send_email(self):
        try:
            # 先关闭上一个的
            if self.dialog:
                self.dialog.close()
            lst_user = self.dit_v.get('user', {}).get('lst', [])
            lst_body = self.dit_v.get('body', {}).get('lst', [])
            lst_title = self.dit_v.get('title', {}).get('lst', [])
            # 起码保证 客户, 账号, 模板有
            if any([self.to_list, lst_user, lst_body, lst_title]):
                # 获取邮件标题和内容组合数
                lst_text = list(
                    product([dit_text['str_title'] for dit_text in lst_title], [dit_text['str_body'] for dit_text in lst_body]))
                lst_info = [dit_info['url'] for dit_info in self.dit_v.get('info', {}).get('lst', [])]
                lst_end = self.dit_v.get('end', {}).get('lst', [])
                self.obj_ui.show_message('提示', '正在后台发送中,请稍等......', '正在后台发送中,请稍等......')
                threading.Thread(target=self.__send_mail, args=(lst_user, lst_text, lst_info, lst_end), daemon=True).start()
            else:
                self.obj_ui.show_message('错误', '缺少数据,无法发送邮件.请重试')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            # 这是最后一个 要置空
            self.dialog = None
            self.lang = None

    def __send_mail(self, lst_user: list, lst_text: list, lst_info: list, lst_end: list):
        """发送邮件"""
        # 发送成功的数量
        int_num = 0
        int_count = 0
        # 收件人数量
        int_len = len(self.to_list)
        # 标题组合存在的数量
        int_title = len(lst_text)
        # 账号数量
        int_user = len(lst_user)
        try:
            # 分配任务
            lst_task = []
            k = 0
            for i in range(0, int_len, self.send_mun):
                if k >= int_user:
                    k = 0
                lst_task.append({
                    'send': self.to_list[i: i + self.send_mun],
                    'user': lst_user[k]
                })
                k += 1

            self.obj_ui.show_message('', '', f"当前发送策略: {'携带网页' if self.send_model else '不携带网页'}, "
                                             f"间隔时间: {self.sleep_mun}s, 轮询数量: {self.send_mun}")

            # 是否携带网页
            str_html = ''
            if self.send_model:
                try:
                    with open(os.path.join(STATIC_PATH, 'templates', 'templates.html'), 'r', encoding='utf-8') as f:
                        str_html = f.read()
                except Exception as er:
                    logger.error(f"{er.__traceback__.tb_lineno}:--:{er}")
            # 附件
            if lst_info:
                # 附件图标
                info_html = '<br><br> <hr><p>attachment：</p><img style="width: 20px; height: 20px;" ' \
                            'src="http://img.mp.itc.cn/upload/20170406/690f8eb8b38144028ee4bf0f04233901.png">'
                # 附件内容
                for str_url in lst_info:
                    str_name = str_url.rsplit("/", 1)[-1]  # type: str
                    if str_name.endswith('.pdf'):
                        info_html += f'<a href="{str_url}" target="_blank" download="{str_name}">{str_name}</a><br>'
                    else:
                        info_html += f'<p><img src="{str_url}"></span></p><br>'
            else:
                info_html = ''

            for dit_key in lst_task:
                dit_user = dit_key['user']
                obj_smtp = self.__login(dit_user['name'], dit_user['pwd'], dit_user['str_type'])
                # key 是公司名称  value 是邮箱
                for dit_send in dit_key['send']:
                    try:
                        #  按索引取值
                        tuple_text = lst_text[int_count % int_title]
                        # 公司名称 + 正文 + 网页
                        firm = dit_send["firm"]
                        str_txt = f'<p style="font-family: {self.dear_font};"> Dear {firm}</p>' + '<br>' + \
                                  tuple_text[1] + '<br>' + str_html
                        # 结尾
                        if lst_end:
                            dit_end = choice(lst_end)
                            end_html, end_url = dit_end.get('content', ''), dit_end.get('url', '')
                            # 加结尾
                            if end_html:
                                str_txt += '<br><br><br>' + end_html
                            # 加结尾图片
                            if end_url:
                                str_txt += f'<p><img src="{end_url}"></span></p>'
                        # 加附件
                        if info_html:
                            str_txt += info_html
                        # 转HTML
                        obj_email = MIMEMultipart('related')
                        # 设置标题
                        obj_email["Subject"] = Header(tuple_text[0], "utf-8")
                        # 日期
                        obj_email['Date'] = formatdate(localtime=True)
                        # 接收人
                        obj_email['To'] = ', '.join([dit_send['email']])
                        obj_email['From'] = dit_user['name']
                        str_html_ = MIMEText(str_txt, 'html', 'utf-8')
                        obj_email.attach(str_html_)
                        obj_smtp.sendmail(dit_user['name'], [dit_send['email']], obj_email.as_string())
                        int_num += 1
                        self.obj_ui.show_message('', '', f"{dit_user['name']} --> {dit_send['email']} 成功")
                        time.sleep(self.sleep_mun)
                    except Exception as err:
                        logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
                    finally:
                        int_count += 1
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            self.obj_ui.show_message('', f'', f'本轮发送结束. 一共需要发送: {int_len}封邮件, 发送成功: {int_num}封邮件')
            # 还原数据
            self.to_list.clear()
            for value in self.dit_v.values():
                value['lst'] = []
