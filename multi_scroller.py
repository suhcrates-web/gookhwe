import multiprocessing
from multiprocessing import Queue
from open_and_scroll_v5 import open_and_scroll
# from exp22 import open_and_scroll
from database import cursor, db
from datetime import date, datetime, timedelta
import time




def do():
    now0 = datetime.now() - timedelta(hours=4)    # 4시간 땡김
    now0 = now0.date()
    cursor.execute(
        f"""
        select xcode, xcgcd from gookhwe_stuffs.live_list where date0 = '{now0}'
        """
    )

    dics = {xcode:xcgcd for xcode, xcgcd in cursor.fetchall()}






    result_list = multiprocessing.Manager().list()
    processes = []
    for xcode, xcgcd in dics.items():
        p = multiprocessing.Process(target=open_and_scroll, args=(xcode, xcgcd, date.today()))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()



if __name__ == '__main__':
    while True:
        do()

        time.sleep(2)