from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = 'https://assembly.webcast.go.kr/main/player.asp?xcode=37&xcgcd=DCM000037213980101&'
options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument("disable-gpu")
driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)
driver.get(url)
time.sleep(5)
player_wrap=driver.find_element(By.CLASS_NAME,'player_wrap')
player_box =player_wrap.find_element(By.CLASS_NAME,'player_box ')
video_01=player_box.find_element(By.ID,'video_01')
player_view = video_01.find_element(By.CLASS_NAME,'player_view ')
mediaBox_01=player_view.find_element(By.ID,'mediaBox_01')
YoonVideo_01=mediaBox_01.find_element(By.ID,'YoonVideo_01')
button=YoonVideo_01.find_element(By.TAG_NAME,'button').click()
player_ctrl=video_01.find_element(By.CLASS_NAME,'player_ctrl')
button_list =player_ctrl.find_element(By.TAG_NAME,'ul')
smi_btn=button_list.find_element(By.ID,'smi_btn')
button=smi_btn.find_element(By.TAG_NAME,'a').click()
time.sleep(10)
viewSubtit=smi_btn.find_element(By.ID,'viewSubtit')
time.sleep(3)
while True:
    incont=viewSubtit.find_element(By.CLASS_NAME,'incont')
    temp=incont.find_elements(By.TAG_NAME,'p')
    for i in temp:
        print(i.text)
    time.sleep(5)