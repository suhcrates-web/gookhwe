######  수집하는 부분 ########

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import binascii, codecs
import mysql.connector
from datetime import date
from ToolBox import still_10
from database import cursor, db


def open_and_scroll(xcode, xcgcd):
    config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        # 'database':'shit',
        'port': '3306'
    }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    cursor.execute(
        f"""
        select content from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{date.today()}'
        """
    )
    a = cursor.fetchall()[0][0]
    if a == None:
        a = b''
    blob_scrol= codecs.decode(a, 'utf-8')
    text_list = blob_scrol.strip().split('\n')

    # url = 'https://assembly.webcast.go.kr/main/player.asp?xcode=37&xcgcd=DCM000037213980101&'
    # url = 'https://assembly.webcast.go.kr/main/player.asp?xcode=34&xcgcd=DCM000034213980301&'
    # url= 'https://assembly.webcast.go.kr/main/player.asp?xcode=HK&xcgcd=DCM0000HK214000301&'
    url= f'https://assembly.webcast.go.kr/main/player.asp?xcode={xcode}&xcgcd={xcgcd}&'
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
    # button=YoonVideo_01.find_element(By.TAG_NAME,'button').click()
    player_ctrl=video_01.find_element(By.CLASS_NAME,'player_ctrl')
    button_list =player_ctrl.find_element(By.TAG_NAME,'ul')
    smi_btn=button_list.find_element(By.ID,'smi_btn')
    button=smi_btn.find_element(By.TAG_NAME,'a').click()
    time.sleep(10)
    viewSubtit=smi_btn.find_element(By.ID,'viewSubtit')
    time.sleep(3)
    while True:
        text_list_10 = text_list[-10:]
        try:
            incont=viewSubtit.find_element(By.CLASS_NAME,'incont')
            temp=incont.find_elements(By.TAG_NAME,'p')
            temp_list = []
            for i in temp:
                temp_text = i.text.strip()
                if temp_text not in text_list_10:
                    text0 = i.text.strip()
                    temp_list.append(text0)
                    blob_scrol += text0+'\n'
            text_list = text_list + temp_list
            # print(text_list)
            print("===================================")
            print(blob_scrol)
            a = bin(int(binascii.hexlify(blob_scrol.encode('utf-8')), 16))[2:]
            config = {
                'user': 'root',
                'password': 'Seoseoseo7!',
                'host': 'localhost',
                # 'database':'shit',
                'port': '3306'
            }

            db = mysql.connector.connect(**config)
            cursor = db.cursor()
            cursor.execute(
                f"""update gookhwe_stuffs.live_list set content = b'{a}' where xcode='{xcode}' and date0= '{date.today()}' """
            )
            db.commit()
            ### 디스플레이하는 부분 #####
            # article = ''
            # for text0 in text_list[10:]:
            #     if text0[0] == '-':
            #         text0 = '\n\n'+text0
            #     article += text0 + ' '
            # print(article)
            print("===================================")

        except Exception as e:
            print(e)
            print("exception *****************************")
            pass





        time.sleep(5)