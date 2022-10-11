######  수집하는 부분 ########

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import binascii, codecs
from ToolBox import still_10
from database import cursor, db



# url = 'https://assembly.webcast.go.kr/main/player.asp?xcode=37&xcgcd=DCM000037213980101&'
# url = 'https://assembly.webcast.go.kr/main/player.asp?xcode=34&xcgcd=DCM000034213980301&'
# url= 'https://assembly.webcast.go.kr/main/player.asp?xcode=58&xcgcd=DCM000058213980201&'
options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument("disable-gpu")
driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
driver.get('https://assembly.webcast.go.kr/main/')
result = 'n'
while result == 'n':
    print("######################################")
    html0 = driver.page_source
    html0 = BeautifulSoup(html0, 'html.parser')
    print(html0)
    result = input(":::::")


