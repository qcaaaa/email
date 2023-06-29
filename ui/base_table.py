#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/27 23:04
# @Author  : Qc
# @File    : base_table.py
# @Software: PyCharm

from loguru import logger
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, QCheckBox, QTableWidgetItem

from constant import DIT_LIST


class BaseTab:

    def __init__(self, table: QTableWidget, table_name: str, parent, page_name: int = -1):
        """
        :param table: 表格对象
        :param table_name: 表格对应的左侧菜单
        :param parent: 表格 的父对象
        :param page_name: 表格显示行数 -1 显示全部数据
        """
        self.table = table
        self.table_name = table_name
        self.page_name = page_name
        self.select_table = set()  # 表头单选框
        self.parent = parent

    def show_table(self, lst_data: list, dit_email: dict):
        """
        :param lst_data: 数据
        :param dit_email: 邮箱类型
        :return: 表头单选按钮
        """
        try:
            self.select_table.clear()
            # 清空表格数据
            self.table.clearContents()
            # 表头
            table_header = DIT_LIST[self.table_name].get('cn', [])
            int_len = len(table_header)

            # 渲染表格数据
            self.table.setColumnCount(int_len)
            if self.page_name == -1:
                self.table.setRowCount(len(lst_data))
            else:
                self.table.setRowCount(len(lst_data) if len(lst_data) <= self.page_name else self.page_name)

            # 表格样式
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 铺满
            self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 前两列自适应
            self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.table.setHorizontalHeaderLabels(table_header)  # 表头
            self.table.horizontalHeader().sectionClicked.connect(self.parent.on_all_checkbox_changed)  # 表头点击事件
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止修改
            self.table.setAlternatingRowColors(True)  # 交替行颜色

            # 表格tip
            if self.parent:
                self.table.installEventFilter(self.parent)
                self.table.setMouseTracking(True)
                self.table.itemEntered.connect(self.parent.enter_item_slot)

            # 填充数据
            en_table_header = DIT_LIST[self.table_name].get('en', [])

            for index_, dit_info in enumerate(lst_data):
                # 创建单选框
                checkbox = QCheckBox()
                checkbox.setObjectName(str(dit_info['id']))
                checkbox.clicked.connect(self.parent.on_checkbox_changed)
                self.table.setCellWidget(index_, 0, checkbox)
                # 设置数据
                for index_j, str_en in enumerate(en_table_header, 1):
                    value = str(dit_info.get(str_en, ''))
                    if str_en == 'str_type' and self.table_name == '账号配置':
                        value = dit_email.get(value, '')
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table.setItem(index_, index_j, item)  # 转换后可插入表格
        except Exception as err_msg:
            logger.error(f"{err_msg.__traceback__.tb_lineno}:--:{err_msg}")
        return