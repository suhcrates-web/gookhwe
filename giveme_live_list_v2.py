import requests
import json
import mysql.connector
from bs4 import BeautifulSoup
from database import cursor, db
from datetime import date
import re
from ToolBox import gimme_wss

def giveme_live_list():
    config = {
        'user': 'root',
        'password': 'Seoseoseo7!',
        'host': 'localhost',
        # 'database':'shit',
        'port': '3306'
    }

    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    url = "https://assembly.webcast.go.kr/main/service/live_list.asp"
    response = requests.get(url)
    contents=response.text
    json_data=json.loads(contents)['xlist']

    # print(json_data)
    dics={}
    for coun in json_data:
        xcode = coun['xcode']  #25
        xcgcd = coun['xcgcd']  #DCM000025213990101',
        xname = coun['xname']   #정무위
        xsubj = coun['xsubj']   # '제399회 국회(임시회) 제01차 법제사법위원회 [10:00]',
        xsami = coun['xsami']   #(자막)
        xdesc = coun['xdesc']  #개의 / 생중계 없음
        xstat = coun['xstat']  # 1 : 진행중, 0 : 휴
        xthmb = coun['xthmb']  # //thumb.webcast.go.kr/api/thumbnail/bokji : 이런식임. 마지막 단어가 smi 링크에 쓰임

        
        if xcgcd != '' and xsami == '1':
            if xthmb != '':
                name0 = re.search(r'(?<=/)[^/]+$',xthmb)[0]
                # print(xname)
                # print(xsubj)
                url = f'https://assembly.webcast.go.kr/main/player.asp?xcode={xcode}&xcgcd={xcgcd}&'

                wss = gimme_wss(xcode, xcgcd) # 이게 더 정확
                # wss = f'wss://smiai.webcast.go.kr:8091/aistt/{name0}/hls'
                
                # print(url)
                # temp = requests.get(url)
                # temp = BeautifulSoup(temp.content, 'html.parser')
                # print(temp)

                today0 = date.today()
                cursor.execute(
                    f"""
                    insert into gookhwe_stuffs.live_list values("{today0}","{today0.strftime('%Y%m%d')}_{xcode}","{xcode}","{xstat}","{xname}","{xdesc}","{xcgcd}","{xsubj}","{xthmb}","{wss}", NULL)
                    on duplicate key update
                    xstat = "{xstat}",
                    xname = "{xname}",
                    xdesc = "{xdesc}",
                    xsubj = "{xsubj}",
                    xthmb = "{xthmb}",
                    wss = "{wss}"
                    """
                )
                dics[xcode] ={'url':url, 'xname':xname, 'xsubj':xsubj, 'xthmb':xthmb, 'wss':wss}
    db.commit()
    return dics
