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
    #'パソコン'
    itemName=input('검색어를 입력하세요..')
    lang='カタカナ'
    url="https://www.amazon.co.jp/s?k="+itemName+"&s=review-rank&__mk_ja_JP="+lang+"&ref=sr_pg_1"
    print('검색할 URL...',url)
    return url

def movePage():
    try:
        itemCnt=1
        pageCnt=0
        arr = []
        
        while True:
            nextPageTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.a-pagination>li.a-last')))
            lastPageTag=checkExistElement(driver,'ul.a-pagination>li.a-disabled.a-last')[0]
            
            #nextBtn이disabled 3페이지이상 넘어가면 중단
            if lastPageTag | (pageCnt==2):
                print('완료되었습니다.')
                break

            for item in driver.find_elements_by_xpath("//div[@data-asin][@data-component-type]"):
                itemCnt+=1
                brandName=checkExistElement(item,'h5')[0]==True and checkExistElement(item,'h5')[1].text or '없음'
                itemName=checkExistElement(item,'h2')[0]==True and checkExistElement(item,'h2')[1].text or '없음'
                reviewCnt=checkExistElement(item,'span.a-size-base')[0]==True and checkExistElement(item,'span.a-size-base')[1].text or '없음'
                price=checkExistElement(item,'span.a-price-whole')[0]==True and checkExistElement(item,'span.a-price-whole')[1].text or '없음'

                arr.append([brandName,itemName,reviewCnt,price])
                #np.append(arr, np.array([mainItemName,subItemName,reviewCntmName,price]))
                print(itemCnt,"번째아이템","브랜드명:",brandName,"아이템명:",itemName,"리뷰수:",reviewCnt,"가격:",price)

            pageCnt+=1
            nextPageTag.click()           
    except Exception as ex: # 에러 종류
        print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
    # finally:
    #     driver.quit()

def checkExistElement(item,selector):
    try:
        reVal=item.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return [False]
    return [True,reVal]

#Main메서드(스크립트실행:__main__ // import: __모듈명__)
if __name__ == "__main__":
    def init():
        try:
            url=searchCondition()
            
            global driver  
            driver = webdriver.Chrome()#크롬 드라이버(chromedriver_path)
            driver.get(url)#조건을 포함한 브라우저를 실행

            global wait
            wait = WebDriverWait(driver , 10) #10초를 기다린다.

            print('프로그램을 시작합니다.')
            movePage()#페이지 이동
        except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
        finally:
            driver.quit()


    # 메인함수실행
    init()
    
