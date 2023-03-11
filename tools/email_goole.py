from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from constant import DRIVER_PATH

# 创建 Chrome 实例
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# 打开谷歌地图
driver.get('https://www.google.com/maps')

# 等待页面加载完成
time.sleep(5)

# 在搜索栏输入关键字
search_box = driver.find_element_by_id('searchboxinput')
search_box.send_keys('餐馆')
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载完成
time.sleep(5)

# 获取搜索结果
search_results = driver.find_elements_by_class_name('section-result-title')

# 打印搜索结果
for result in search_results:
    print(result.text)

# 关闭浏览器
driver.quit()
