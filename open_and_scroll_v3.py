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

def open_and_scroll(xcode, xcgcd):
    open0 = False

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
                select xstat from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{date.today()}'
                """
            )
    
            xstat0 = int(cursor.fetchall()[0][0])
            # print('here_outside', end='')
            print(f"{xcode} /{open0}/  {xstat0}")
            if xstat0 == 1:
                if open0 == True:
                    pass
                elif open0 == False:
                    open0 = True
                    # 열어서 활동 시작
    
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
                # print('here3',end='')
                async def connect(wss0, blob_scrol, xcode):
                    async with websockets.connect(wss0) as websocket:
                        while True:
                            message = await websocket.recv()
                            message = json.loads(message)
                            # print('here1', end='')
                            if message['transcripts'][0][0] != -1:
                            # if message['final'] == True:
                                # print('here2', end='')
                                # print(f'<<<{message}>>>>', end='')
    
                                blob_scrol += ' ' + message['transcript'].replace('-','\n\n-')
                                # print(message['transcript'].replace('-','\n\n-'), end=' ')
    
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
                                    break  # 0으로 바꼈으면 while 깸
                        
                asyncio.run(connect(wss0, blob_scrol, xcode ))
            elif xstat0 == 0:
                if open0 == True:
                    open0 = False
                if open0 == False:
                    pass
            time.sleep(2)
        except:
            print(f'{xcode}   닫혔었음')