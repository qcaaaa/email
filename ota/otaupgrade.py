# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : otaupgrade.py

@Email: yypqcaa@163.com

@Date : 2023/4/17 20:37

@Desc :
"""

import os
import time
import requests
import threading
from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QProgressBar
from version import VERSION
from functools import partial
from constant import STATIC_PATH


class OtaUpgrade:

    def __init__(self, obj_ui, git_url: str):
        """
        :param obj_ui: 主界面 UI读对象
        :param git_url: 仓库地址  ps: https://gitee.com/yypqc/email
        """
        self.obj_ui = obj_ui
        self.git_url = git_url
        self.__str_ver = '----'
        self.__dest = ''
        self.__create = ''
        self.__dit_url = {}

    def get_ver(self):
        """获取软件最新版本
        :return:
        """
        try:
            response = requests.get(f'{self.git_url}/releases/latest')
            response.raise_for_status()
            dit_data = response.json().get('release', {})
            self.__str_ver = dit_data.get('tag', {}).get('name', '----')
            self.__create = dit_data.get('release', {}).get('created_at', '')
            self.__dest = dit_data.get('release', {}).get('description', '')
            lst_url = dit_data.get('release', {}).get('attach_files', [])
            self.__dit_url = lst_url[0] if lst_url else {}
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return

    def set_ver(self):
        """设置软件版本
        :return:
        """

        def __do():
            self.get_ver()
            str_title = f'软件当前版本: {VERSION} 最新版本: {self.__str_ver}'
            self.obj_ui.ver_label.setText(str_title)
            try:
                if self.__str_ver.count('.') == VERSION.count('.') == 3:
                    lst_new_ver = [int(i) for i in self.__str_ver.lower().replace('v', '').split('.')]
                    lst_old_ver = [int(i) for i in VERSION.lower().replace('v', '').split('.')]

                    for index_ in range(4):
                        if lst_new_ver[index_] > lst_old_ver[index_]:
                            self.obj_ui.upd_btu.setText('立即查看')
                            self.obj_ui.upd_btu.setEnabled(True)
                            break
            except Exception as e:
                logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

        threading.Thread(target=__do).start()

    def show_page(self):
        """显示升级信息
        :return:
        """
        try:
            if self.__dit_url:
                dialog = QDialog()  # 自定义一个dialog
                dialog.setWindowTitle('版本更新')
                dialog.setWindowIcon(QIcon(os.path.join(STATIC_PATH, 'images', 'update.png')))
                dialog.resize(600, 400)
                # 垂直布局
                layout = QVBoxLayout()

                label = QLabel("版本描述:", dialog)
                label.setFont(QFont("黑体", 14, QFont.Bold))
                layout.addWidget(label)

                # QTextEdit
                text_edit = QTextEdit(dialog)
                text_edit.setReadOnly(True)
                text_edit.setFixedHeight(300)
                str_info = f'<h2>{self.__str_ver}___<em>{self.__create}</em></h2>'
                str_d = ''
                if self.__dest:
                    for str_dest in self.__dest.replace('<p>', '').replace('</p>', '').split('<br>'):
                        str_d += f'<li style="font-size:14px; margin: 10px;">{str_dest}</li>'
                else:
                    str_info = '<li style="font-size:14px; margin: 10px;">修复一些已知问题</li>'
                str_info = f'{str_info}<ul >{str_d}</ur>'
                text_edit.setHtml(str_info)
                layout.addWidget(text_edit)
                # 添加一个可伸缩空间，使 QTextEdit 控件尽可能填满布局
                layout.addStretch(1)

                # 进度条，默认隐藏
                progress_bar = QProgressBar(dialog)
                progress_bar.setMaximum(100)
                progress_bar.hide()
                progress_bar.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; background-color: #FFFFFF; "
                                           "text-align:center; font-size:20px}")
                layout.addWidget(progress_bar)

                # 按钮
                button_layout = QHBoxLayout()
                skip_button = QPushButton("跳过版本", dialog)
                skip_button.setFixedSize(100, 30)
                skip_button.clicked.connect(dialog.close)
                upgrade_button  = QPushButton("立即升级", dialog)
                upgrade_button .setFixedSize(100, 30)
                upgrade_button .clicked.connect(partial(self.download_page, dialog, progress_bar, upgrade_button))
                button_layout.addWidget(skip_button, alignment=Qt.AlignLeft)
                button_layout.addWidget(upgrade_button , alignment=Qt.AlignRight)

                # 将按钮放到底部
                layout.addStretch(1)
                layout.addLayout(button_layout)

                dialog.setLayout(layout)
                dialog.show()
                if dialog.exec() == QDialog.Accepted:
                    pass
                else:
                    dialog.close()
            else:
                self.obj_ui.show_message('错误', '未获取到最新版本下载地址')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def download_page(self, obj_dialog, obj_bar, obj_btu):
        """下载安装包
        :return:
        """
        try:
            obj_bar.show()
            obj_btu.setDisabled(True)
            for _ in range(1, 101):
                obj_bar.setValue(_)
                time.sleep(0.1)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def install_page(self):
        """安装升级包
        :return:
        """
        pass
