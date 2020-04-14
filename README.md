# SimplePanel
Monitor your BDS Server in broswer
# Requirements
Python3<br>
Flask (use `pip3 install flask` to install)<br>
# Configure
modify `main.py`<br>
modify `SECRET_KEY=b"YOUR_PASSWORD_ENG_NUMBER"`<br>
specify your server path `["F:\\bedrock-server-1.14.21.0\\bedrock_server.exe"],"F:\\bedrock-server-1.14.21.0\\"`<br>
specify www port `app.run(host="0.0.0.0", port=3390)`<br>
# Start
`python3 main.py`<br>
daemon will restart server when it dies.<br>
open http://your_ip:3390/ in browser
