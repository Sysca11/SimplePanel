#coding=utf8
SECRET_KEY=b"YOUR_PASSWORD_ENG_NUMBER"
ENCODE="utf8"
from flask import Flask
from flask import request,redirect,send_file
from Daemon import Daemon
D=Daemon(["F:\\bedrock-server-1.14.21.0\\bedrock_server.exe"],"F:\\bedrock-server-1.14.21.0\\")
D.ENCODE=ENCODE
import json
import hashlib
SEC_MD5=hashlib.md5(SECRET_KEY).hexdigest()

app = Flask(__name__)

def checkPerm(cookie):
    if cookie.get("p")==SEC_MD5:
        return True
    return False
@app.route('/')
def default():
    return Main()
@app.route('/index')
def Main():
    if checkPerm(request.cookies)==False:
        return redirect("/auth")
    return send_file("index.html")
@app.route('/auth')
def Auth():
    return send_file('auth.html')
@app.route('/ctrl/<ctrl>',methods=['GET', 'POST'])
def control(ctrl):
    if checkPerm(request.cookies)==False:
        return redirect("/auth")
    if ctrl=="start":
        D.start()
    if ctrl=="stop":
        D.stop()
    if ctrl=="i":
        D.input(bytes(request.form["inp"],encoding="utf8"))
    return ""
@app.route('/log/<int:tim>')
def getLog(tim):
    if checkPerm(request.cookies)==False:
        return "False"
    if tim==D.lastTime:
        return json.dumps({"time":tim,"log":"none"})
    else:
        return json.dumps({"time":D.lastTime,"log":str(D.getLog(),encoding=ENCODE)})
app.run(host="0.0.0.0", port=3390)