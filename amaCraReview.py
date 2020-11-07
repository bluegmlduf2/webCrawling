import requests
from bs4 import BeautifulSoup

a='マフラー'
b='カタカナ'
url="https://www.amazon.co.jp/s?k="+a+"&__mk_ja_JP="+b+"&ref=sr_pg_1"
res=requests.get(url)

soup=BeautifulSoup(res.content,"html.parser")


print(soup.find_all("div",attrs={"data-component-id":True}))