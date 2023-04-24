from giveme_live_list_v2 import giveme_live_list
from live_list_start import live_list_start
import time




live_list_start()


while True:

    try:
        print('live_list')
        giveme_live_list()


    except Exception as e:
        print(e)
    time.sleep(10)

