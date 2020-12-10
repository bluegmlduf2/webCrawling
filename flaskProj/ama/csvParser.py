import pandas as pd
import os

def parseCsv(data):
    # 샘플 데이터 생성
    #soda = {'상품명': ['콜라', '사이다'], '가격': [2700, 2000]}
    csvData=data
    df = pd.DataFrame(csvData)

    # .to_csv 
    # 최초 생성 이후 mode는 append
    if not os.path.exists('output.csv'):
        df.to_csv('output.csv', index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)