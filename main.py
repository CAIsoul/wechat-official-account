from flask import Flask, request, abort
import hashlib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

Token = config.get('credential', 'token')
Host = config.get('setting', 'host')
Port = config.get('setting', 'port')

app = Flask(__name__)

@app.route('/wx', methods=['GET', 'POST'])
def handle():
    try:
        data = request.args
        if not data:
            return "hello, this is handle view"
        
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')

        token = Token
        list_to_hash = [token, timestamp, nonce]
        list_to_hash.sort()
        sha1 = hashlib.sha1()

        for item in list_to_hash:
            sha1.update(item.encode('utf-8'))

        hashcode = sha1.hexdigest()
        print(f"handle/GET func: hashcode, signature: {hashcode}, {signature}")

        if hashcode == signature:
            return echostr
        else:
            return ""
        
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host=Host, port=Port, debug=True)