from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#import re
import time

str_page = '1'

def start_crawling():
    contents_list = []
    title_list = []
    int_page = 1
    driver = webdriver.Chrome()    # 현재 폴더에 chromedriver.exe가 있어서 경로 설정X
    driver.get('https://kin.naver.com/search/list.naver?query=여행&page=' + str_page)    # 지식인 페이지에서 검색
    time.sleep(1.5)
    
    while int_page<4:
        contents = driver.find_elements(By.XPATH, '//*[@id="s_content"]/div[3]/ul/li/dl/dt/a')
        
        for idx, c in enumerate(contents):
            time.sleep(1.5)
            c.click()
            time.sleep(1.5)
            driver.switch_to.window(driver.window_handles[-1])
            title = driver.title
            title = title.replace('.', '')
            title_list.append(title.replace(' : 지식iN', '').strip())
            #print(title_list)
            time.sleep(1.5)
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1.5)
        next_button = driver.find_element(By.XPATH, '//*[@id="s_content"]/div[3]/div[2]/a['+str(int_page)+']')    # 다음페이지 버튼 클릭
        int_page += 1
        next_button.click()
        time.sleep(1.5)
    
    save_txt(title_list)
          
def save_txt(title_list):
    txt_file_path = "titles.txt"

    # 텍스트 파일을 쓰기 모드로 열고 내용을 저장
    with open(txt_file_path, mode="w", encoding="UTF-8") as file:
        for title in title_list:
            file.write(title + "\n")

start_crawling()