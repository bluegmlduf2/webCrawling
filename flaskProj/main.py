from flask import Flask,render_template,request
from ama import amazon as amaModule

app = Flask(__name__)

@app.route('/')
def index():
    '''시작페이지'''
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    '''검색페이지'''
    amaInst=amaModule.Amazon(request.form)
    value=amaInst.run()
    return render_template('index.html',sendData=value,optionData=request.form)    

if __name__ == '__main__':
    app.run(debug=True)
