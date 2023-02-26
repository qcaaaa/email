# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : constant.py

@Email: yypqcaa@163.com

@Date : 2022/8/22 10:05

@Desc :
"""

# 表格行数,数据库一次查询数量
INT_LIMIT = 40

# 表格字体大小
FONT_SIZE = 9

# 表格字体高度
FONT_WEIGHT = 73

# 表格头
DIT_LIST = {
    '账号配置': ['', '账号', '授权码', '邮箱类型'],
    '邮件模板': ['', '邮件标题', '邮件正文'],
    '邮件附件': ['', '附件地址'],
    '邮件结尾': ['', '名称', '结尾内容', '结尾图片'],
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

