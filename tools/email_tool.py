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
from json import load
from tools.aly_s3 import AlyS3
from sql.sql_db import MySql
from loguru import logger
from random import choice
from functools import partial
from datetime import datetime
from itertools import product
from email.header import Header
from email.utils import formatdate
from PyQt5.QtGui import QTextCursor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constant import INT_LIMIT, BASE_PATH, DIT_DATABASE, CONFIG_PATH
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox, \
    QTextEdit, QFileDialog, QCheckBox, QGridLayout, QPushButton


class EmailTools:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui
        self.email_dict = self.load_file()
        self.to_list = []
        self.str_page = ''  # 当前在那个选择页
        self.dit_v = {
            'user': {'key': 'name', 'len': 10, 'lst': [], 'cn': '账号'},
            'template': {'key': 'title', 'len': 5, 'lst': [], 'cn': '标题/内容'},
            'info': {'key': 'url', 'len': 3, 'lst': [], 'cn': '附件'},
            'end': {'key': 'name', 'len': 10, 'lst': [], 'cn': '结尾'}
        }
        self.dialog = None  # 下一步之前的页面 用于下一步后 关闭上一个页面
        self.button = None  # 每个页面的下一步按钮
        self.send_mun = 50  # 一个账号一次发50封

    @staticmethod
    def __sub_html(str_html: str) -> str:
        try:
            import re
            str_html = '\n'.join(re.findall('<p .*</p>', str_html))
        except Exception as err:
            logger.error(f'截取html失败: {err.__traceback__.tb_lineno}: {err}')
        return str_html

    def __login(self, str_user: str, str_pwd: str, str_type: str):
        try:
            dit_config = self.load_file()
            str_server, int_port = dit_config[str_type]['server'], dit_config[str_type]['port']
            obj_smtp = smtplib.SMTP(str_server, port=int_port, local_hostname='localhost')
            obj_smtp.login(str_user, str_pwd)
        except Exception as err:
            self.show_message('', '', f"{err.__traceback__.tb_lineno}: {err}")
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

    @staticmethod
    def load_file(str_file: str = 'email.json'):
        dit_info = {}
        try:
            with open(os.path.join(CONFIG_PATH, str_file), 'r', encoding='utf-8') as f:
                dit_info = load(f)
        except Exception as err_msg:
            logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
        return dit_info

    def show_message(self, title: str = '', text: str = '', info: str = ''):
        try:
            if title and text:
                QMessageBox.information(self.obj_ui, title, text, QMessageBox.Yes)
            if info:
                self.obj_ui.log_text.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {info}")
                self.obj_ui.log_text.moveCursor(QTextCursor.End)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

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
                    self.show_message('错误提示', '收件人文件格式错误', '收件人文件格式错误')
                else:
                    self.show_message('提示', '上传收件人文件成功', f'上传收件人文件成功, 此次导入收件人: {len(self.to_list)}个')
            else:
                self.show_message('错误提示', '收件人文件不存在', '收件人文件不存在')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            if self.to_list:
                self.obj_ui.send_button.setEnabled(True)
            else:
                self.obj_ui.send_button.setDisabled(True)

    def add_table(self):
        """增加页面
        """
        try:
            # 当前页面
            str_page = self.obj_ui.page
            dialog = QDialog(self.obj_ui)  # 自定义一个dialog
            formLayout = QFormLayout(dialog)  # 配置layout
            if str_page == '账号配置':
                dialog.setWindowTitle('增加邮箱账号')
                dialog.resize(300, 100)
                user_input = QLineEdit(self.obj_ui)
                formLayout.addRow('邮箱账号:', user_input)
                pwd_input = QLineEdit(self.obj_ui)
                formLayout.addRow('邮箱密码:', pwd_input)
                serve_box = QComboBox(self.obj_ui)
                serve_box.addItems([dit_e['name_cn'] for dit_e in self.email_dict.values()])
                formLayout.addRow('邮箱服务器:', serve_box)
            elif str_page == '邮件模板':
                dialog.setWindowTitle('增加邮件标题/正文')
                dialog.resize(600, 300)
                str_title = QLineEdit(self.obj_ui)
                formLayout.addRow('邮件标题:', str_title)
                str_txt = QTextEdit(self.obj_ui)
                formLayout.addRow('邮件正文:', str_txt)
            elif str_page == '邮件附件':
                dialog.setWindowTitle('增加邮件附件')
                dialog.resize(300, 100)
                file_path = QLineEdit(self.obj_ui)
                formLayout.addRow('附件地址:', file_path)
                formLayout.addRow(file_path)
            elif str_page == '邮件结尾':
                dialog.setWindowTitle('增加邮件结尾')
                dialog.resize(500, 300)
                temp_name = QLineEdit(self.obj_ui)
                formLayout.addRow('模板名称:', temp_name)
                temp_txt = QTextEdit(self.obj_ui)
                formLayout.addRow('结尾内容', temp_txt)
                url_path = QLineEdit(self.obj_ui)
                formLayout.addRow('图片地址:', url_path)
                formLayout.addRow(url_path)
            button = QDialogButtonBox(QDialogButtonBox.Ok)
            formLayout.addRow(button)
            button.clicked.connect(dialog.accept)
            dialog.show()
            if dialog.exec() == QDialog.Accepted:
                lst_data = []
                if str_page == '账号配置':
                    if serve_box.currentText() == '阿里企业邮箱':
                        str_type = '1'
                    elif serve_box.currentText() == '网易邮箱':
                        str_type = '3'
                    else:
                        str_type = '2'
                    str_1, str_2, str_3 = user_input.text().strip(), pwd_input.text().strip(), str_type
                    if all([str_1, str_2, str_3]):
                        lst_data = [str_1, str_2, str_3]
                elif str_page == '邮件模板':
                    str_1, str_2 = str_title.text().strip(), self.__sub_html(str_txt.toHtml())
                    if any([str_1, str_2]):
                        lst_data = [str_1, str_2]
                elif str_page == '邮件结尾':
                    str_1, str_2, str_3 = temp_name.text(), self.__sub_html(temp_txt.toHtml()), url_path.text().strip()
                    if any([str_1, str_2, str_3]):
                        lst_data = [str_1, str_2, str_3]
                elif str_page == '邮件附件':
                    str_1 = file_path.text().strip()
                    if str_1:
                        lst_data = [str_1]
                if lst_data:
                    int_ret = self.add_info(DIT_DATABASE[str_page], lst_data)
                    self.show_message('成功' if int_ret == 1 else '失败', '添加成功' if int_ret == 1 else '添加失败')
                    if int_ret == 1:
                        self.obj_ui.flush_table(True)
                else:
                    self.show_message('错误', '未正确填写')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
            self.show_message('错误', '添加失败')

    def check_email(self):
        """邮箱检测"""
        file_name, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取文件', os.getcwd(), 'Text File(*.txt)')
        if os.path.isfile(file_name):
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    lst_email = list(set([i for i in f.read().split('\n') if i.strip()]))
                if lst_email:
                    self.show_message('提示', '上传邮箱账号文件成功,后台正在校验中....', '上传邮箱账号文件成功,后台正在校验中....')
                    from tools.email_check import check_email
                    threading.Thread(target=check_email, args=(lst_email, self), daemon=True).start()
                else:
                    self.show_message('错误提示', '邮箱账号文件格式错误', '邮箱账号文件格式错误')
            except Exception as e:
                self.show_message('', '', f"{e.__traceback__.tb_lineno}:{e}")
        else:
            self.show_message('错误提示', '邮箱账号文件不存在', '邮箱账号文件不存在')

    def upload_aly(self):
        """上传文件至阿里云"""
        title = 'Text File(*.pdf);;JPG File(*.jpg);;PNG File(*.png)'
        lst_file, _ = QFileDialog.getOpenFileNames(self.obj_ui, '选取文件', os.getcwd(), title)
        int_num = 0
        if lst_file:
            dit_config = self.load_file('config.json')
            obj_s3 = AlyS3(dit_config['AccessKey_ID'], dit_config['AccessKey_Secret'], dit_config['bucket'],
                           dit_config['url'])
            self.show_message('', '', 'Aly OSS 连接成功')
            if obj_s3:
                for str_path in lst_file:
                    try:
                        if os.path.isfile(str_path) and obj_s3.push_file(str_path) == 1:
                            int_num += 1
                            url = f"https://{dit_config['bucket']}.{dit_config['url'][8:]}/{os.path.split(str_path)[-1]}"
                            int_ret = self.add_info('info', [url])
                            self.show_message('', '', f'附件{str_path} 保存{"成功" if int_ret == 1 else "失败"}')
                    except Exception as e:
                        self.show_message('', '', f"{e.__traceback__.tb_lineno}:{e}")
                else:
                    self.show_message('提示', f'本次上传文件至阿里云OSS成功{int_num}个文件', f'本次上传文件至阿里云OSS成功{int_num}个文件')
                    if self.obj_ui.page == '邮件附件':
                        self.obj_ui.flush_table(True)
            else:
                self.show_message('错误提示', '上阿里云OSS连接失败,请检查配置', '上阿里云OSS连接失败,请检查配置')
        else:
            self.show_message('错误提示', '未选择文件', '未选择文件')

    def __on_checkbox_changed(self, dit_value: dict, state):
        lst_c = []
        try:
            checkbox = self.obj_ui.sender()
            str_user = checkbox.text()
            dit_info = self.dit_v[self.str_page]
            lst_c = dit_info['lst']
            if checkbox.isChecked():
                self.show_message('', '', f'{dit_info["cn"]}:{str_user}已选择')
                lst_c.append(dit_value)
            else:
                self.show_message('', '', f'{dit_info["cn"]}:{str_user}取消选择')
                lst_c.remove(dit_value)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            # 账号,模板 页面的下一步按钮禁用/启用
            if self.str_page in ['user', 'template']:
                if lst_c and self.button:
                    self.button.setEnabled(True)
                elif not lst_c and self.button:
                    self.button.setDisabled(True)

    def __show_dialog(self, table: str, func):
        dialog = None
        try:
            str_key, str_len, str_title = self.dit_v[table]['key'], self.dit_v[table]['len'], self.dit_v[table]['cn']
            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle(f'选择{str_title}')
            dialog.resize(400, 200)
            # 数据源
            lst_user = self.get_info(table).get('lst_ret', [])
            # 创建多选按钮
            lst_checkboxes = []
            for i, item in enumerate(lst_user):
                checkbox = QCheckBox(str(item[str_key]))
                # checkbox.stateChanged.connect(self.__on_checkbox_changed)
                checkbox.clicked.connect(partial(self.__on_checkbox_changed, item))
                lst_checkboxes.append(checkbox)
            # 创建布局
            layout = QGridLayout()
            for i, checkbox in enumerate(lst_checkboxes):
                row = i // str_len
                col = i % str_len
                layout.addWidget(checkbox, row, col)
            dialog.setLayout(layout)
            self.button = QPushButton('下一步')
            # 账号,模板 按钮最开始禁用
            if table in ['user', 'template']:
                self.button.setDisabled(True)
            self.button.clicked.connect(func)
            layout.addWidget(self.button, len(lst_checkboxes), str_len)
            self.str_page = table
            dialog.show()
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}--{table}")
        return dialog

    def select_account(self):
        """选择账号"""
        try:
            if self.to_list:
                # 每次第一个页面先还原一下数据
                for value in self.dit_v.values():
                    value['lst'] = []
                self.dialog = self.__show_dialog(DIT_DATABASE['账号配置'], self.select_templates)
            else:
                self.show_message('提示', '先导入收件人')
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")

    def select_templates(self):
        """选择邮件内容"""
        try:
            # 先关闭上一个的
            if self.dialog:
                self.dialog.close()
            self.dialog = self.__show_dialog(DIT_DATABASE['邮件模板'], self.select_file)
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
        """选择邮件附件"""
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
            lst_text = self.dit_v.get('template', {}).get('lst', [])
            # 起码保证 客户, 账号, 模板有
            if any([self.to_list, lst_user, lst_text]):
                # 先把邮件标题和内容拆开 获取组合数
                lst_text = list(
                    product([dit_text['title'] for dit_text in lst_text], [dit_text['content'] for dit_text in lst_text]))
                lst_info = [dit_info['url'] for dit_info in self.dit_v.get('info', {}).get('lst', [])]
                lst_end = self.dit_v.get('end', {}).get('lst', [])
                self.show_message('提示', '正在后台发送中,请稍等......', '正在后台发送中,请稍等......')
                threading.Thread(target=self.__send_mail, args=(lst_user, lst_text, lst_info, lst_end), daemon=True).start()
            else:
                self.show_message('错误', '缺少数据,无法发送邮件.请重试')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            # 这是最后一个 要置空
            self.dialog = None

    def __send_mail(self, lst_user: list, lst_text: list, lst_info: list, lst_end: list):
        """发送邮件"""
        # 发送成功的数量
        int_num = 0
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
            contain_html = self.obj_ui.contain_html.currentText()
            # 间隔时间
            int_sleep = int(self.obj_ui.sleep_edit.text() or 20)
            self.show_message('', '', f"当前发送策略: {contain_html}, 间隔时间: {int_sleep}s, 轮询数量: {self.send_mun}")

            if contain_html == '带网页':
                with open(os.path.join(BASE_PATH, 'template', 'templates.html'), 'r', encoding='utf-8') as f:
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
                        tuple_text = lst_text[int_num] if int_num < int_title else lst_text[int_num - int_title]
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
                        self.show_message('', '', f"{dit_user['name']} --> {dit_send['email']} 成功")
                        time.sleep(int_sleep)
                    except Exception as err:
                        logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
                else:
                    if obj_smtp:
                        obj_smtp.close()
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            self.show_message('', f'', f'本轮发送结束. 一共需要发送: {int_len}封邮件, 发送成功: {int_num}封邮件')
            # 还原数据
            self.to_list.clear()
            for value in self.dit_v.values():
                value['lst'] = []
