from exp18 import open_and_scroll
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def do():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
    driver.get("http://testbot.ddns.net:5234/donga/dangbun/")
a=1
while a==1:
    do()
    time.sleep(3)
    a = input("shit here")