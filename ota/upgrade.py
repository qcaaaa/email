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


def copy_file(source_file: str, dest_file: str, str_type: str):
    try:
        if str_type == 'copy':
            return shutil.copy(source_file, dest_file)
        else:
            return shutil.move(source_file, dest_file)
    except:
        pass


def install(name: str, file_path: str, str_db: str, str_conf: str):
    """安装软件"""
    close_program(name)
    # 安装程序路径
    # 创建启动信息对象
    if os.path.isfile(file_path):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # 复制文件
        _, tmp_db = tempfile.mkstemp(suffix='.db')
        copy_file(str_db, tmp_db, str_type='copy')
        _, tmp_conf = tempfile.mkstemp(suffix='json')
        copy_file(str_conf, tmp_conf, str_type='copy')

        # 执行安装程序
        subprocess.call(['cmd.exe', '/C', file_path], startupinfo=si)

        # 移动旧数据
        copy_file(tmp_db, str_db, str_type='mv')
        copy_file(tmp_conf, str_conf, str_type='mv')

        # 删除安装包, 删除升级后生成的db
        for str_f in [file_path, tmp_db, tmp_conf]:
            try:
                if os.path.isfile(str_f):
                    os.remove(str_f)
            except:
                pass

    else:
        win32api.MessageBox(0, '升级文件丢失', '错误', win32con.MB_ICONWARNING)


if __name__ == '__main__':
    lst_args = sys.argv
    if len(lst_args) >= 5:
        install(lst_args[1], lst_args[2], lst_args[3], lst_args[4])
    else:
        win32api.MessageBox(0, '升级失败', '错误', win32con.MB_ICONWARNING)
