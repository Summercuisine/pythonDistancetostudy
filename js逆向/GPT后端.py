from flask import Flask, request, jsonify, render_template
import hashlib
import requests
import time
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    # POST 请求
    input_content = request.form['input_content']

    # 创建当前用户的消息
    user_message = {"role": "user", "content": input_content}

    # 创建 payload
    timestamp_ms = int(time.time() * 1000)
    r = f"{timestamp_ms}:{input_content}:undefined"
    sign = hashlib.sha256(r.encode('utf-8')).hexdigest()
    messages = dialogue + [user_message]
    payload = {
        'messages': messages,
        'time': timestamp_ms,
        'pass': None,
        'sign': sign
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39",
        "Origin": "https://supremes.pro",
        "Referer": "https://supremes.pro/",
    }

    url = "https://supremes.pro/api/generate"

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)

        # 解析机器人的回复，并将对话内容添加到对话历史中
        reply_content = response.text.strip()

        # 在机器人的回复前添加 "AI: "
        assistant_message = {"role": "assistant", "content": reply_content}

        # 在用户的消息前添加 "User: "
        user_message_with_prefix = {"role": "user", "content": input_content}

        dialogue.append(user_message_with_prefix)
        dialogue.append(assistant_message)

        # 打印机器人的回复并保存对话记录到文件中
        print(assistant_message['content'])
        with open("dialogue.json", "w") as f:
            json.dump(dialogue, f, indent=4, ensure_ascii=False)

        # 返回 JSON 格式数据
        return jsonify(reply_content)

    except requests.exceptions.SSLError as e:
        raise SSLError(e, request=request)

@app.route('/conversation')
def conversation():
    with open("dialogue.json", "r") as f:
        dialogue = json.load(f)
    return render_template('conversation.html', dialogue=dialogue)

if __name__ == '__main__':
    dialogue = []
    app.run()
