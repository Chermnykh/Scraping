from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo.errors import DuplicateKeyError as dke
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=chrome_options)

url = 'https://www.mvideo.ru'
driver.get(url)

# Search for the necessary item on the page
while True:
    try:
        wait = WebDriverWait(driver, 10)
        button_trend = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'В тренде')]")))
        button_trend.click()
        break
    except:
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()

trends = driver.find_element(By.XPATH, ".//mvid-shelf-group[contains(@class, 'page-carousel-padding ng-star-inserted')]")

# List of prices
title_list = []
titles = trends.find_elements(By.XPATH, ".//div[@class='title']/a/div")
for title in titles:
    title_list.append(title.text)

# List of prices
price_list = []
prices = trends.find_elements(By.XPATH, ".//span[contains(@class, 'price__main-value')]")
for price in prices:
    price_list.append(price.text)

# List ofo links and ids
link_list = []
id_list = []
links = trends.find_elements(By.XPATH, ".//div[@class='title']//*[@href]")
for link in links:
    link_list.append(link.get_attribute('href'))
    id_list.append(int(link.get_attribute('href').split('-')[-1]))

# Join items together
keys = ['_id', 'title', 'price', 'link']
mvideo_items = zip(id_list, title_list, price_list, link_list)
mvideo_trends = [dict(zip(keys, values)) for values in mvideo_items]


# DB
client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_db']
mvideo = db.mvideo

for elem in mvideo_trends:
    try:
        mvideo.insert_one(elem)
    except dke:
        print("Duplicate key error collection")
