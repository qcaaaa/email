# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : otaupgrade.py

@Email: yypqcaa@163.com

@Date : 2023/4/17 20:37

@Desc :
"""

import requests
import threading
from loguru import logger
from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QLabel
from version import VERSION


class OtaUpgrade:

    def __init__(self, obj_ui, git_url: str):
        """
        :param obj_ui: 主界面 UI读对象
        :param git_url: 仓库地址  ps: https://gitee.com/yypqc/email
        """
        self.obj_ui = obj_ui
        self.git_url = git_url
        self.__str_ver = '----'
        self.__title = ''
        self.__dest = ''
        self.__create = ''
        self.__url = {}

    def get_ver(self):
        """获取软件最新版本
        :return:
        """
        try:
            response = requests.get(f'{self.git_url}/releases/latest')
            response.raise_for_status()
            dit_data = response.json().get('release', {})
            self.__str_ver = dit_data.get('tag', {}).get('name', '----').lower().replace('v', '')
            self.__title = dit_data.get('release', {}).get('title', '')
            self.__create = dit_data.get('release', {}).get('created_at', '')
            self.__dest = dit_data.get('release', {}).get('description', '')
            lst_url = dit_data.get('release', {}).get('attach_files', [])
            self.__url = lst_url[0] if lst_url else {}
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
                    lst_new_ver, lst_old_ver = [int(i) for i in self.__str_ver.split('.')], [int(i) for i in VERSION.split('.')]

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
