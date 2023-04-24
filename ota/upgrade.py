#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 20:53
# @Author  : Qc
# @File    : upgrade.py
# @Software: PyCharm
import os.path
import sys
import psutil
import winreg
import subprocess
import win32api
import win32con


def get_install_path(name: str):
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    key = winreg.OpenKey(registry, key_path)

    install_location = None
    for i in range(winreg.QueryInfoKey(key)[0]):
        subkey_name = winreg.EnumKey(key, i)
        subkey = winreg.OpenKey(key, subkey_name)
        try:
            if name in winreg.QueryValueEx(subkey, "DisplayName")[0]:
                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                break
        except:
            pass
        finally:
            winreg.CloseKey(subkey)

    winreg.CloseKey(key)
    winreg.CloseKey(registry)
    return install_location


def close_program(name):
    """关闭软件"""
    for proc in psutil.process_iter():
        try:
            # 检查进程名称是否匹配
            if proc.name() == name:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def install(name: str, file_path: str):
    """安装软件"""
    close_program(name)
    # install_path = get_install_path(name)
    # 安装程序路径
    # 创建启动信息对象
    if os.path.isfile(file_path):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # 执行安装程序
        subprocess.call(['cmd.exe', '/C', file_path], startupinfo=si)
        try:
            os.remove(file_path)
        except:
            pass
    else:
        win32api.MessageBox(0, '升级文件丢失', '错误', win32con.MB_ICONWARNING)


if __name__ == '__main__':
    lst_args = sys.argv
    if len(lst_args) >= 3:
        install(lst_args[1], lst_args[2])
    else:
        win32api.MessageBox(0, '升级失败', '错误', win32con.MB_ICONWARNING)
