### 자동 on off 추가

######  수집하는 부분 ########
import websockets
import asyncio

import socketio
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

# pip install "python-socketio<5" # EIO=3를 사용하기 위해 버전을 낮춰야함

async def connect_normal(wss0, blob_scrol, xcode, today0, live_key):
    # Socket.IO 클라이언트 설정
    sio = socketio.AsyncClient(logger=False, engineio_logger=False) # logger=True, engineio_logger=True

    @sio.event
    async def connect():
        print(f'{xcode}: Connected to Socket.IO server')

    # 서버에서 메시지를 보낼 때 사용하는 정확한 이벤트 이름을 지정
    @sio.on(event='receive message', namespace=f'/{xcode}')
    async def on_message(message):
        nonlocal blob_scrol  # blob_scrol을 수정 가능하게 설정
        # print(f"Received message: {message}")
        
        # process_message 함수로 메시지를 처리하고 업데이트된 blob_scrol을 반환
        blob_scrol = await process_message(message, blob_scrol, xcode, today0, live_key)




    @sio.event
    async def connect_error(data):
        print(f"Connection error: {data}")

    @sio.event
    async def disconnect():
        print('Disconnected from Socket.IO server')

    try:
        await sio.connect(
            wss0,
            transports=['websocket'],
            headers={
                'Origin': 'https://assembly.webcast.go.kr',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            },
            socketio_path='/socket.io'
        )
        print("Waiting for messages...")
        await sio.wait()
    except Exception as e:
        print(f"Socket.IO connection error: {e}")
        raise e
    finally:
        await sio.disconnect()

async def process_message(mes0, blob_scrol, xcode, today0, live_key):
    # 메시지에 시간 삽입
    if '-' in mes0:
        now0 = datetime.strftime(datetime.now(), '%y-%m-%d %H:%M:%S')
        mes0 = mes0.replace('-', f'\n\n- ({now0})')

    # blob_scrol에 메시지 추가
    blob_scrol += ' ' + mes0

    # 말뚝 삽입을 위한 거리 계산
    num_list = re.findall(r'(?<=\[)\d+(?=\])', blob_scrol)
    num_last = num_list[-1]
    gap = re.search(fr'{num_last}].*', blob_scrol.replace('\n', ''))[0].__len__()

    # 거리가 5000 이상일 때 말뚝 추가
    if gap > 5000:
        blob_scrol += f'<span style="visibility: hidden;">[{str(int(num_last) + 1)}]</span>'


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
        f"""update gookhwe_stuffs.live_list set content = b'{a}' where xcode='{xcode}' and date0= '{today0}' """
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
        select xstat from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{today0}'
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
            f"""update gookhwe_stuffs.live_list set content = b'{a}' where xcode='{xcode}' and date0= '{today0}' """
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

    print(f"sofar: {blob_scrol}")

    # 업데이트된 blob_scrol 반환
    return blob_scrol

# async def main(wss0, blob_scrol, xcode):
    # await connect_normal(wss0, blob_scrol, xcode)


# def open_and_scroll(xcode,xcgd, today0):
def open_and_scroll():
    xcode='21'
    today0 = date.today()
    live_key = "".join(str(today0).split("-")) + '_' + str(xcode)

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
                select xstat, xname from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{today0}'
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
                    select wss, content from gookhwe_stuffs.live_list where xcode='{xcode}' and date0 = '{today0}'
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


                asyncio.run(connect_normal(wss0, blob_scrol, xcode, today0, live_key))

            elif xstat0 == 0:
                pass
            
            time.sleep(10)
            
        except Exception as e:
            print(f'{xcode}  . 사유: {e}', flush=True)
            sys.stdout.flush()

            # traceback.print_exc()

            time.sleep(10)
            if date.today() != today0:   # 12시 넘어서 exception 나면 종료됨.
                return 0
            
open_and_scroll()