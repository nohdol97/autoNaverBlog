from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip as pp
import time
from random import uniform, randrange, shuffle

#좋아요 누른 개수, 다음 태그로 넘어가는 개수
clickedLikeNum : int = 0
stopTagNum : int = 0

# 원하는 태그 목록
# searchWords : list = ["원하는","태그","입력"]

# 태그 순서 섞기
# shuffle(searchWords)

# 각 태그당 좋아요를 누를 최소, 최대 개수
# tagMinNum : int = 40
# tagMaxNum : int = 60

def inputkeys(driver, someWord : str, placeholder : str):
    pp.copy(someWord)
    holderInput = driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
    holderInput.click()
    pp.copy(someWord)
    time.sleep(uniform(1.0, 5.0))
    
    # 윈도우 환경에서 붙여넣기
    holderInput.send_keys(Keys.CONTROL, 'v')
    
    # 맥 환경에서 붙여넣기
    # holderInput.send_keys(Keys.COMMAND, 'v')
    
def login(driver, naverid : str, naverpassword : str):
    fail_login = False
    for i in range(2):
        if i == 1 and fail_login == False:
            break
        driver.get("https://nid.naver.com/nidlogin.login?svctype=262144&url=http://m.naver.com/aside/")    
        inputkeys(driver, naverid, "아이디")
        inputkeys(driver, naverpassword, "비밀번호")
        driver.find_element(By.XPATH, f"//input[@placeholder='비밀번호']").send_keys(Keys.ENTER)
        time.sleep(2)
        fail_login = failLogin(driver)

def failLogin(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="error_message"]')
        return True
    except:
        return False

def scrollEndPosition(driver):
    document_height = int(driver.execute_script("return document.body.scrollHeight"))
    now_scroll_height = int(driver.execute_script("return window.scrollY + window.innerHeight"))
    if now_scroll_height >= (document_height*9/10):
        return False
    else : 
        return True
    
def searchBlog(driver, searchWord : str, articleLimit : int):
    adress = "https://m.search.naver.com/search.naver?where=m_blog&query="+searchWord+"&nso=so%3Add%2Cp%3Aall"
    driver.get(adress)
    driver.implicitly_wait(5)
    articles = driver.find_elements(By.XPATH, "//div[@class='title_area']/a")
    numOfArticles = len(articles)
    SCROLL_PAUSE_TIME = 1
    while numOfArticles < articleLimit :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        articles = driver.find_elements(By.XPATH, "//div[@class='title_area']/a")
        numOfArticles = len(driver.find_elements(By.XPATH, "//div[@class='title_area']/a"))
    
    articles = driver.find_elements(By.XPATH, "//div[@class='title_area']/a")
    numOfArticles = len(articles)
    urls = []
    for i in range(numOfArticles):
        url = str(articles[i].get_attribute("href"))
        urls.append(url)
    return urls

def openBlog(driver, url):
    driver.execute_script(f"window.open('{url}');")
    driver.switch_to.window(driver.window_handles[1])

def closeBlog(driver):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def availableLike(driver):
    global stopTagNum
    try : 
        confirmlike = driver.find_element(By.XPATH, "//*[@id='body']/div[10]/div/div[1]/div/div/a").get_attribute("class").split(" ")
        if "on" in confirmlike :
            stopTagNum += 1
            print(f'이미 좋아요 누른 게시물 {stopTagNum}개')
            return False
        elif "off" in confirmlike : 
            return True
    except Exception as e: 
        print(e)
        print('좋아요가 제한된 게시물')
        return False
    
def clickLike(driver, scrollMinPauseTime, scrollMaxPauseTime):
    while scrollEndPosition(driver):
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        time.sleep(uniform(scrollMinPauseTime, scrollMaxPauseTime))
    
    like_btn = driver.find_element(By.XPATH, "//div[@class='btn_like']/div")
    driver.execute_script("arguments[0].scrollIntoView({block : 'center'});", like_btn)
    like_btn.click()
    global clickedLikeNum
    clickedLikeNum += 1
    print(f"블로그 좋아요를 {clickedLikeNum}개 누름")
    # closeBlog()
    
def neighborNewFeed(driver, maxnum : int):
    driver.get("https://m.blog.naver.com/FeedList.naver")
    time.sleep(uniform(3, 7))
    cancelNotification(driver)
    unliked_blog_xpath ='''//*[@id="root"]/div[1]/div[2]/div[2]/ul//a[contains(@class, 'u_likeit_list_btn _button off')]/ancestor::div[5]//div[@class ='text_area__mOuKZ']//a'''
    neighborBlogs = driver.find_elements(By.XPATH, unliked_blog_xpath)   
    numOfneighborblogs = len(neighborBlogs)
    SCROLL_PAUSE_TIME = 1
    while numOfneighborblogs < maxnum :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        neighborBlogs = driver.find_elements(By.XPATH, unliked_blog_xpath)
        numOfneighborblogs = len(neighborBlogs)
        if scrollEndPosition(driver) == False:
            break
    print(numOfneighborblogs)
    neighborUrls = []
    for neighborBlog in neighborBlogs:
        neighborUrls.append(neighborBlog.get_attribute('href'))
    return neighborUrls

def cancelNotification(driver):
    try:
        link_xpath2 = '//*[@id="root"]/div[1]/div[2]/div/div[2]/div/div[2]/a[1]/span'
        link_element2 = driver.find_element(By.XPATH, link_xpath2)
        link_element2.click()
        driver.get("https://m.blog.naver.com/FeedList.naver")
        time.sleep(uniform(3, 7))
    except:
        pass
    try:
        time.sleep(1)
        link_xpath1 = '//*[@id="root"]/div[1]/div[2]/div/div[2]/div/div[2]/a[2]/span'
        link_element1 = driver.find_element(By.XPATH, link_xpath1)
        link_element1.click()
        driver.get("https://m.blog.naver.com/FeedList.naver")
        time.sleep(uniform(3, 7))
    except:
        pass

# # 설정한 태그 공감 누르기
# for searchWord in searchWords :
#     urls = searchBlog(searchWord, randrange(tagMinNum, tagMaxNum))
#     for url in urls:
#         openBlog(url)
#         # 블로그 페이지 로딩을 위한 시간
#         time.sleep(uniform(3.0, 7.0))
        
#        # 좋아요가 클릭 가능한지 확인 후 클릭, 아니면 창 닫기 
#         if availableLike() :
#             clickLike()
#         else : 
#             closeBlog()