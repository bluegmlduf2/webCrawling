import requests
import time
import test
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from googletrans import Translator #번역
from currency_converter import CurrencyConverter #환율
from urllib import parse #url 디코딩용

def searchCondition():
    #itemName='マフラー'
    #'パソコン'
    global selectCnt

    # translatedWord=translateJap(input('검색어를 입력하세요(please input keyword) => '))
    # selectCnt=int(input('검색할 아이템 수를 입력하세요(please input item count) => '))
    translatedWord=translateJap('광어')
    selectCnt=int('5')

    lang='カタカナ'
    url="https://www.amazon.co.jp/s?k="+translatedWord+"&s=review-rank&__mk_ja_JP="+lang+"&ref=sr_pg_1"
    print('검색(URL) : ',url)
    return url

def movePage():
    try:
        itemCnt=1
        pageCnt=1
        arr = []

        while True:
            nextPageTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.a-pagination>li.a-last')))
            lastPageTag=checkExistElement(driver,'ul.a-pagination>li.a-disabled.a-last')[0]
            
            #nextBtn이disabled ２페이지까지 출력
            if lastPageTag | (pageCnt>2):
                print('검색이 완료되었습니다(searching complete)')
                return arr
            
            for item in driver.find_elements_by_xpath("//div[@data-asin][@data-component-type]"):
                brandName=checkExistElement(item,'h5')[0]==True and checkExistElement(item,'h5')[1].text or '없음'
                itemName=checkExistElement(item,'h2')[0]==True and checkExistElement(item,'h2')[1].text or '없음'
                reviewCnt=checkExistElement(item,'span.a-size-base')[0]==True and int(checkExistElement(item,'span.a-size-base')[1].text) or '없음'
                price=checkExistElement(item,'span.a-price-whole')[0]==True and convCurrency(checkExistElement(item,'span.a-price-whole')[1].text) or '0'
                itemUrl=checkExistElement(item,'h2')[0]==True and parse.unquote(checkExistElement(item,'h2>a')[1].get_attribute("href")) or '없음'

                arr.append([itemCnt,brandName,itemName,reviewCnt,price,itemUrl])
                #print(itemCnt,"번째아이템","브랜드명:",brandName,"아이템명:",itemName,"리뷰수:",reviewCnt,"가격:",price)
                itemCnt+=1

                if itemCnt>selectCnt:
                    print('검색이 완료되었습니다(searching complete)')
                    return arr

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

def translateJap(searchWord):
    trans = Translator()

    while True:
        try:
            text = trans.translate(searchWord, dest="ja").text
            print('번역한 검색어 (translated keyword) : ',text)
            return text
        except Exception:
            trans = Translator()

def convCurrency(japYen):
    try:
        #curCov.currencies지원통화확인
        return int(curCov.convert(japYen[1:].replace(',',''),'JPY','KRW'))
    except Exception as ex: # 에러 종류
        print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름

def getSortedArr(arr):
    #평가는 많고 가격은 낮은것
    #arr[itemCnt,brandName,itemName,reviewCnt,price]
    arr.sort(key = lambda x: [-x[3],x[4]])
    return arr

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

            global curCov
            curCov = CurrencyConverter()#통화 인스턴스 초기화

            print('프로그램을 시작합니다(Start Application)')
            arr=movePage()#페이지 이동
            arrSorted=getSortedArr(arr)#정렬된 리스트 가져오기
            print(arrSorted)
        except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
        finally:
            print('프로그램 종료(Exits application)')
            time.sleep(60)
            #driver.quit()



#######시작함수#######
init()


    
