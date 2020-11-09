import requests
from bs4 import BeautifulSoup

#크롤링 접속차단 해제
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

a='マフラー'
b='カタカナ'
url="https://www.amazon.co.jp/s?k="+a+"&__mk_ja_JP="+b+"&ref=sr_pg_1"
res=requests.get(url,headers = headers)

soup=BeautifulSoup(res.content,"html.parser")

#print(soup.find_all("div",attrs={'class':'s-expand-height s-include-content-margin s-latency-cf-section'}))
print(soup.find_all("span",attrs={'class':'a-price'}))#가격
#print(soup.find_all("div",attrs={'class':'a-size-base a-link-normal a-text-normal'}))#이름