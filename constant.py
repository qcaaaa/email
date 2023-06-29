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
from utils.tools import get_qss_style

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

LOG_PATH = os.path.join(BASE_PATH, 'log')

EMAIL_CHECK_PATH = os.path.join(BASE_PATH, 'email_check')

EMAIL_SEARCH_PATH = os.path.join(BASE_PATH, 'email_google')

STATIC_PATH = os.path.join(BASE_PATH, 'static')

CONFIG_PATH = os.path.join(BASE_PATH, 'config')

DB_PATH = os.path.join(BASE_PATH, 'sql')

DRIVER_PATH = os.path.join(BASE_PATH, 'driver', 'chromedriver')

# 采集超时时间
INT_TIMEOUT = 60

# 表格头
DIT_LIST = {
    '账号配置': {'cn': ['全选', '#', '账号', '授权码', '邮箱类型', '产品'], 'en': ['id', 'name', 'pwd', 'str_type', 'language']},
    '邮件标题': {'cn': ['全选', '#', '邮件标题', '产品'], 'en': ['id', 'str_title', 'language']},
    '邮件正文': {'cn': ['全选', '#', '邮件正文', '产品'], 'en': ['id', 'str_body', 'language']},
    '邮件附件': {'cn': ['全选', '#', '附件地址', '产品'], 'en': ['id', 'url', 'language']},
    '邮件结尾': {'cn': ['全选', '#', '名称', '结尾内容', '结尾图片'], 'en': ['id', 'name', 'content', 'url']},
}

# 表格对应的数据库
DIT_DATABASE = {
    '账号配置': 'user',
    '邮件标题': 'title',
    '邮件正文': 'body',
    '邮件附件': 'info',
    '邮件结尾': 'end'
}

# 有过滤的表
FILTER_TABLE = ['info', 'body', 'title']
# 语种表
FILTER_LANG = ['info_lang', 'body_lang', 'title_lang']
# 必须要选择数据的表
MAST_SELECT_TABLE = ['user', 'body', 'title']

# 搜索表头
SEARCH_TITLE = ['城市', '关键字', '类型', '公司名称', '公司地址1', '公司地址2', '公司网站', '公司联系电话']

# 校验表头
CHECK_TITLE = ['邮箱地址', '验证日期', '第一步', '第二步', '第三步', '第四步', '第五步', '第六步', '结果', '有效性概率(%)']

# 项目地址
GIT_URL = 'https://gitee.com/yypqc/email'

# 打包软件名称
EXE_NAME = 'Email.exe'

# qss 样式
QSS_STYLE = get_qss_style()

# dear 字体
DEAR_FONT = ['Times New Roman', '黑体', '楷体', '宋体', '新宋体', '仿宋', '隶书', '方正舒体', '方正姚体']
