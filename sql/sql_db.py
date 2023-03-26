# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : sql_db.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 22:24

@Desc :
"""

import os
import sqlite3
from loguru import logger
from threading import Lock

from constant import INT_LIMIT, DB_PATH

conn = sqlite3.connect('data.sql')

LOOK = Lock()


class MySql:

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DB_PATH, 'data.db'))
        self.conn.row_factory = self.__dict_factory
        self.curr = self.conn.cursor()

    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx] if row[idx] else ''
        return d

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.curr:
                self.curr.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--:{e}")

    def __exec_sql(self, str_type: str, str_sql: str, lst_data: list = None) -> int:
        int_ret = 0
        LOOK.acquire()
        try:
            if lst_data:
                self.curr.execute(str_sql, lst_data)
            else:
                self.curr.execute(str_sql)
            if str_type != 'select':
                self.conn.commit()
                int_ret = 1
        except Exception as e:
            logger.error(f"{e.__traceback__.tb_lineno}:--{e}:{str_sql}")
        finally:
            LOOK.release()
        return int_ret

    def select_sql(self, table: str, int_start: int = 1, int_limit: int = INT_LIMIT) -> dict:
        lst_ret = []
        int_mun = 1
        str_sql = ''
        int_count = 0
        try:
            if int_start != -1:
                str_sql = f"select * from {table} limit {int_limit} offset {(int_start - 1) * int_limit}"
            else:
                str_sql = f"select * from {table}"
            self.__exec_sql('select', str_sql)
            lst_ret = self.curr.fetchall()
            if lst_ret and int_start != -1:
                str_sql = f"select count(*) as num from {table}"
                self.__exec_sql('select', str_sql)
                int_count = self.curr.fetchone().get('num', 0)
                lst_divmod = divmod(int_count, INT_LIMIT)
                int_mun = lst_divmod[0]
                int_mun = lst_divmod[0] + (1 if lst_divmod[-1] > 0 else 0)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--{e}:{str_sql}")
        return {'lst_ret': lst_ret, 'count': int_mun, 'int_count': int_count}

    def del_sql(self, table: str, int_id: int) -> int:
        int_ret = 0
        str_sql = ''
        try:
            str_sql = f"delete from {table} where id={int_id}"
            int_ret = self.__exec_sql('del', str_sql)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--{e}:{str_sql}")
        return int_ret

    def add_sql(self, table: str, lst_info: list) -> int:
        int_ret = 0
        str_sql = ''
        try:
            if table == 'user':
                str_sql = f"insert into {table} (name, pwd, str_type) values (?, ?, ?)"
            elif table == 'template':
                str_sql = f"insert into {table} (title, content, language) values (?, ?, ?)"
            elif table == 'info':
                str_sql = f"insert into {table} (url, language) values (?, ?)"
            elif table == 'end':
                str_sql = f"insert into {table} (name, content, url) values (?, ?, ?)"
            int_ret = self.__exec_sql('add', str_sql, lst_info)
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--{e}:{str_sql}")
        return int_ret

    def get_language(self, str_type: str) -> list:
        lst_ret = []
        str_sql = ''
        try:
            if str_type == 'template':
                str_sql = "select distinct language from template"
            elif str_type == 'info':
                str_sql = "select distinct language from info"
            self.__exec_sql('select', str_sql)
            print(self.curr.fetchall())
        except Exception as e:
            logger.debug(f"{e.__traceback__.tb_lineno}:--{e}:{str_sql}")
        return lst_ret
