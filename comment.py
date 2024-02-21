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
    comment_list1 = [
        f"재미난 글 감사드립니다 {random_emoticon1} 잘 읽고 가요!! ",
        f"안녕하세요~ 정성스런 글 재미있게 보고 갑니당~{random_emoticon1}\n",
        f"재미난 글 읽고 하트 누르고 갑니당~{random_emoticon1}",
        f"정성스런 글 재미나게 보고 갑니다ㅎㅎ!{random_emoticon1}",
        f"블로그 글 재미있게 보고 갑니다.{random_emoticon1}\n",
        f"정성스럽게 쓰신 글 재미나게 보고 가유!\n{random_emoticon1}",
        f"알찬 정보가 많은 글이네요ㅎㅎ{random_emoticon1}\n",
        f"글이 술술 읽히네요~ 재밌게 보고 가요!!{random_emoticon1}\n",
        f"글이 재미있고 흥미로워요!{random_emoticon1} 즐겁게 보고 가요~ 하트도 누릅니당!",
        f"글이 너무 깔끔하고 잘 정리되어 있네요!!{random_emoticon1} 참고하고 갑니당~"
    ]
    random_emoticon2 = random.choice(emoticon)
    comment_list2 = [
        f"제 블로그도 시간내셔서 한번 들러주세요~\n행복한 {day} 되세요!",
        f"{day} 좋은 하루되세요!",
        f"편안한 하루 되세요!{random_emoticon2}",
        f"행복한 하루 되세요!",
        f"행복한 {day} 되시구, 내일도 화이팅임다!!!",
        f"제 블로그도 시간나시면 한번 들러주세요~~!ㅎ",
        f"제 블로그도 시간나시면 한번 들러주세요!{random_emoticon2} 재밌는 글 많습니다ㅎㅅㅎ",
        f"즐거운 {day} 되세요! 또 방문할게요.",
        f"제 블로그도 한번 구경하러 와주세요. 좋은 글이 많아요~\n{day} 행복하고 즐거운 하루 되세요!",
        f"제 블로그도 한번 살펴봐주세요. 유용한 정보 많아요~ ㅎㅎ\n{day} 편안하고 좋은 하루 되세요!",
    ]
    random_comment = random.choice(comment_list1) + random.choice(comment_list2)
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