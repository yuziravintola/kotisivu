from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

# 设置ChromeDriver的路径
service = Service('/Applications/chromedriver-mac-arm64/chromedriver')

# 启动Chrome浏览器
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 如果你想让浏览器在后台运行
options.add_argument('--save-page-as-mhtml')  # 保存为MHTML格式

driver = webdriver.Chrome(service=service, options=options)

# 打开网页
driver.get('https://wolt.com/fi/fin/helsinki/restaurant/ravintola-yu-zi')

# 等待页面加载完成
time.sleep(30)  # 根据页面复杂性调整等待时间

# 保存页面为MHTML到 ./cache
if not os.path.exists('./cache'):
    os.makedirs('./cache')

file_path = './cache/saved_page.mhtml'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(driver.page_source)

# 关闭浏览器
driver.quit()

print(f"页面已成功保存为 {file_path}")
