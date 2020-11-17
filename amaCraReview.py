import requests
import time
import test
#import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def searchCondition():
    #itemName='マフラー'
    itemName='パソコン'
    lang='カタカナ'
    url="https://www.amazon.co.jp/s?k="+itemName+"&s=review-rank&__mk_ja_JP="+lang+"&ref=sr_pg_1"
    print(url)
    return url

def movePage():
    try:
        pageCnt=0
        arr = []
        
        while True:
            nextPageTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.a-pagination>li.a-last')))
            lastPageTag=checkExistElement('ul.a-pagination>li.a-disabled.a-last')
            
            #nextBtn이disabled 10페이지이상 넘어가면 중단
            if lastPageTag | (pageCnt==9):
                print('완료되었습니다.')
                break

            for item in driver.find_elements_by_xpath("//div[@data-asin][@data-component-type]"):
                try:
                    mainItemName=item.find_element(By.CSS_SELECTOR, 'h5.s-line-clamp-1')
                    subItemName=item.find_element(By.CSS_SELECTOR, 'h2.s-line-clamp-2')
                    reviewCntmName=item.find_element(By.CSS_SELECTOR, 'span.a-size-base')
                    price=item.find_element(By.CSS_SELECTOR, 'span.a-price-whole')
                    arr.append([mainItemName.text,subItemName.text,reviewCntmName.text,price.text])
                    #np.append(arr, np.array([mainItemName,subItemName,reviewCntmName,price]))
                    # print(mainItemName.text,'###',subItemName.text,'###',reviewCntmName.text,'###',price.text)
                except NoSuchElementException:
                    pass
                
            pageCnt+=1
            nextPageTag.click()           
    except Exception as ex: # 에러 종류
        print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
    # finally:
    #     driver.quit()

def checkExistElement(elem):
    try:
        driver.find_element(By.CSS_SELECTOR,elem)
    except NoSuchElementException:
        return False
    return True

#Main메서드(스크립트실행:__main__ // import: __모듈명__)
if __name__ == "__main__":
    def init():
        global driver  
        driver = webdriver.Chrome()#크롬 드라이버(chromedriver_path)
        driver.get(searchCondition())#조건을 포함한 브라우저를 실행

        global wait
        wait = WebDriverWait(driver , 10) #10초를 기다린다.

        movePage()#페이지 이동

    # 메인함수실행
    init()
    
