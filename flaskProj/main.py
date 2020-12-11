from flask import Flask,render_template,request
from ama import amazon as amaModule
from ama import csvParser as parseModule
import json
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    '''시작페이지'''
    try:
        return render_template('index.html')
    except Exception as ex: 
        #sys.exc_info()
        print(traceback.print_exc())
        return render_template('error_404.html')
    finally:
        print('프로그램 종료(Exits application)')

@app.route('/search',methods=['POST'])
def search():
    try:
        '''검색페이지'''
        amaInst=amaModule.Amazon(request.form)
        value=amaInst.run()  
    except Exception as ex: 
        #sys.exc_info() #raise Exception
        print(traceback.print_exc())
        return render_template('error_404.html')
    else:
        return render_template('index.html',sendData=value,optionData=request.form)
    finally:
        print('프로그램 종료(Exits application)')

@app.route('/parseCsv',methods=['POST'])
def parseCsv():
    try:
        parseModule.csvParser(request.json)
    except Exception as ex: 
        #sys.exc_info()
        print(traceback.print_exc())
    finally:
        print('프로그램 종료(Exits application)')


#if __name__ == '__main__':
    #app.run(debug=True)

#if __name__ == '__main__':
app.run(debug=True)