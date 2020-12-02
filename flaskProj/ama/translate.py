import requests,json

# def __init__():
#     print('1')
#     setUrl()

def setUrl():
    print('2')
    URL = 'https://papago.naver.com/apis/n2mt/translate'
    # data = {'param1': 'value1', 'param2': 'value'} 
    data={'deviceId': '15458545-720f-45eb-a582-d0570524def5'
    ,'locale':'ja'
    ,'dict': 'true'
    ,'dictDisplay': 30
    ,'honorific': 'false'
    ,'instant': 'false'
    ,'paging': 'false'
    ,'source': 'ko'
    ,'target': 'ja'
    ,'text': '%EC%95%88%EB%85%95'} 
    data=json.dumps(data,indent=2)
    print(data)
    base64.
    response = requests.post(URL, data=data)
    sc=response.status_code
    rt=response.text
    print(sc)
    print(rt)

if __name__ == "__main__":
    setUrl()