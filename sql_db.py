# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : sql_db.py

@Email: yypqcaa@163.com

@Date : 2023/2/26 22:24

@Desc :
"""
import sqlite3
from loguru import logger
from threading import Lock

from constant import INT_LIMIT

conn = sqlite3.connect('data.sql')

LOOK = Lock()


class MySql:

    def __init__(self, str_file: str = './data.db'):
        self.conn = sqlite3.connect(str_file)
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

    def __exec_sql(self, str_type: str, str_sql: str) -> int:
        int_ret = 0
        LOOK.acquire()
        try:
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
            str_sql = f"select * from {table} limit {int_limit} offset {(int_start - 1) * int_limit}"
            self.__exec_sql('select', str_sql)
            lst_ret = self.curr.fetchall()
            if lst_ret:
                str_sql = f"select count(*) as num from {table}"
                self.__exec_sql('select', str_sql)
                int_count = self.curr.fetchone().get('num', 0)
                lst_divmod = divmod(int_count, INT_LIMIT)
                int_mun = lst_divmod[0] + 1 if lst_divmod[-1] > 0 else 0
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

