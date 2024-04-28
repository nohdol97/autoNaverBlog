from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip as pp
import time
from random import uniform, randrange, shuffle
from datetime import date

import action
import comment
import driverInfo
import util
import expiration

# 좋아요를 누르기 전 스크롤을 할 때 스크롤 최소, 최대 시간
scrollMinPauseTime : float = 0.5
scrollMaxPauseTime : float = 1.0

# 이웃 블로그 최대 수(이웃이 많을 경우 스크롤 제한하기)
maxneighbornum = 1000

# 처음 실행
firstRunning = True

def execute(id, pw, execute_max, random_rate, is_secret):
    try:
        driver = driverInfo.setup_chrome_driver()
    except:
        driver = driverInfo.setup_chrome_driver()
    action.login(driver, id, pw)
    urls = action.neighborNewFeed(driver, maxneighbornum)
    cnt = 0
    for url in urls:
        if cnt >= execute_max:
            break
        action.openBlog(driver, url)
        # 블로그 페이지 로딩을 위한 시간
        time.sleep(uniform(1.0, 3.0))
            
        # 좋아요가 클릭 가능한지 확인 후 클릭, 아니면 창 닫기 
        if action.availableLike(driver) :
            cnt = cnt + 1
            action.clickLike(driver, scrollMinPauseTime, scrollMaxPauseTime)
            if(util.random_choice_with_probability(random_rate)):
                comment.leaveComment(driver, is_secret)
            else:
                action.closeBlog(driver) # 종료
        else :
            action.closeBlog(driver)

def time_execute(id, pw, execute_max, execute_hour, random_rate, is_secret):
    hour = 0
    if len(str(execute_hour)) < 2:
        hour = f"0{execute_hour}"
    else:
        hour = str(execute_hour)
    minute = util.getMinute()
    exeTime = f"{hour}:{minute}"
    print(f"작업 시작할 시간: {exeTime}")
    util.wait_until(exeTime)
    execute(id, pw, execute_max, random_rate, is_secret)

def main(id, pw, execute_hour_list, execute_max, random_rate, is_secret):
    global firstRunning
    for execute_hour in execute_hour_list:
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        execute_minute = util.getMinute()
        if firstRunning:
            if current_hour < execute_hour:
                time_execute(id, pw, execute_max, execute_hour, execute_minute, random_rate, is_secret)
            elif current_hour == execute_hour and current_minute > execute_minute and current_minute < 40:
                time_execute(id, pw, execute_max, execute_hour, current_minute + 2, random_rate, is_secret)
            firstRunning = False
        else:
            if execute_hour == execute_hour_list[0]:
                if execute_hour_list[-1] == 23 and execute_hour_list[0] == 0:
                    if current_hour == 0 and current_minute > execute_minute and current_minute < 40:
                        time_execute(id, pw, execute_max, execute_hour, current_minute + 2, random_rate, is_secret)
                    elif current_hour == 0 and current_minute >= 40:
                        continue
                    elif current_hour == 23:
                        time_execute(id, pw, execute_max, execute_hour, execute_minute, random_rate, is_secret)
                else:
                    time_execute(id, pw, execute_max, execute_hour, execute_minute, random_rate, is_secret)
            else:
                if current_hour < execute_hour:
                    time_execute(id, pw, execute_max, execute_hour, execute_minute, random_rate, is_secret)
                elif current_hour == execute_hour and current_minute > int(execute_minute) and current_minute < 40:
                    time_execute(id, pw, execute_max, execute_hour, current_minute + 2, random_rate, is_secret)

def work(id, pw, execute_hour_list, execute_max, random_rate, is_secret):
    driver = driverInfo.setup_chrome_driver()
    action.login(driver, id, pw)
    time.sleep(3)
    checkFailLogin = action.failLogin(driver)
    driver.quit()
    if checkFailLogin:
        print("로그인에 실패하였습니다.\n아이디와 비밀번호를 확인해주세요.")
    else:
        print("블로그 작업을 시작합니다.")
        days = 0
        while True:
            if days == 3:
                comment.name_list.clear()
                days = 0
            days = days + 1
            main(id, pw, execute_hour_list, execute_max, random_rate, is_secret)

def auto(id, pw, execute_hour_list, execute_max, random_rate, is_secret):
    if isinstance(expiration.expiration_date, date):
        if date.today() <= expiration.expiration_date:
            work(id, pw, execute_hour_list, int(execute_max), random_rate, is_secret)
        else:
            print("사용 기간이 만료되었습니다.")
    else:
        work(id, pw, execute_hour_list, int(execute_max), random_rate, is_secret)
