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
from utils.tools import sub_html, word_2_html, load_file
from constant import INT_LIMIT, BASE_PATH, DIT_DATABASE, DIT_EMAIL, FILTER_TABLE, FILTER_LANG, QSS_STYLE
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox, \
    QTextEdit, QFileDialog, QCheckBox, QGridLayout, QPushButton, QVBoxLayout, QRadioButton, QHBoxLayout
from ui.base_ui import BaseButton, BaseLabel, BaseLineEdit


class EmailTools:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui
        self.email_dict = load_file()
        self.to_list = []
        self.str_page = ''  # 当前在那个选择页
        self.dit_v = {
            'user': {'key': 'name', 'len': 5, 'lst': [], 'cn': '账号'},
            'body': {'key': 'str_body', 'len': 1, 'lst': [], 'cn': '内容'},
            'title': {'key': 'str_title', 'len': 3, 'lst': [], 'cn': '标题'},
            'info': {'key': 'url', 'len': 2, 'lst': [], 'cn': '附件'},
            'end': {'key': 'name', 'len': 5, 'lst': [], 'cn': '结尾'},
            'info_lang': {'key': 'language', 'len': 3, 'lst': [], 'cn': '附件语种'},
            'body_lang': {'key': 'language', 'len': 3, 'lst': [], 'cn': '正文语种'},
            'title_lang': {'key': 'language', 'len': 3, 'lst': [], 'cn': '标题语种'},
        }
        self.dialog = None  # 下一步之前的页面 用于下一步后 关闭上一个页面
        self.button = None  # 每个页面的下一步按钮
        self.send_mun = 50  # 一个账号一次发50封
        self.lang = None
        self.str_url = ''

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

    @staticmethod
    def get_info(table: str, where: str = '', int_start: int = 1, int_limit: int = INT_LIMIT):
        """获取数据库信息"""
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

    def import_user(self):
        """导入客户"""
        try:
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
                    self.obj_ui.show_message('提示', '上传收件人文件成功', f'上传收件人文件成功, 此次导入收件人: {len(self.to_list)}个')
            else:
                self.obj_ui.show_message('错误提示', '收件人文件不存在', '收件人文件不存在')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    @staticmethod
    def __get_language(str_type: str):
        with MySql() as obj_sql:
            lst_info = obj_sql.get_language(str_type)
        return lst_info

    def __add_user(self):
        dialog = QDialog(self.obj_ui)  # 自定义一个dialog
        form_layout = QFormLayout(dialog)  # 配置layout
        dialog.setWindowTitle('增加邮箱账号')
        dialog.resize(300, 100)
        user_input = QLineEdit(self.obj_ui)
        user_input.setStyleSheet("height: 20px")
        form_layout.addRow('邮箱账号:', user_input)
        pwd_input = QLineEdit(self.obj_ui)
        pwd_input.setStyleSheet("height: 20px")
        form_layout.addRow('邮箱密码:', pwd_input)
        serve_box = QComboBox(self.obj_ui)
        serve_box.addItems([dit_e['name_cn'] for dit_e in self.email_dict.values()])
        serve_box.setStyleSheet("height: 20px")
        form_layout.addRow('邮箱服务器:', serve_box)
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        form_layout.addRow(button)
        button.clicked.connect(dialog.accept)
        dialog.show()
        if dialog.exec() == QDialog.Accepted:
            str_type = DIT_EMAIL.get(serve_box.currentText(), '腾讯邮箱')
            str_1, str_2 = user_input.text().strip(), pwd_input.text().strip()
            if all([str_1, str_2, str_type]):
                return self.add_info(DIT_DATABASE[self.obj_ui.page], [str_1, str_2, str_type])
            return -1

    def __add_title(self):
        str_file, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取邮件标题文件', os.getcwd(), 'Text File(*.txt)')
        if os.path.isfile(str_file):
            with open(str_file, 'r', encoding='utf-8') as f:
                dialog = QDialog(self.obj_ui)  # 自定义一个dialog
                dialog.resize(500, 200)
                form_layout = QFormLayout(dialog)  # 配置layout
                dialog.setWindowTitle('增加邮件标题')
                str_txt = QTextEdit(self.obj_ui)
                str_txt.setText(f.read())
                form_layout.addRow('邮件标题:', str_txt)
                button = QDialogButtonBox(QDialogButtonBox.Ok)
                form_layout.addRow(button)
                button.clicked.connect(dialog.accept)
                dialog.show()
                if dialog.exec() == QDialog.Accepted:
                    if str_txt:
                        for str_t in str_txt.toPlainText().split('\n'):
                            if str_t.strip() and ' ' in str_t:
                                self.add_info(DIT_DATABASE[self.obj_ui.page], str_t.rsplit(maxsplit=1))
                        return 1
                    else:
                        return -1
        else:
            self.obj_ui.show_message('错误', '未选择文件')

    def __add_body(self):
        str_file, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取邮件正文文件', os.getcwd(), 'Text File(*.docx)')
        if os.path.isfile(str_file):
            result = word_2_html(str_file)
            if result:
                dialog = QDialog(self.obj_ui)  # 自定义一个dialog
                form_layout = QFormLayout(dialog)  # 配置layout
                dialog.setWindowTitle('增加邮件正文')
                dialog.resize(1000, 500)
                str_txt = QTextEdit(self.obj_ui)
                str_txt.setHtml(result)
                form_layout.addRow('邮件正文:', str_txt)
                str_box = QComboBox(self.obj_ui)
                str_box.addItems(self.__get_language('body'))
                str_box.setEditable(True)
                form_layout.addRow('模板语种:', str_box)
                button = QDialogButtonBox(QDialogButtonBox.Ok)
                form_layout.addRow(button)
                button.clicked.connect(dialog.accept)
                dialog.show()
                if dialog.exec() == QDialog.Accepted:
                    str_2, str_3 = sub_html(str_txt.toHtml()), str_box.currentText().strip()
                    if all([str_2, str_3]):
                        return self.add_info(DIT_DATABASE[self.obj_ui.page], [str_2, str_3])
                    return -1
            else:
                self.obj_ui.show_message('错误', 'Word未获取到内容')
        else:
            self.obj_ui.show_message('错误', '未选择文件')

    def __add_info(self):
        dialog = QDialog(self.obj_ui)  # 自定义一个dialog
        form_layout = QFormLayout(dialog)  # 配置layout
        dialog.setWindowTitle('增加邮件附件')
        dialog.resize(600, 100)
        push_button = QPushButton()
        push_button.setText('选择本地文件上传并使用')
        form_layout.addRow('本地上传:', push_button)
        file_path = QLineEdit(self.obj_ui)
        file_path.setStyleSheet("height: 20px")
        form_layout.addRow('现有附件S3地址:', file_path)
        push_button.clicked.connect(partial(self.__upload_aly, file_path))
        str_box = QComboBox(self.obj_ui)
        str_box.addItems(self.__get_language('info'))
        str_box.setEditable(True)
        form_layout.addRow('附件语种:', str_box)
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        form_layout.addRow(button)
        button.clicked.connect(dialog.accept)
        dialog.show()
        if dialog.exec() == QDialog.Accepted:
            str_1, str_2 = file_path.text().strip(), str_box.currentText().strip()
            if all([str_1, str_2]):
                return self.add_info(DIT_DATABASE[self.obj_ui.page], [str_1, str_2])
            return -1

    def __add_end(self):
        dialog = QDialog(self.obj_ui)  # 自定义一个dialog
        form_layout = QFormLayout(dialog)  # 配置layout
        dialog.setWindowTitle('增加邮件结尾')
        dialog.resize(1000, 500)
        temp_name = QLineEdit(self.obj_ui)
        temp_name.setStyleSheet("height: 20px")
        form_layout.addRow('模板名称:', temp_name)
        temp_txt = QTextEdit(self.obj_ui)
        form_layout.addRow('结尾内容', temp_txt)
        url_path = QLineEdit(self.obj_ui)
        url_path.setStyleSheet("height: 20px")
        form_layout.addRow('图片地址:', url_path)
        form_layout.addRow(url_path)
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        form_layout.addRow(button)
        button.clicked.connect(dialog.accept)
        dialog.show()
        if dialog.exec() == QDialog.Accepted:
            str_1, str_2, str_3 = temp_name.text(), sub_html(temp_txt.toHtml()), url_path.text().strip()
            if any([str_1, str_2, str_3]):
                return self.add_info(DIT_DATABASE[self.obj_ui.page], [str_1, str_2, str_3])
            return -1

    def add_table(self):
        """增加页面
        """
        int_ret = 0
        try:
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
            if int_ret == 1:
                self.obj_ui.show_message('成功', '添加成功')
                self.obj_ui.flush_table(True)
            elif int_ret == -1:
                self.obj_ui.show_message('错误', '未正确填写')
            elif int_ret == 0:
                self.obj_ui.show_message('失败', '添加失败')

    def __upload_aly(self, obj_file_line = None):
        """上传文件至阿里云"""
        title = 'Text File(*.pdf);;JPG File(*.jpg);;PNG File(*.png)'
        str_file, _ = QFileDialog.getOpenFileName(self.obj_ui, '选择本地附件上传', os.getcwd(), title)
        if os.path.isfile(str_file):
            dit_config = load_file('config.json')
            obj_s3 = AlyS3(dit_config['AccessKey_ID'], dit_config['AccessKey_Secret'], dit_config['bucket'], dit_config['url'])
            self.obj_ui.show_message('', '', 'Aly OSS 连接成功')
            if obj_s3:
                try:
                    if obj_s3.push_file(str_file) == 1:
                        self.str_url = f"https://{dit_config['bucket']}.{dit_config['url'][8:]}/{os.path.split(str_file)[-1]}"
                        self.obj_ui.show_message('', '', f'附件{str_file} 上传成功, 保存地址: {self.str_url}')
                        if obj_file_line and self.str_url:
                            obj_file_line.setText(self.str_url)
                except Exception as e:
                    self.obj_ui.show_message('', '', f"{e.__traceback__.tb_lineno}:{e}")
            else:
                self.obj_ui.show_message('错误提示', '上阿里云OSS连接失败,请检查配置', '上阿里云OSS连接失败,请检查配置')
        else:
            self.obj_ui.show_message('错误', '未选择文件')

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
            if self.str_page in FILTER_TABLE:
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
            if self.str_page in FILTER_TABLE:
                self.button.setEnabled(state)

    def __show_dialog(self, table: str, func):
        dialog = None
        try:
            str_key, str_len, str_title = self.dit_v[table]['key'], self.dit_v[table]['len'], self.dit_v[table]['cn']
            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle(f'选择{str_title}')
            dialog.resize(800, 600)

            # 创建多选按钮
            layout = QGridLayout()
            if table in FILTER_LANG:
                int_count = 1
                lst_lang = ['全部'] + self.__get_language('info' if table == 'info_lang' else ('body' if table == 'body_lang'
                                                                                             else 'title'))
                self.lang = QComboBox(self.obj_ui)
                self.lang.setStyleSheet("height: 30px")
                self.lang.addItems(lst_lang)
                layout.addWidget(self.lang, 0, 0)
            else:
                int_count = 0 if table not in ['body', 'title'] else 1
                # 数据源
                lst_user = self.get_info(table, int_start=-1).get('lst_ret', [])
                if table in FILTER_TABLE and self.lang:
                    str_lang = self.lang.currentText()
                    if str_lang and str_lang != '全部':
                        lst_user = [dit_info for dit_info in lst_user if dit_info['language'] == str_lang]
                lst_all = []
                for i, item in enumerate(lst_user, int_count):
                    str_t = str(item[str_key])
                    checkbox = QCheckBox(str_t if len(str_t) <= 400 else str_t[:400])
                    checkbox.setStyleSheet("height: 30px")
                    checkbox.clicked.connect(partial(self.__on_checkbox_changed, item))
                    row = i // str_len
                    col = i % str_len
                    layout.addWidget(checkbox, row, col)
                    int_count += 1
                    lst_all.append({'obj': checkbox, 'value': item})
                if table in ['body', 'title']:
                    checkbox = QCheckBox('全选')
                    checkbox.setStyleSheet("height: 30px")
                    checkbox.clicked.connect(partial(self.__on_all_checkbox_changed, lst_all))
                    layout.addWidget(checkbox, 0, 0)
            dialog.setLayout(layout)
            self.button = QPushButton('下一步')
            # 账号,模板 按钮最开始禁用
            if table in FILTER_TABLE:
                self.button.setDisabled(True)
            self.button.clicked.connect(func)
            layout.addWidget(self.button, int_count, str_len)
            self.str_page = table
            dialog.show()
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}--{table}")
        return dialog

    def select_user(self):
        """导入用户以及选择配置"""
        try:
            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle('导入用户以及设置基本配置')
            dialog.resize(500, 300)
            # 横向布局
            h_layout_1 = QHBoxLayout()
            label_user = BaseLabel(dialog, str_text='导入联系人').label
            btu_user = BaseButton(dialog, str_text='选择联系人文件', func=self.import_user).btu
            h_layout_1.addWidget(label_user)
            h_layout_1.addWidget(btu_user)

            h_layout_2 = QHBoxLayout()
            label_interval = BaseLabel(dialog, str_text='最大发送').label
            interval_edit = BaseLineEdit(dialog, (820, 20, 80, 30), QSS_STYLE, '50').lineedit
            interval_edit.setValidator(QtGui.QIntValidator())
            h_layout_2.addWidget(label_interval)
            h_layout_2.addWidget(interval_edit)

            h_layout_3 = QHBoxLayout()
            label_sleep = BaseLabel(dialog, str_text='发送间隔(s)').label
            sleep_edit = BaseLineEdit(dialog, (565, 20, 80, 30), QSS_STYLE, '20').lineedit
            sleep_edit.setValidator(QtGui.QIntValidator())
            h_layout_3.addWidget(label_sleep)
            h_layout_3.addWidget(sleep_edit)

            radio_button = QRadioButton("带网页", dialog)
            radio_button.setChecked(False)

            # 垂直布局
            v_layout = QVBoxLayout()
            v_layout.addLayout(h_layout_1)
            v_layout.addLayout(h_layout_2)
            v_layout.addLayout(h_layout_3)
            v_layout.addWidget(radio_button)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            v_layout.addWidget(button)
            button.clicked.connect(dialog.accept)

            dialog.setLayout(v_layout)

            dialog.show()

            if dialog.exec() == QDialog.Accepted:
                print(self.to_list)
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
        self.send_mun = int(self.obj_ui.interval_edit.text() or self.send_mun)
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

            # 是否携带网页
            contain_html = self.obj_ui.radio_button.isChecked()
            # 间隔时间
            int_sleep = int(self.obj_ui.sleep_edit.text() or 20)
            self.obj_ui.show_message('', '', f"当前发送策略: {'携带网页' if contain_html else '不携带网页'}, 间隔时间: {int_sleep}s, 轮询数量: {self.send_mun}")

            if contain_html:
                with open(os.path.join(BASE_PATH, 'body', 'templates.html'), 'r', encoding='utf-8') as f:
                    str_html = f.read()
            else:
                str_html = ''

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
                        str_txt = f'Dear {firm}<br><br>' + tuple_text[1] + '<br>' + str_html
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
                        time.sleep(int_sleep)
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
