import requests
import time
import test
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def searchCondition():
    itemName='マフラー'
    lang='カタカナ'
    url="https://www.amazon.co.jp/s?k="+itemName+"&s=review-rank&__mk_ja_JP="+lang+"&ref=sr_pg_1"
    return url

def movePage():
    try:
        while True:
            nextPageTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.a-pagination>li.a-last')))
            pageCnt=0
            #driver.findElements( By.id("...") ).size() != 0
            #extPageTagChk=driver.findElements(By.CSS_SELECTOR('ul.a-pagination>li.a-last>a')).size() > 0
            #nextBtnList = driver.find_elements_by_css_selector('ul.a-pagination>li.a-last>a')
            #nextBtn이disabled 10페이지이상 넘어가면 중단
            if len(nextPageTag.size)>0 & pageCnt<10:
                mainNameTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'h5.s-line-clamp-1')))
                priceTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.a-price-whole')))
                #subNameTag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.a-size-base-plus a-color-base a-text-normal')))
                print('상품명',mainNameTag.text)
                print('가격',priceTag.text)
                pageCnt=+1
                nextPageTag.click()
            else:
                break
    except Exception as ex: # 에러 종류
        print('에러가 발생 했습니다', ex) # ex는 발생한 에러의 이름
    finally:
        driver.quit()

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
    

# liTag = browser.find_elements_by_css_selector('ul.a-pagination>li.a-selected')

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