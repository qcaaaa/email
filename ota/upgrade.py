#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 20:53
# @Author  : Qc
# @File    : upgrade.py
# @Software: PyCharm
import os.path
import sys
import tempfile

import psutil
import shutil
import subprocess
import win32api
import win32con


def close_program(name):
    """关闭软件"""
    for proc in psutil.process_iter():
        try:
            # 检查进程名称是否匹配
            if proc.name() == name:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def install(name: str, file_path: str, str_db: str):
    """安装软件"""
    close_program(name)
    # 安装程序路径
    # 创建启动信息对象
    if os.path.isfile(file_path):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # 执行安装程序
        subprocess.call(['cmd.exe', '/C', file_path], startupinfo=si)

        # 删除安装包, 删除升级后生成的db
        for str_f in [file_path, str_db]:
            try:
                if os.path.isfile(str_f):
                    os.remove(str_f)
            except:
                pass

    else:
        win32api.MessageBox(0, '升级文件丢失', '错误', win32con.MB_ICONWARNING)


if __name__ == '__main__':
    lst_args = sys.argv
    if len(lst_args) >= 4:
        install(lst_args[1], lst_args[2], lst_args[3])
    else:
        win32api.MessageBox(0, '升级失败', '错误', win32con.MB_ICONWARNING)
