import urllib.request
import json
import os

class Papago:
    def __init__(self):
        '''클라이언트 키 초기화'''
        #클라이언트 키 경로
        path_key=os.path.abspath('..')
        fileName='\papagoKey.json'
        key=None
        #파파고 클라이언트 키 읽기
        with open(path_key+fileName, 'r',-1,"utf-8") as keyText:
            key = json.loads(keyText.read())

        #번역키
        global client_id_tran
        client_id_tran= key['trans']['client_id_tran']
        global client_secret_tran
        client_secret_tran = key['trans']['client_secret_tran']
        
        #언어감지키
        global client_id_check
        client_id_check= key['check']['client_id_check']
        global client_secret_check
        client_secret_check = key['check']['client_secret_check']

    def translate(self,targetLang,searchWord):
        '''번역기능'''
        srcLang=self.checkLang(searchWord)
        encText = urllib.parse.quote(searchWord)
        data = "source="+srcLang+"&target="+targetLang+"&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id_tran)
        request.add_header("X-Naver-Client-Secret", client_secret_tran)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()

        if(rescode == 200):
            response_body = response.read()
            #return jsonObj_reVal=json.loads(response_body.decode('utf-8'))['langCode']
            message_reVal=json.loads(response_body.decode('utf-8'))['message']['result']['translatedText']
            return message_reVal
        else:
            print("Error Code:" + rescode)

    def checkLang(self,searchWord):
        '''언어감지
        1. ko: 한국어
        2. ja: 일본어
        3. zh-CN: 중국어 간체
        '''
        encQuery = urllib.parse.quote(searchWord)
        data = "query=" + encQuery
        url = "https://openapi.naver.com/v1/papago/detectLangs"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id_check)
        request.add_header("X-Naver-Client-Secret",client_secret_check)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            jsonObj_reVal=json.loads(response_body.decode('utf-8'))['langCode']
            return jsonObj_reVal
        else:
            print("Error Code:" + rescode)
        
# p=Papago()
# p.translate('ja','안녕하세요?')