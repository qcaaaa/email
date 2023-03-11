# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : constant.py

@Email: yypqcaa@163.com

@Date : 2022/8/22 10:05

@Desc :
"""
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

LOG_PATH = os.path.join(BASE_PATH, 'log')

EMAIL_CHECK_PATH = os.path.join(BASE_PATH, 'email_check')

STATIC_PATH = os.path.join(BASE_PATH, 'static')

CONFIG_PATH = os.path.join(BASE_PATH, 'config')

DB_PATH = os.path.join(BASE_PATH, 'sql')

DRIVER_PATH = os.path.join(BASE_PATH, 'driver', 'chromedriver.exe')

# 表格行数,数据库一次查询数量
INT_LIMIT = 22

# 表格字体大小
FONT_SIZE = 9

# 表格字体高度
FONT_WEIGHT = 73

# 表格头
DIT_LIST = {
    '账号配置': ['编号', '账号', '授权码', '邮箱类型', '操作'],
    '邮件模板': ['编号', '邮件标题', '邮件正文', '操作'],
    '邮件附件': ['编号', '附件地址', '操作'],
    '邮件结尾': ['编号', '名称', '结尾内容', '结尾图片', '操作'],
}

# 表格对应的数据库

DIT_DATABASE = {
    '账号配置': 'user',
    '邮件模板': 'template',
    '邮件附件': 'info',
    '邮件结尾': 'end'
}

# 第一个菜单栏

FIRST_TAB = list(DIT_LIST.keys())[0]

