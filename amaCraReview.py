import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#browser = webdriver.Chrome("C:\Users\YOON\Desktop\pythonProj\chromedriver_win32.exe")
browser = webdriver.Chrome()

a='マフラー'
b='カタカナ'
#pageCnt=1

url="https://www.amazon.co.jp/s?k="+a+"&__mk_ja_JP="+b+"&ref=sr_pg_1"
browser.get(url)

# liTag = browser.find_elements_by_css_selector('ul.a-pagination>li.a-selected')

while True:
    nextBtnList = browser.find_elements_by_css_selector('ul.a-pagination>li.a-last>a')
    pageCnt=0
    
    #nextBtn이disabled이거나 10페이지이상 넘어가면 중단
    if int(len(nextBtnList))>0 & pageCnt<10:
        pageCnt=+1
        nextBtnList[0].click()
        time.sleep(5) 
    else:
        break


# if int(len(nextBtnList))>0:
#     nextBtnList[0].click()
#     while True:
#         browser.find_elements_by_css_selector('span.a-price-whole')
#         div_elems = browser.find_elements_by_xpath("//div[@data-asin]")




#nextBtn.click()  # 클릭
 
#import time
# time.sleep(5) # 5초 대기
# browser.quit() # 브라우저 종료
#time.sleep(5) # 5초 대기
#ul.a-pagination>li.a-last
# ul.a-pagination>li.a-last.a-disabled

#크롤링 접속차단 해제
#headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

# a='マフラー'
# b='カタカナ'

# # pageCnt=str(10)

# pageCnt=1

# while 0 < pageCnt:
#     url="https://www.amazon.co.jp/s?k="+a+"&__mk_ja_JP="+b+"&ref=sr_pg_"+str(pageCnt)
#     res=requests.get(url,headers = headers)
#     print(url)
#     if res.ok:
#         pageCnt+=1
#     else:
#         break

# print(pageCnt)

#soup=BeautifulSoup(res.content,"html.parser")

#print(soup.find_all("div",attrs={'class':'s-expand-height s-include-content-margin s-latency-cf-section'}))
#print(soup.find_all("span",attrs={'class':'a-price-whole'}))#가격
#print(soup.find_all("div",attrs={'class':'a-size-base a-link-normal a-text-normal'}))#이름