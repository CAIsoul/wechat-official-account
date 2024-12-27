from flask import Flask, request
from datetime import datetime
import util.chat_prompt as ai
import xml.etree.ElementTree as ET
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

        if hashcode != signature:
            return "Wrong Credential"

        if request.method == 'POST':
            return handlePostRequest(request.data)

        return echostr
        
    except Exception as e:
        return str(e)


def handlePostRequest(xmlData):
    root = ET.fromstring(xmlData)

    to_user_name = root.findtext('ToUserName')
    from_user_name = root.findtext('FromUserName')
    create_time = root.findtext('CreateTime')
    msg_type = root.findtext('MsgType')
    content = root.findtext('Content')
    msg_id = root.findtext('MsgId')
    msg_data_id = root.findtext('MsgDataId')
    idx = root.findtext('Idx')

    now = datetime.now()

    # Convert to a timestamp
    current_time_seconds = datetime.timestamp(now)

    print(f"ToUserName: {to_user_name}")
    print(f"FromUserName: {from_user_name}")
    print(f"CreateTime: {create_time}")
    print(f"MsgType: {msg_type}")
    print(f"Content: {content}")
    print(f"MsgId: {msg_id}")
    print(f"MsgDataId: {msg_data_id}")
    print(f"Idx: {idx}")

    xml_string = """
        <xml>
            <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
            <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[{msg_type}]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
        </xml>
    """.format(
        to_user_name = to_user_name,
        from_user_name = from_user_name,
        create_time = current_time_seconds,
        msg_type = msg_type,
        content = ai.ask_question(content)
    )

    print(xml_string)
    return xml_string



if __name__ == '__main__':
    app.run(host=Host, port=Port, debug=True)