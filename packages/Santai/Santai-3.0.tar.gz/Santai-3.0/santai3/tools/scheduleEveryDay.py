import datetime
import schedule #pip install schedule
import threading
import time
#import mkdir
#mkdir.mkdirA("")

def job1():
    print("I'm working for job1")
    time.sleep(2)
    print("job1:", datetime.datetime.now())


def job2():
    print("I'm working for job2")
    time.sleep(2)
    print("job2:", datetime.datetime.now())


def job1_task():
    threading.Thread(target=job1).start()


def job2_task():
    threading.Thread(target=job2).start()


def run():
    print("I am run")
    schedule.every(10).seconds.do(job1_task)
    schedule.every(10).seconds.do(job2_task)

    while True:
        print("I am run2")
        schedule.run_pending()
        time.sleep(15)

run()