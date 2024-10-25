import requests
import json
import mysql.connector
from bs4 import BeautifulSoup
from database import cursor, db
from datetime import date, datetime
import re
from ToolBox import gimme_wss
import time
import traceback


def giveme_live_list():
    config = {
        'user': 'root',
        'password': 'donga123123!',
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
        try:
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

                    today0 = datetime.now()
                    if int(today0.strftime("%H")) >5 :  # 05시 이후.
                        cursor.execute(
                            f"""
                            insert into gookhwe_stuffs.live_list values("{today0}","{today0.strftime('%Y%m%d')}_{xcode}","{xcode}","{xstat}","{xname}","{xdesc}","{xcgcd}","{xsubj}","{xthmb}","{wss}", NULL, NULL)
                            on duplicate key update
                            xstat = "{xstat}",
                            xname = "{xname}",
                            xdesc = "{xdesc}",
                            xsubj = "{xsubj}",
                            xthmb = "{xthmb}",
                            wss = "{wss}"
                            """
                        )
                        db.commit()
                        dics[xcode] ={'url':url, 'xname':xname, 'xsubj':xsubj, 'xthmb':xthmb, 'wss':wss}

                    else :  # 05시 이전
                        # 어제 날짜로 취급.
                        # primar key 가 이미 있는 항목만 업데이트.(새로 추가하지 않음.) -> 이미 있는지 확인하는 절차를 거침.
                        # 제목은 손대지 않고,   xstat,  xdesc   만 고침.

                        temp_today0 = today0 - timedelta(days=1)

                        cursor.execute(f"select 1 from gookhwe_stuffs.live_list where key0='{temp_today0.strftime('%Y%m%d')}_{xcode}'")
                        verify = len(cursor.fetchall()) # 1 : 있음  / 0 : 없음

                        if verify ==0:
                            pass
                        else: # 있음
                            today0
                            cursor.execute(
                            f"""
                            insert into gookhwe_stuffs.live_list values("{today0}","{today0.strftime('%Y%m%d')}_{xcode}","{xcode}","{xstat}","{xname}","{xdesc}","{xcgcd}","{xsubj}","{xthmb}","{wss}", NULL, NULL)
                            on duplicate key update
                            xstat = "{xstat}",
                            xdesc = "{xdesc}",
                            """
                            )
                            db.commit()
        except Exception as e:
            traceback.print_exc()
            print(e, flush=True)

        time.sleep(5)
    db.commit()

    cursor.close()
    db.close()
    return dics
