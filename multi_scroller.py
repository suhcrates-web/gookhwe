import multiprocessing
from multiprocessing import Queue
# from open_and_scroll_new import open_and_scroll
from exp22 import open_and_scroll
from database import cursor, db
from datetime import date
import time



cursor.execute(
    f"""
    select xcode, xcgcd from gookhwe_stuffs.live_list where date0 = '{date.today()}'
    """
)

dics = {xcode:xcgcd for xcode, xcgcd in cursor.fetchall()}





def do():
    result_list = multiprocessing.Manager().list()
    processes = []
    for xcode, xcgcd in dics.items():
        p = multiprocessing.Process(target=open_and_scroll, args=(xcode, xcgcd))
        processes.append(p)
        p.start()




if __name__ == '__main__':
   do()