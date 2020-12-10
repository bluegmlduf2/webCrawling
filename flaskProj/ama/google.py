from googletrans import Translator 

class Google:
    def __init__(self):
        pass

    def translate(self,lang,searchWord):
        '''번역함수'''
        trans = Translator(service_urls=['translate.googleapis.com'])
        text = trans.translate(searchWord, dest=lang).text
        return text
        # trans = Translator(service_urls=['translate.googleapis.com'])
        # while True:
        #     try:
        #         text = trans.translate(searchWord, dest=lang).text
        #         #print('번역한 검색어 (translated keyword) : ',text)
        #         return text
        #     except Exception:
        #         trans = Translator(service_urls=['translate.googleapis.com'])
