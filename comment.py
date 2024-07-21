from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip as pp
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

import action
import util

name_dict = {}

day = util.getDay() + "요일"
emoticon = ['🔥','🌈','✨','😀','😃','😄','😁',
            '😆','😊','🙂','😍','🥰','😝','❤️',
            '🩷','🧡','💛','💚','💙','🩵','💗',
            '💖','👍','💫','⭐️','🌟']

def getComment1():
    random_emoticon1 = random.choice(emoticon)
    with open('commentList1.txt', 'r', encoding='utf-8') as file:
        lines1 = file.readlines()
    comment_list1 = [f"{line.strip().replace('{emoticon}', random_emoticon1).replace('{day}', day)}" for line in lines1]
    return random.choice(comment_list1)
def getComment2():
    random_emoticon2 = random.choice(emoticon)
    with open('commentList2.txt', 'r', encoding='utf-8') as file:
        lines2 = file.readlines()
    comment_list2 = [f"{line.strip().replace('{emoticon}', random_emoticon2).replace('{day}', day)}" for line in lines2]
    return random.choice(comment_list2)

def leaveComment(driver, is_secret, is_leaveComment):
    try:
        name = ""
        try:
            name_label_xpath = '//*[@id="ct"]//div[contains(@class, "nickname")]'
            name_label_element = driver.find_element(By.XPATH, name_label_xpath)
            name = name_label_element.text
            print(name)
        except:
            print('nickname label 위치가 바뀌었습니다.')
        if name in name_dict.keys():
            name_dict[name] = name_dict[name] + 1
            action.closeBlog(driver) # 종료
        else:
            name_dict[name] = 1
            time.sleep(1)
            if (is_leaveComment):
                # 댓글 달기로 이동
                try:
                    link_xpath = '//*[@id="ct"]//span[contains(text(), "댓글")]'
                    link_element = driver.find_element(By.XPATH, link_xpath)
                    link_element.click()
                except:
                    print('댓글 위치가 바뀌었습니다.')
                time.sleep(2)
                # 댓글 공간
                comment_label_xpath = '//*[@id="naverComment__write_textarea"]'
                comment_label_element = driver.find_element(By.XPATH, comment_label_xpath)
                # 댓글 작성
                randomValue = random.random()
                actions = ActionChains(driver)
                if randomValue < 1: # 20퍼 확률
                    pp.copy(str(name) + "님 :)")
                    actions.click(comment_label_element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                elif randomValue < 0.4: # 20퍼 확률
                    pp.copy(str(name) + "님~")
                    actions.click(comment_label_element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                elif randomValue < 0.6: # 20퍼 확률
                    pp.copy("안녕하세요! " + str(name) + "님~")
                    actions.click(comment_label_element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                elif randomValue < 0.8: # 20퍼 확률
                    pp.copy(str(name) + "님 :) 오늘도 방문했어요 ㅎㅎ")
                    actions.click(comment_label_element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                actions.send_keys(Keys.ENTER).perform()
                time.sleep(1)
                pp.copy(getComment1())
                actions.click(comment_label_element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                time.sleep(1)
                actions.send_keys(Keys.ENTER).perform()
                pp.copy(getComment2())
                actions.click(comment_label_element).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                time.sleep(2)
                # 비밀글로 할지
                if(is_secret and util.random_choice_with_probability(0.3)):
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