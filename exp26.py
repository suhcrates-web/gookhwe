import websockets
import asyncio
import json
import mysql
import binascii
from datetime import date, datetime
xcode = 33
blob_scrol=''
wss0 = 'wss://smiai.webcast.go.kr:8091/aistt/bokji/hls'
async def connect(wss0, blob_scrol, xcode):
    async with websockets.connect(wss0) as websocket:
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            if message['final'] == True:
                blob_scrol += ' ' + message['transcript'].replace('-','\n\n-')
                print(message['transcript'].replace('-','\n\n-'), end=' ')

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

                # print(f'작업중 {xstat0}')

                if xstat0 == 0:
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
                    break  # 0으로 바꼈으면 while 깸
        
asyncio.run(connect(wss0, blob_scrol, xcode ))