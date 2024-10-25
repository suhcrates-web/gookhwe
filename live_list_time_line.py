from giveme_live_list_v3 import giveme_live_list
from live_list_start import live_list_start
import time
import sys
import traceback
import mysql.connector
from datetime import datetime, timedelta
from database import config

# live_list_start()
error_num=0

# 매일 한 번씩 restart할 때마다 mysql에서 4일 지난 데이터는 삭제하는 명령어를 실행
four_days_ago = datetime.now() - timedelta(days=4)
cutoff_date = four_days_ago.strftime('%Y-%m-%d')
db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute(f"""
DELETE FROM gookhwe_stuffs.summary_list
WHERE live_key IN (SELECT key0 FROM gookhwe_stuffs.live_list WHERE date0 < '{cutoff_date}');
""")
db.commit() # 변경사항 커밋

cursor.execute(
    f"""
    delete
    from gookhwe_stuffs.live_list
    where date0 < '{cutoff_date}'
    """
)
db.commit() # 변경사항 커밋
cursor.close()

db.close()


while True:
    try:
        print('live_list', flush=True)
        sys.stdout.flush()

        giveme_live_list()
        error_num=0

    except Exception as e:
        traceback.print_exc()
        print(e, flush=True)
        error_num +=1
        if error_num > 11:
            exit()

    time.sleep(20)