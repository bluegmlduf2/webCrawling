import requests
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from googletrans import Translator #번역
from currency_converter import CurrencyConverter #환율
from urllib import parse #url 디코딩용

class Amazon:
    def __init__(self,searchList):
        '''인스턴스 생성시 초기화'''
        url=self.searchCondition(searchList)
        
        global driver  
        driver = webdriver.Chrome("C:\\Users\\YOON\\Desktop\\pythonProj\\webCrawling\\flaskProj\\ama\\chromedriver.exe")#크롬 드라이버(chromedriver_path)
        driver.get(url)#조건을 포함한 브라우저를 실행

        global wait
        wait = WebDriverWait(driver , 10) #10초를 기다린다.

        global curCov
        curCov = CurrencyConverter()#통화 인스턴스 초기화

    def searchCondition(self,searchList):
        '''검색조건입력'''
        global selectCnt
        global currency
        global language
        global trans
        trans = Translator(service_urls=['translate.googleapis.com'])
        
        #검색조건
        keyword=searchList['keyword']
        itemCount=searchList['itemCount']
        translateParam=searchList['translate']
        currencyParam=searchList['currency']

        translatedWord=self.translate('ja',keyword)
        selectCnt=int(itemCount)
        language=translateParam#ko,ja,zh-cn
        currency=currencyParam#KRW,JPY,CNY

        searchlang='カタカナ'
        url="https://www.amazon.co.jp/s?k="+translatedWord+"&s=review-rank&__mk_ja_JP="+searchlang+"&ref=sr_pg_1"
        print('검색(URL) : ',url)
        print('검색어(keyWord)  : ',keyword)
        print('검색 아이템수(item Count) : ',selectCnt)
        print('통화 (currency) : ',currency)
        print('번역언어 (language) : ',language)
        return url

    def movePage(self):
        '''페이지 이동 함수'''
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
                    reviewCnt=self.checkExistElement(item,'span.a-size-base')[0]==True and int(self.checkExistElement(item,'span.a-size-base')[1].text.replace(',','')) or 0
                    price=self.checkExistElement(item,'span.a-price-whole')[0]==True and self.convCurrency(self.checkExistElement(item,'span.a-price-whole')[1].text) or 0
                    itemUrl=self.checkExistElement(item,'h2')[0]==True and parse.unquote(self.checkExistElement(item,'h2>a')[1].get_attribute("href")) or 'none'

                    #translate
                    if language != 'ja':
                        brandName=self.translate(language,brandName)
                        itemName=self.translate(language,itemName)
                
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

    def checkExistElement(self,item,selector):
        '''널 체크 함수'''
        try:
            reVal=item.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return [False]
        return [True,reVal]

    def translate(self,lang,searchWord):
        '''번역함수'''
        global trans

        while True:
            try:
                text = trans.translate(searchWord, dest=lang).text
                #print('번역한 검색어 (translated keyword) : ',text)
                return text
            except Exception:
                trans = Translator(service_urls=['translate.googleapis.com'])

    def convCurrency(self,japYen):
        '''환율검색함수'''
        try:
            reVal=japYen
            #curCov.currencies지원통화확인
            if currency=='KRW':
                reVal='￦'+ format(int(curCov.convert(japYen[1:].replace(',',''),'JPY','KRW')), ',')
            if currency=='CNY':
                reVal='¥'+ format(int(curCov.convert(japYen[1:].replace(',',''),'JPY','CNY')), ',')#format(i,',') 3글자포맷
            return reVal
        except Exception as ex: # 에러 종류
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름

    def getSortedArr(self,arr):
        '''평가순 정렬함수'''
        #arr[itemCnt,brandName,itemName,reviewCnt,price]
        #sort(key=value) value => int(x) 
        arr.sort(key = lambda x: [int(-x[3])])
        return arr

    def run(self):
        '''실행함수'''
        try:
            print('프로그램을 시작합니다(Start Application)')
            arr=self.movePage()#페이지 이동
            arrSorted=self.getSortedArr(arr)#정렬된 리스트 가져오기
            return arrSorted
        except Exception as ex: # 에러 종류
            print(traceback.print_stack())
            print(traceback.print_exc())
            print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
            print('에러가 발생 했습니다', ex.__traceback__) # ex는 발생한 에러의 이름
        finally:
            print('프로그램 종료(Exits application)')
            #time.sleep(60)
            driver.quit()

