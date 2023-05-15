# -*- coding: utf-8 -*-
"""
@Tool : PyCharm

@User : 21407

@File : email_check.py

@Email: yypqcaa@163.com

@Date : 2023/3/13 22:31

@Desc :
"""

import os
import time
import threading
import pyautogui
from loguru import logger
from datetime import datetime
from itertools import product
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from constant import DRIVER_PATH, INT_TIMEOUT, SEARCH_TITLE, EMAIL_SEARCH_PATH


class GoogleTool:

    def __init__(self, obj_ui):

        self.obj_ui = obj_ui
        self.driver = None
        self.wb = None
        self.ws = None
        self.succ = 0

    def google_search(self):
        """谷歌定位搜索
        :return:
        """
        dialog = QDialog(self.obj_ui)  # 自定义一个dialog
        form_layout = QFormLayout(dialog)  # 配置layout
        dialog.setWindowTitle('谷歌定位搜索(一行一个,当前仅支持谷歌浏览器111版本)')
        dialog.resize(500, 100)
        city_input = QLineEdit(self.obj_ui)
        city_input.setStyleSheet("height: 30px")
        form_layout.addRow('定位城市:', city_input)
        key_input = QLineEdit(self.obj_ui)
        form_layout.addRow('关键字:', key_input)
        key_input.setStyleSheet("height: 30px")
        button = QDialogButtonBox(QDialogButtonBox.Ok)
        form_layout.addRow(button)
        button.clicked.connect(dialog.accept)
        dialog.show()
        if dialog.exec() == QDialog.Accepted:
            city = city_input.text().strip()
            keyword = key_input.text().strip()
            if city and keyword:
                self.obj_ui.show_message('提示', f'点击确认,后台开始抓取数据....', f'后台开始抓取数据....')
                threading.Thread(target=self.__search, args=(city, keyword), daemon=True).start()
                self.obj_ui.google_button.setDisabled(True)
            else:
                self.obj_ui.show_message('错误', f'缺少数据,无法搜索')

    def __search(self, city, keyword):
        lst_search = list(product(city.split('\n'), keyword.split('\n')))
        self.obj_ui.show_message('', '', f'本轮一共 {len(lst_search)} 种搜索组合')
        str_file = self.__get_excel()
        for tuple_search in lst_search:
            try:
                self.driver = webdriver.Chrome(service=Service(DRIVER_PATH))
                # 全屏
                self.driver.maximize_window()
                # 打开谷歌地图
                self.driver.get('https://www.google.com/maps')
            except Exception as err_:
                logger.error(f'打开谷歌地图失败: {err_.__traceback__.tb_lineno}: {err_}')
            else:
                self.obj_ui.show_message('', '', f'成功打开谷歌地图')
                str_city, str_key = tuple_search
                try:
                    # 在搜索栏输入关键字
                    # 等待页面加载完成
                    search_box = WebDriverWait(self.driver, INT_TIMEOUT).until(
                        EC.presence_of_element_located((By.ID, "searchboxinput"))
                    )
                    search_box.clear()
                    search_box.send_keys(str_city)
                    search_box.send_keys(Keys.RETURN)
                    self.obj_ui.show_message('', '', f'成功定位至 {str_city}')
                    time.sleep(5)
                    # 点击附近按钮
                    button = WebDriverWait(self.driver, INT_TIMEOUT).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '附近')]"))
                    )
                    button.click()
                    time.sleep(5)
                    # 在搜索栏输入关键字
                    search_box = WebDriverWait(self.driver, INT_TIMEOUT).until(
                        EC.presence_of_element_located((By.ID, 'searchboxinput'))
                    )
                    search_box.send_keys(str_key)
                    search_box.send_keys(Keys.RETURN)
                    self.obj_ui.show_message('', '', f'开始搜索关键字: {str_key}')
                    time.sleep(5)
                    # 滑动 获取全部搜索结果
                    if self.__load(str_key):

                        # 获取所有搜索的 超链接
                        a_tags = WebDriverWait(self.driver, INT_TIMEOUT).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, 'hfpxzc'))
                        )
                        self.obj_ui.show_message('', '', f'开始解析数据')
                        # 同步写入数据
                        if str_file and self.ws and self.wb:
                            self.__check_url(a_tags, str_city, str_key, str_file)
                        else:
                            self.obj_ui.show_message('', '', f'生成搜索结果文件失败')
                except Exception as err:
                    logger.error(f'定位失败: {err.__traceback__.tb_lineno}: {err}')
            finally:
                # 关闭浏览器
                if self.driver:
                    self.driver.quit()
                    self.driver = None
        else:
            self.obj_ui.google_button.setEnabled(True)
            if self.wb:
                self.wb.close()
                self.obj_ui.show_message('', '', f'共搜索出{self.succ}条有效数据')
        return

    def __load(self, str_key):
        element = None
        try:
            tuple_size = pyautogui.size()
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'// *[ @ aria-label="与“{str_key}”相符的搜索结果"]'))
                )
            except:
                self.obj_ui.show_message('', '', f'无法通过页面定位, 开始控制鼠标移动, 请勿移动鼠标...')
                pyautogui.moveTo(90, tuple_size[1] // 2)

            s_time = time.time()

            while time.time() - s_time <= 10 * 60:
                try:
                    # 没有更多结果
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "HlvSq"))
                    )
                except:
                    if not element:
                        pyautogui.scroll(-(tuple_size[0] // 2))
                    else:
                        self.driver.execute_script('arguments[0].style.overflow = "auto";arguments[0].scrollTop = 100000', element)
                    self.obj_ui.show_message('', '', f'搜索更多结果中....')
                    # 三分钟 没有滑动 跳过
                    if time.time() - s_time >= 3 * 60:
                        try:
                            WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, f'// *[ @ aria-label="返回页首"'))
                            )
                        except:
                            self.obj_ui.show_message('', '', f'连续3分钟未滑动页面,结束搜索...')
                            break
                else:
                    self.obj_ui.show_message('', '', f'所有结果搜索完毕')
                    break
        except Exception as err:
            logger.error(f'{err.__traceback__.tb_lineno}: {err}')
            return False
        return True

    def __get(self, sty_type, str_path, str_key) -> str:
        str_info = ''
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((sty_type, str_path))
            )
            str_info = element.get_attribute(str_key)
        except:
            pass
        return str_info

    def __check_url(self, lst_tags, city, keyword, str_file: str):
        index_win = self.driver.window_handles[0]
        # 获取具体信息 加速打开网站
        # 创建ChromeOptions实例
        options = Options()
        # 只加载 html
        options.page_load_strategy = "eager"
        self.driver.options = options
        for a_tag in lst_tags:
            second_snap_value = address1 = address2 = url = phone = str_type = ''
            try:
                self.obj_ui.show_message('', '', f'-' * 20)

                second_snap_value = a_tag.get_attribute('aria-label')
                self.obj_ui.show_message('', '', f'公司名称: {second_snap_value}')

                str_url = a_tag.get_attribute('href')
                # 根据链接 开启新窗口
                self.driver.execute_script(f"window.open('{str_url}', '_blank')")
                # 切换到新窗口
                new_window = self.driver.window_handles[-1]
                if new_window != index_win:
                    self.driver.switch_to.window(new_window)
                else:
                    self.obj_ui.show_message('', '', f'未打开新窗口')

                url = self.__get(By.XPATH, "// *[ @ data-tooltip='打开网站']", "href").strip()
                self.obj_ui.show_message('', '', f'公司网站: {url}')

                if not url:
                    self.obj_ui.show_message('', '', f'未采集到公司网站, 跳过')
                    continue

                address1 = self.__get(By.XPATH, "// *[ @ data-item-id='address']", "aria-label").replace('地址:', '').strip()
                self.obj_ui.show_message('', '', f'公司地址1: {address1}')

                address2 = self.__get(By.XPATH, "// *[ @ data-item-id='laddress']", "aria-label").replace('地址:', '').strip()
                self.obj_ui.show_message('', '', f'公司地址2: {address2}')

                phone = self.__get(By.XPATH, "// *[ @ data-tooltip='复制电话号码']", "aria-label").replace('电话:', '').strip()
                self.obj_ui.show_message('', '', f'公司电话: {phone}')

                try:
                    str_btu = WebDriverWait(self.driver, INT_TIMEOUT).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "DkEaL "))
                    )
                except:
                    str_type = ''
                else:
                    str_type = str_btu.text
                    self.obj_ui.show_message('', '', f'公司类型: {str_type}')

            except Exception as err:
                logger.error(f'解析失败: {err.__traceback__.tb_lineno}: {err}')
            finally:
                if self.driver:
                    # 关闭新窗口
                    if self.driver.current_window_handle != index_win:
                        self.driver.close()
                    self.driver.switch_to.window(index_win)
                if url and any([second_snap_value, address1, address2, phone, str_type]):
                    self.__write_excel([city, keyword, str_type, second_snap_value, address1, address2, url, phone], str_file)
        else:
            self.obj_ui.show_message('', '', f'{city}--{keyword}组合搜索完毕')
        return

    def __get_excel(self) -> str:
        str_file = ''
        try:
            str_file = os.path.join(EMAIL_SEARCH_PATH, f"search_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
            self.wb = Workbook()
            # 默认工作簿
            self.ws = self.wb.active
            # 写入表头
            self.ws.append(SEARCH_TITLE)
            self.wb.save(str_file)
        except Exception as err:
            logger.error(f'生成搜索结果文件失败: {err.__traceback__.tb_lineno}: {err}')
            self.wb = None
            self.ws = None
        return str_file

    def __write_excel(self, lst_data: list, str_file: str):
        try:
            self.ws.append(lst_data)
            self.wb.save(str_file)
            self.succ += 1
        except Exception as err:
            logger.error(f'保存搜索结果失败: {err.__traceback__.tb_lineno}: {err}')
        return
