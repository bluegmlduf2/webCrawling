import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from googletrans import Translator #번역
from currency_converter import CurrencyConverter #환율
from urllib import parse #url 디코딩용

class amazon:
    def __init__(self,searchList):
        #검색어 초기설정
        url=self.searchCondition(searchList)
        
        global driver  
        driver = webdriver.Chrome('C:\\Users\\YOON\\Desktop\\pythonProj\\webCrawling\\flaskProj\\ama\\chromedriver.exe')#크롬 드라이버(chromedriver_path)
        driver.get(url)#조건을 포함한 브라우저를 실행

        global wait
        wait = WebDriverWait(driver , 10) #10초를 기다린다.

        global curCov
        curCov = CurrencyConverter()#통화 인스턴스 초기화

    def searchCondition(self,searchList):
        global selectCnt
        global currency
        global language
        global trans
        trans = Translator()
        
        keyword=searchList['keyword']
        itemCount=searchList['itemCount']
        translateParam=searchList['translate']
        currencyParam=searchList['currency']

        #keyword=input('검색어를 입력하세요(please input keyword) => ')
        # selectCnt=int(input('검색할 아이템 수를 입력하세요(please input item count) => '))
        translatedWord=self.translate(translateParam,keyword)
        selectCnt=int(itemCount)
        language=translateParam#ko,ja
        currency=currencyParam#KRW,JPY

        searchlang='カタカナ'
        url="https://www.amazon.co.jp/s?k="+translatedWord+"&s=review-rank&__mk_ja_JP="+searchlang+"&ref=sr_pg_1"
        print('검색(URL) : ',url)
        print('검색어(keyWord)  : ',keyword)
        print('검색 아이템수(item Count) : ',selectCnt)
        print('통화 (currency) : ',currency=='KRW' and '원화(￦)' or '엔화(￥)')
        print('번역언어 (language) : ',language=='ko' and '한국어(kor)' or '일본어(jap)')
        return url

    def movePage(self):
        try:
            itemCnt=1
            pageCnt=1
            arr = []

            while True:
                nextPageTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.a-pagination>li.a-last')))
                lastPageTag=self.checkExistElement(driver,'ul.a-pagination>li.a-disabled.a-last')[0]
                
                #nextBtn이disabled ２페이지까지 출력
                if lastPageTag | (pageCnt>2):
                    print('검색이 완료되었습니다(searching complete)')
                    return arr
                
                for item in driver.find_elements_by_xpath("//div[@data-asin][@data-component-type]"):
                    brandName=self.checkExistElement(item,'h5')[0]==True and self.checkExistElement(item,'h5')[1].text or 'none'
                    itemName=self.checkExistElement(item,'h2')[0]==True and self.checkExistElement(item,'h2')[1].text or 'none'
                    reviewCnt=self.checkExistElement(item,'span.a-size-base')[0]==True and int(self.checkExistElement(item,'span.a-size-base')[1].text) or 'none'
                    price=self.checkExistElement(item,'span.a-price-whole')[0]==True and self.convCurrency(self.checkExistElement(item,'span.a-price-whole')[1].text) or '0'
                    itemUrl=self.checkExistElement(item,'h2')[0]==True and parse.unquote(self.checkExistElement(item,'h2>a')[1].get_attribute("href")) or 'none'

                    #transfer to kor
                    if language=='ko':
                        brandName=self.translate('ko',brandName)
                        itemName=self.translate('ko',itemName)

                    arr.append([itemCnt,brandName,itemName,reviewCnt,price,itemUrl])
                    print(itemCnt,"번째아이템","브랜드명:",brandName,"아이템명:",itemName,"리뷰수:",reviewCnt,"가격:",price)
                    itemCnt+=1

                    if itemCnt>selectCnt:
                        print('검색이 완료되었습니다(searching complete)')
                        return arr

                pageCnt+=1
                nextPageTag.click()
        except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름

    def checkExistElement(self,item,selector):
        try:
            reVal=item.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return [False]
        return [True,reVal]

    def translate(self,lang,searchWord):
        global trans

        while True:
            try:
                text = trans.translate(searchWord, dest=lang).text
                #print('번역한 검색어 (translated keyword) : ',text)
                return text
            except Exception:
                trans = Translator()

    def convCurrency(self,japYen):
        try:
            reVal=japYen
            #curCov.currencies지원통화확인
            if currency=='KRW':
                reVal='￦'+ format(int(curCov.convert(japYen[1:].replace(',',''),'JPY','KRW')), ',')
            return reVal
        except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름

    def getSortedArr(self,arr):
        #평가는 많고 가격은 낮은것 
        #arr[itemCnt,brandName,itemName,reviewCnt,price]
        arr.sort(key = lambda x: [-x[3],x[4]])
        return arr

    def run(self):
        try:
            print('프로그램을 시작합니다(Start Application)')
            arr=self.movePage()#페이지 이동
            arrSorted=self.getSortedArr(arr)#정렬된 리스트 가져오기
            return arrSorted
            # for i in arrSorted: 
            #     print(i)
        except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
        finally:
            print('프로그램 종료(Exits application)')
            #time.sleep(60)
            driver.quit()

#######시작함수######################################################################3
