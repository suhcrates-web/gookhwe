### 자동 on off 추가

######  수집하는 부분 ########
import websockets
import asyncio

import time
import binascii, codecs
import mysql.connector
from datetime import date, datetime
from ToolBox import still_10
from database import cursor, db
import json
import traceback
import sys
import re
import requests

def open_and_scroll(xcode, xcgcd, today0):
    # open0 = False
    live_key = "".join(str(date.today()).split("-")) + '_' + str(xcode)
    while True:
        try:
            config = {
                'user': 'root',
                'password': 'donga123123!',
                'host': 'localhost',
                # 'database':'shit',
                'port': '3306'
            }
    
            db = mysql.connector.connect(**config)
            cursor = db.cursor()
    
            cursor.execute(
                f"""
                select xstat, xname from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{date.today()}'
                """
            )
            parcel= cursor.fetchall()
            xstat0 = int(parcel[0][0])
            xname = parcel[0][1]
            # print('here_outside', end='')
            print(f"{xcode}/ {xname} / open:  {xstat0}", flush=True)
            sys.stdout.flush()

            if xstat0 == 1:
    
                cursor.execute(
                    f"""
                    select wss, content from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{date.today()}'
                    """
                )
                wss0, a = cursor.fetchall()[0]
                wss0 = wss0 + '/hls'
                if a == None:
                    a = b''
                blob_scrol = codecs.decode(a, 'utf-8')
                n0 = datetime.now()
                blob_scrol += f"<BR>======================\n <BR> {n0.hour}시 {n0.minute}분 {n0.second}초 시작<BR> \n====================== <BR> \n "

                #말뚝 없으면 말뚝 삽입
                num_list = re.findall(r'(?<=\[)\d+(?=\])', blob_scrol)
                if len(num_list) ==0:
                    blob_scrol += '<span style="visibility: hidden;">[0]</span>'

                # print('here3',end='')
                async def connect(wss0, blob_scrol, xcode):
                    async with websockets.connect(wss0) as websocket:
                        while True:
                            message = await websocket.recv()
                            message = json.loads(message)
                            # print('here1', end='')
                            if message['transcripts'][0][0] != -1:
                                mes0 = message['transcripts'][0][-1]
                                
                                ## 시간 삽입 ##
                                if '-' in mes0:
                                    now0 = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
                                    mes0 = mes0.replace('-', f'\n\n- ({now0})')

                                blob_scrol += ' ' + mes0


                                #### 말뚝 삽입 ######

                                num_list = re.findall(r'(?<=\[)\d+(?=\])', blob_scrol)
                                num_last = num_list[-1]
                                gap = re.search(fr'{num_last}].*',blob_scrol.replace('\n',''))[0].__len__() # 이전 말뚝과의 거리
                                if gap > 5000:
                                    blob_scrol +=  f'<span style="visibility: hidden;">[{str(int(num_last) +1 )}]</span>'

                                config = {
                                            'user': 'root',
                                            'password': 'donga123123!',
                                            'host': 'localhost',
                                            # 'database':'shit',
                                            'port': '3306'
                                        }
    
                                db = mysql.connector.connect(**config)
                                cursor = db.cursor()
                                a = bin(int(binascii.hexlify(blob_scrol.encode('utf-8')), 16))[2:]
                                cursor.execute(
                                    f"""update gookhwe_stuffs.live_list set content = b'{a}' where xcode='{xcode}' and date0= '{date.today()}' """
                                )
                                db.commit()

                                cursor.close()
                                db.close

                                # 말뚝을 박은 후 db에 저장되고 나면 request를 보내서 summary 생성하도록
                                if gap > 5000:
                                    data = {
                                            'key0' : live_key,
                                            'index' : str(int(num_last))
                                    }
                                    requests.post('http://52.79.156.227:8000/create', data=data)
    
                            ####### xstate0 다시 확인하는 부분 ####
                                config = {
                                    'user': 'root',
                                    'password': 'donga123123!',
                                    'host': 'localhost',
                                    'port': '3306'
                                }
                                db = mysql.connector.connect(**config)
                                cursor = db.cursor()
                                cursor.execute(
                                    f"""
                                    select xstat from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{date.today()}'
                                    """
                                )
                                xstat0 = int(cursor.fetchall()[0][0])
    
                                if xstat0 == 0: # 끝났으면
                                    n0 = datetime.now()
                                    print(f"{n0.hour}시 {n0.minute}분 {n0.second}초")
                                    blob_scrol +=f"<BR>======================\n <BR> {n0.hour}시 {n0.minute}분 {n0.second}초 정회<BR> \n====================== <BR> \n "
                                    a = bin(int(binascii.hexlify(blob_scrol.encode('utf-8')), 16))[2:]
                                    config = {
                                        'user': 'root',
                                        'password': 'donga123123!',
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
                                    print('did',end=' ')
                                    cursor.close()
                                    db.close()

                                    # 마지막 부분에 대한 요약을 수행하기 위해 Summary Request 요청
                                    data = {
                                            'key0' : live_key,
                                            'index' : str(int(num_last))
                                    }
                                    requests.post('http://52.79.156.227:8000/create', data=data)

                                    break  # 0으로 바꼈으면 while 깸
                        
                asyncio.run(connect(wss0, blob_scrol, xcode ))
            elif xstat0 == 0:

                    pass
            time.sleep(10)
        except Exception as e:
            print(f'{xcode}  . 사유: {e}', flush=True)
            sys.stdout.flush()

            # traceback.print_exc()

            time.sleep(10)
            if date.today() != today0:
                return 0
