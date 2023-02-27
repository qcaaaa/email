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
import threading
from json import load
from aly_s3 import AlyS3
from loguru import logger
from datetime import datetime
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QPlainTextEdit, QComboBox, \
    QTextEdit,  QFileDialog

from sql_db import MySql
from constant import INT_LIMIT, BASE_PATH, DIT_DATABASE


class EmailTools:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui
        self.email_dict = self.load_file()

    @staticmethod
    def __sub_html(str_html: str) -> str:
        try:
            import re
            str_html = '\n'.join(re.findall('<p .*</p>', str_html))
        except Exception as err:
            logger.error(f'截取html失败: {err.__traceback__.tb_lineno}: {err}')
        return str_html

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
    def add_info(table: str, dit_data: dict):
        """增加数据库信息"""
        with MySql() as obj_sql:
            int_ret = obj_sql.add_sql(table, dit_data)
        return int_ret

    @staticmethod
    def load_file():
        dit_info = {}
        try:
            with open(os.path.join(BASE_PATH, 'email.json'), 'r', encoding='utf-8') as f:
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
                dit_data = {}
                if str_page == '账号配置':
                    if serve_box.currentText() == '阿里企业邮箱':
                        str_type = '1'
                    elif serve_box.currentText() == '网易邮箱':
                        str_type = '2'
                    else:
                        str_type = '3'
                    dit_data = {'name': user_input.text().strip(), 'pwd': pwd_input.text().strip(), 'str_type': str_type}
                elif str_page == '邮件模板':
                    dit_data = {'title': str_title.text().strip(), 'content': self.__sub_html(str_txt.toHtml())}
                elif str_page == '邮件结尾':
                    dit_data = {'content': self.__sub_html(temp_txt.toHtml()), 'url': url_path.text().strip(), 'name': temp_name.text()}
                if dit_data:
                    int_ret = self.add_info(DIT_DATABASE[str_page], dit_data)
                    self.show_message('成功' if int_ret == 1 else '失败', '添加成功' if int_ret == 1 else '添加失败')
                    if int_ret == 1:
                        self.obj_ui.flush_table(True)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
            self.show_message('错误', '添加失败')

    def check_email(self):
        """邮箱检测"""
        file_name, _ = QFileDialog.getOpenFileName(self.obj_ui, '选取文件', os.getcwd(), 'Text File(*.txt)')
        if os.path.isfile(file_name):
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    lst_email = [i for i in f.read().split('\n') if i.strip()]
                if lst_email:
                    self.show_message('提示', '上传邮箱账号文件成功,后台正在校验中....', '上传邮箱账号文件成功,后台正在校验中....')
                    from email_check import check_email
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
            with open('./config.json', 'rb') as f:
                dit_config = load(f)
                obj_s3 = AlyS3(dit_config['AccessKey_ID'], dit_config['AccessKey_Secret'], dit_config['bucket'],
                               dit_config['url'])
                self.show_message('', '', 'Aly OSS 连接成功')
                if obj_s3:
                    for str_path in lst_file:
                        try:
                            if os.path.isfile(str_path) and obj_s3.push_file(str_path) == 1:
                                int_num += 1
                                url = f"https://{dit_config['bucket']}.{dit_config['url'][8:]}/{os.path.split(str_path)[-1]}"
                                int_ret = self.add_info('info', {'url': url})
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

