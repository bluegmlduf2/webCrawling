from flask import Flask,render_template,request
from ama import amazon as amaModule

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    amaInst=amaModule.amazon(request.form)
    value=amaInst.run()
    return render_template('index.html',sendData=value)    

#  if __name__ == 'main':
# if __name__ == '__main__':
app.run(debug=True)
