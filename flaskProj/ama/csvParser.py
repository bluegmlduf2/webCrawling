import pandas as pd
import os

def csvParser(data):
    df = pd.DataFrame(data)
    # .to_csv 
    # 최초 생성 이후 mode는 append
    if not os.path.exists('output.csv'):
        df.to_csv('output.csv', index=False, mode='w', encoding='utf-8')
    else:
        df.to_csv('output.csv', index=False, mode='a', encoding='utf-8', header=False)