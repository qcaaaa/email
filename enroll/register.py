#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/18 21:22
# @Author  : Qc
# @File    : register.py
# @Software: PyCharm

import win32api
import win32com.client


class Register:

    def __init__(self, str_key: str):
        """
        :param str_key: 软件唯一key
        """
        self.str_key = str_key

    @staticmethod
    def get_hardware_info():
        # 创建WMI对象
        wmi = win32com.client.GetObject("winmgmts:")

        # 获取处理器信息
        processors = wmi.ExecQuery("SELECT * FROM Win32_Processor")
        print("处理器:")
        for processor in processors:
            print(f"  型号: {processor.Name}")
            print(f"  核心数: {processor.NumberOfCores}")
            print(f"  线程数: {processor.NumberOfLogicalProcessors}")
            print(f"  制造商: {processor.Manufacturer}")
            print(f"  架构: {processor.Architecture}")

        volume_serial_number = win32api.GetVolumeInformation('C:\\')[1]
        print("C盘卷序列号:", volume_serial_number)


if __name__ == '__main__':
    Register('').get_hardware_info()
