import time
import random

def random_choice_with_probability(probability):
    return random.random() < probability

def getDay():
    now = time.localtime()
    daylist = ['월', '화', '수', '목', '금', '토', '일']
    return daylist[now.tm_wday]

def getMinute():
    random_number = random.randint(2, 30)
    minute = "0"
    if 0 <= random_number <= 9:
        minute = minute + str(random_number)
    else:
        minute = str(random_number)
    return minute

def wait_until(specified_time: str) -> None:
    specified_hour, specified_minute = map(int, specified_time.split(":"))
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == specified_hour and current_time.tm_min >= specified_minute:
            break
        time.sleep(1)