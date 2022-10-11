import multiprocessing
from multiprocessing import Queue
import time

def do_something(seconds, result):
    print(f'Sleeping {seconds} second...')
    time.sleep(seconds)
    result.append(seconds)
    print(f'Done Sleeping {seconds}')


def do():
    result_list = multiprocessing.Manager().list()
    processes = []
    for t in [1,4,10,3,2]:
        p = multiprocessing.Process(target=do_something, args=(t, result_list)) ## target function의 arg는 이런식으로 넣는 것.
        processes.append(p)
        p.start()


    print('here')

    for pro in processes:
        pro.join()
    print(result_list)

if __name__ == '__main__':
   do()