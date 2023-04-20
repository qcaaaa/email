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
import tempfile
import requests
import threading
from loguru import logger
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QProgressBar, QMessageBox
from functools import partial
from constant import STATIC_PATH


class OtaUpgrade:

    def __init__(self, obj_ui, git_url: str, str_ver: str, str_exe: str = ''):
        """
        :param obj_ui: 主界面 UI读对象
        :param git_url: 仓库地址  ps: https://gitee.com/yypqc/email
        :param str_ver: 当前版本
        :param str_exe: 打包软件名称
        """
        self.obj_ui = obj_ui
        self.git_url = git_url
        self.exe_name = str_exe
        self.str_ver = str_ver
        self.__str_ver = '----'
        self.__dest = ''
        self.__create = ''
        self.__url = ''
        self.progress_bar = None

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
            for dit_url in lst_url:
                if self.exe_name and dit_url.get('name') == self.exe_name:
                    self.__url = dit_url.get('download_url', '')
                    break
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        return

    def set_ver(self):
        """设置软件版本
        :return:
        """

        def __do():
            self.get_ver()
            str_title = f'软件当前版本: {self.str_ver} 最新版本: {self.__str_ver}'
            self.obj_ui.ver_label.setText(str_title)
            try:
                if self.__str_ver.count('.') == self.str_ver.count('.') == 3:
                    lst_new_ver = [int(i) for i in self.__str_ver.lower().replace('v', '').split('.')]
                    lst_old_ver = [int(i) for i in self.str_ver.lower().replace('v', '').split('.')]

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
            if self.__url:
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
                text_edit.setFixedHeight(250)
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
                self.progress_bar = QProgressBar(dialog)
                self.progress_bar.setMaximum(100)
                self.progress_bar.hide()
                self.progress_bar.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; "
                                                "background-color: #FFFFFF; text-align:center; font-size:20px}")
                layout.addWidget(self.progress_bar)

                # 按钮
                button_layout = QHBoxLayout()
                skip_button = QPushButton("跳过版本", dialog)
                skip_button.setFixedSize(100, 30)
                skip_button.clicked.connect(dialog.close)
                upgrade_button = QPushButton("立即升级", dialog)
                upgrade_button.setFixedSize(100, 30)
                upgrade_button.clicked.connect(partial(self.download_page, dialog, upgrade_button, skip_button))
                button_layout.addWidget(skip_button, alignment=Qt.AlignLeft)
                button_layout.addWidget(upgrade_button, alignment=Qt.AlignRight)
                # 将按钮放到底部
                layout.addStretch(1)
                layout.addLayout(button_layout)

                dialog.setLayout(layout)
                dialog.exec_()
            else:
                self.obj_ui.show_message('错误', '未获取到最新版本下载地址')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def download_page(self, obj_dialog, load_btu, skip_btu):
        """下载安装包
        :return:
        """
        try:
            self.progress_bar.show()
            _, tmp_file = tempfile.mkstemp(suffix='.exe')
            thread = Worker(obj_dialog, self.__url, tmp_file)
            thread.progress.connect(self.__set_progress)
            thread.finished.connect(partial(self.install_page, obj_dialog, tmp_file))
            thread.start()
            load_btu.setDisabled(True)
            skip_btu.setDisabled(True)
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def __set_progress(self, value):
        """设置进度条"""
        self.progress_bar.setValue(value)

    def install_page(self, obj_dialog, str_file):
        """安装升级包
        :return:
        """
        try:
            msg_box = QMessageBox(obj_dialog)
            msg_box.setWindowTitle('升级')
            msg_box.setText('下载完成是否立即重启升级!')
            yes_button = msg_box.addButton('确认', QMessageBox.YesRole)
            msg_box.addButton('取消', QMessageBox.NoRole)
            msg_box.exec_()
            if msg_box.clickedButton() == yes_button:
                print('升级成功')
            else:
                print('取消升级')
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
        finally:
            if obj_dialog:
                obj_dialog.close()


class Worker(QThread):
    progress = pyqtSignal(int)

    def __init__(self, p, str_url, str_file):
        super(Worker, self).__init__(p)
        self.str_url = str_url
        self.str_file = str_file

    def run(self):
        try:
            url = f'https://gitee.com{self.str_url}'
            response = requests.get(url=url, stream=True)
            response.raise_for_status()
            total_length = int(response.headers.get('content-length'))

            int_length = 0
            with open(self.str_file, 'wb') as f:
                for content in response.iter_content(1024 * 1024):
                    f.write(content)
                    f.flush()
                    int_length += len(content)
                    self.progress.emit(int(int_length / total_length * 100))
        except Exception as e:
            if os.path.isfile(self.str_file):
                os.unlink(self.str_file)
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")
