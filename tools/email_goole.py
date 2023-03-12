import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from constant import DRIVER_PATH

# 创建 Chrome 实例
driver = webdriver.Chrome(service=Service(DRIVER_PATH))

# 全屏
driver.maximize_window()

# 打开谷歌地图
driver.get('https://www.google.com/maps')

# 在搜索栏输入关键字
# 等待页面加载完成
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "searchboxinput"))
)
search_box.send_keys('莫斯科')
search_box.send_keys(Keys.RETURN)

# 点击附近按钮
button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '附近')]"))
)
button.click()

time.sleep(5)

# 在搜索栏输入关键字
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'searchboxinput'))
)
search_box.send_keys('трактор')
search_box.send_keys(Keys.RETURN)

time.sleep(10)

# 获取所有搜索的 超链接
a_tags = driver.find_elements(By.CLASS_NAME, 'hfpxzc')

for a_tag in a_tags:
    str_url = a_tag.get_attribute('href')
    # 根据链接 开启新窗口
    driver.execute_script(f"window.open('{str_url}', '_blank')")
    # 切换到新窗口
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)
    # 获取公司名字
    h1 = driver.find_element(By.TAG_NAME, 'h1')
    snap_list = h1.find_elements(By.CSS_SELECTOR, 'span')
    second_snap_value = snap_list[1].text
    print(second_snap_value)
    # 获取地址1
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "// *[ @ data-item-id='address']"))
        )
    except:
        pass
    else:
        print(element.get_attribute('aria-label'))
    # 获取地址2
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "// *[ @ data-item-id='laddress']"))
        )
    except:
        pass
    else:
        print(element.get_attribute('aria-label'))
    try:
        # 获取网站
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "// *[ @ data-tooltip='打开网站']"))
        )
    except:
        pass
    else:
        print(element.get_attribute('aria-label'))
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "// *[ @ data-tooltip='复制电话号码']"))
        )
    except:
        pass
    else:
        print(element.get_attribute('aria-label'))
    # 关闭新窗口
    driver.close()
    # 切换回原来的窗口
    driver.switch_to.window(driver.window_handles[0])

# 关闭浏览器
driver.quit()
