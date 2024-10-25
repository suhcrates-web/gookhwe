import multiprocessing
import time

start= time.perf_counter()
print(__name__)
def time_count(t):
    time.sleep(t)
    return(t)

# p1 = multiprocessing.Process(target=upbit_jusik_corr_calculator, args=(from_when, end_when, 'val','num', 'same'))

if __name__ == '__main__':
    # p = multiprocessing.Process(target=time_count)
    # p2 = multiprocessing.Process(target=time_count)
    # p.start()
    # p2.start()
    processes = []
    for t in [1,4,2,3,5]:
        p = multiprocessing.Process(target=time_count,args=[t])
        p.start()
        processes.append(p)
    for process in processes:
        print(process.value)
        a = process.join()
        print(process)
        print(a)