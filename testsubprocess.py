from multiprocessing import Process
from time import sleep

def printsec():
    cnt = 0
    p = Process(target=printsecp5)
    p.start()
    while True:
        print(cnt)
        sleep(1)
        cnt += 1
        
        if cnt > 5:
            break


def printsecp5():
    cnt = 0
    while True:
        print("\t"+str(cnt))
        sleep(0.2)
        cnt += 1
        if cnt > 10:
            cnt = 0
            continue


if __name__=="__main__":
    printsec()
