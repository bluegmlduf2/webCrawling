from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import amazonReviewCnt

# python -m http.server
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #parsed_path=urlparse(self.path)
        # message_parts='Client address :',self.client_address,
        # 'Client string :',self.address_string(),
        # 'Command : ',self.command,
        # 'Path : ',self.path,
        # 'real path : ',parsed_path.path,
        # 'query : ',parsed_path.query,
        # 'request version : ',self.request_version,
        # 'server_version : ',self.server_version,
        # 'sys_version : ',self.sys_version,
        # 'protocol_version : ',self.protocol_version
        #message='<br>'.join(message_parts)
        self.send_response(200) #응답코드
        self.end_headers() #헤더가 본문을 구분
        # self.wfile.write(message.encode('utf-8'))
        reArr=amazonReviewCnt.init()
        #json으로 보내기
        self.wfile.write(self.path.encode())
        self.wfile.write(reArr[2].encode('utf-8'))
        
        return None

s=HTTPServer(('localhost',8888),MyHandler)
print('Started WebServer on port 8888...')
s.serve_forever()
