import os
import requests
import time
from ama import google #디버깅탐색기의 FLASK_APP가 시작위치
from ama import papago
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from currency_converter import CurrencyConverter #환율
from urllib import parse #url 디코딩용

class Amazon:
    def __init__(self,searchList):
        '''인스턴스 생성시 초기화'''
        url=self.searchCondition(searchList)
        
        global driver  
        driver = webdriver.Chrome(os.getcwd()+"\\flaskProj\\ama\\chromedriver.exe")#크롬 드라이버(chromedriver_path)
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

        #번역기 선택
        if searchList['siteName']=='gl':
            trans=google.Google()
        else:
            trans=papago.Papago()

        #검색조건
        keyword=searchList['keyword']
        itemCount=searchList['itemCount']
        translateParam=searchList['translate']
        currencyParam=searchList['currency']

        #중국어간체_naver #삼한연산자_조건2개
        translateParam=(translateParam=='zh-cn' and searchList['siteName']=='na') ==True and 'zh-CN' or translateParam
        
        #검색조건
        translatedWord=trans.translate('ja',keyword)
        selectCnt=int(itemCount)
        language=translateParam#ko,ja,zh-CN
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
                #TAG
                brandName_tag=self.checkExistElement(item,'h5')
                itemName_tag=self.checkExistElement(item,'h2')
                reviewCnt_tag=self.checkExistElement(item,'span.a-size-base')
                price_tag=self.checkExistElement(item,'span.a-price-whole')
                itemUrl_tag=self.checkExistElement(item,'h2>a')
                image_tag=self.checkExistElement(item,'img')

                #VALUE
                brandName_val=brandName_tag[0]==True and brandName_tag[1].text or 'none'
                itemName_val=itemName_tag[0]==True and itemName_tag[1].text or 'none'
                reviewCnt_val=(reviewCnt_tag[0]==True and reviewCnt_tag[1].text.isdigit()==True) and int(reviewCnt_tag[1].text.replace(',','')) or 0 #isdigit() 문자열에 숫자포함하는지
                price_val=price_tag[0]==True and self.convCurrency(price_tag[1].text) or 0
                itemUrl_val=itemName_tag[0]==True and parse.unquote(itemUrl_tag[1].get_attribute("href")) or 'none' #unquote->%urlDecode
                imageSrc_val=image_tag[0]==True and image_tag[1].get_attribute("src") or ''

                #translate
                if language != 'ja':
                    brandName_val=trans.translate(language,brandName_val)
                    itemName_val=trans.translate(language,itemName_val)
            
                arr.append([itemCnt,brandName_val,itemName_val,reviewCnt_val,price_val,itemUrl_val,imageSrc_val])
                #print(itemCnt,"번째아이템","브랜드명:",brandName,"아이템명:",itemName,"리뷰수:",reviewCnt,"가격:",price)
                itemCnt+=1

                if itemCnt>selectCnt:
                    print('검색이 완료되었습니다(searching complete)')
                    return arr

            pageCnt+=1
            nextPageTag.click()

    def checkExistElement(self,item,selector):
        '''널 체크 함수'''
        try:
            reVal=item.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return [False]
        else:
            return [True,reVal]

    def convCurrency(self,japYen):
        '''환율검색함수'''
        reVal=japYen
        #curCov.currencies지원통화확인
        if currency=='KRW':
            reVal='￦'+ format(int(curCov.convert(japYen[1:].replace(',',''),'JPY','KRW')), ',')
        if currency=='CNY':
            reVal='¥'+ format(int(curCov.convert(japYen[1:].replace(',',''),'JPY','CNY')), ',')#format(i,',') 3글자포맷
        return reVal

    def getSortedArr(self,arr):
        '''평가순 정렬함수'''
        #arr[itemCnt,brandName,itemName,reviewCnt,price,url,imageSrc]
        #sort(key=value) value => int(x) 
        arr.sort(key = lambda x: [int(-x[3])])
        return arr

    def run(self):
        '''실행함수'''
        try:
            print('프로그램을 시작합니다(Start Application)')
            arr=self.movePage()#페이지 이동
            arrSorted=self.getSortedArr(arr)#정렬된 리스트 가져오기

        except TimeoutException:
            raise
            print("wait timeout..")
        except Exception as ex:
            raise #throw : 앞서 일어난 에러를 다시 던진다 
        else:
            return arrSorted
        finally:
            driver.close()
            driver.quit()
            
            

