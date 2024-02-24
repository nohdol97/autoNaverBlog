from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip as pp
import time
from random import uniform, randrange, shuffle
import random
import pyperclip

import action
import util

name_list = []

def getComment():
    day = util.getDay() + "요일"
    emoticon = ['🔥','🌈','✨','😀','😃','😄','😁',
                '😆','😊','🙂','😍','🥰','😝','❤️',
                '🩷','🧡','💛','💚','💙','🩵','💗',
                '💖','👍','💫','⭐️','🌟']
    random_emoticon1 = random.choice(emoticon)
    with open('commentList1.txt', 'r', encoding='utf-8') as file:
        lines1 = file.readlines()
    comment_list1 = [f"{line.strip().replace('{emoticon}', random_emoticon1).replace('{day}', day)}" for line in lines1]
    with open('commentList2.txt', 'r', encoding='utf-8') as file:
        lines2 = file.readlines()
    random_emoticon2 = random.choice(emoticon)
    comment_list2 = [f"{line.strip().replace('{emoticon}', random_emoticon2).replace('{day}', day)}" for line in lines2]
    random_comment = random.choice(comment_list1) + "\n" + random.choice(comment_list2)
    return random_comment

def leaveComment(driver):
    try:
        name_label_xpath = '//*[@id="ct"]/div[4]/div[4]/div/a/div[2]/strong'
        name_label_element = driver.find_element(By.XPATH, name_label_xpath)
        name = name_label_element.text
        if name in name_list:
            action.closeBlog(driver) # 종료
        else:
            name_list.append(name)
            time.sleep(1)
            # 댓글 달기로 이동
            link_xpath = "//*[@id='ct']/div[4]/div[3]/div/div[2]/a[1]"
            link_element = driver.find_element(By.XPATH, link_xpath)
            link_element.click()
            time.sleep(2)
            # 댓글 공간
            comment_label_xpath = '//*[@id="naverComment__write_textarea"]'
            comment_label_element = driver.find_element(By.XPATH, comment_label_xpath)
            # 댓글 작성
            randomValue = random.random()
            if randomValue < 0.2: # 20퍼 확률
                pyperclip.copy(str(name) + "님 :)\n" + getComment())
                comment_label_element.send_keys(Keys.CONTROL,'v')
            elif randomValue < 0.4: # 20퍼 확률
                pyperclip.copy(str(name) + "님~\n" + getComment())
                comment_label_element.send_keys(Keys.CONTROL,'v')
            elif randomValue < 0.6: # 20퍼 확률
                pyperclip.copy("안녕하세요! " + str(name) + "님~\n" + getComment())
                comment_label_element.send_keys(Keys.CONTROL,'v')
            elif randomValue < 0.8: # 20퍼 확률
                pyperclip.copy(str(name) + "님 :) 오늘도 방문했어요 ㅎㅎ\n" + getComment())
                comment_label_element.send_keys(Keys.CONTROL,'v')
            else: # 30퍼 확률
                pyperclip.copy(getComment())
                comment_label_element.send_keys(Keys.CONTROL,'v')
            time.sleep(2)
            # 비밀글로 할지
            if(util.random_choice_with_probability(0.3)):
                secret_xpath = '//*[@id="naverComment__write_textarea_secret_check"]'
                secret_element = driver.find_element(By.XPATH, secret_xpath)
                secret_element.click()
                time.sleep(2)
            # 댓글 제출
            subit_xpath = '//*[@id="naverComment"]/div/div[7]/div[1]/form/fieldset/div/div/div[6]/button'
            submit_element = driver.find_element(By.XPATH, subit_xpath)
            submit_element.click()
            time.sleep(2)
            action.closeBlog(driver) # 종료
    except:
        action.closeBlog(driver) # 종료
        pass