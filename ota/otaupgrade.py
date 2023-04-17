# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : otaupgrade.py

@Email: yypqcaa@163.com

@Date : 2023/4/17 20:37

@Desc :
"""

import threading
from loguru import logger
from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QLabel
from version import VERSION


class OtaUpgrade:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui

    @staticmethod
    def get_ver() -> str:
        """获取软件最新版本
        :return:
        """
        str_ver = '---'
        return str_ver

    def set_ver(self):
        """设置软件版本
        :return:
        """

        def __do():
            new_ver = self.get_ver()
            str_title = f'软件当前版本: {VERSION} 最新版本: {new_ver}'
            self.obj_ui.ver_label.setText(str_title)
            try:
                if new_ver.count('.') == VERSION.count('.') == 3:
                    self.obj_ui.upd_btu.setText('立即查看')
                    self.obj_ui.upd_btu.setEnabled(True)
            except Exception as e:
                logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

        threading.Thread(target=__do).start()

    def show_page(self):
        """显示升级信息
        :return:
        """
        print("Label clicked!")

    def download_page(self):
        """下载安装包
        :return:
        """

    def install_page(self):
        """安装升级包
        :return:
        """
        pass
