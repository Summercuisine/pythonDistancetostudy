import hashlib
import requests
import time
import json
import os

url = "https://supremes.pro/api/generate"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39",
    "Origin": "https://supremes.pro",
    "Referer": "https://supremes.pro/",
}

dialogues = [f for f in os.listdir('.') if f.endswith('.json')]

while True:
    # 询问用户是否要创建新的对话文件
    new_dialogue = input("要创建新的对话文件吗？（是/否）")

    if new_dialogue.lower() in ['y', 'yes', '是']:
        # 如果用户选择创建新的对话，则让其输入对话文件名，并创建空的对话列表
        filename = input("请输入对话文件名：")
        if not filename.endswith('.json'):
            filename += '.json'
        dialogue = []
        print(f"创建新的对话文件 {filename} 成功。")
        break

    elif new_dialogue.lower() in ['n', 'no', '否']:
        # 如果用户选择不创建新的对话文件，则列出当前目录下的所有对话文件并让用户选择一个
        if len(dialogues) > 0:
            print("请选择要加载的对话文件：")
            for i, d in enumerate(dialogues):
                print(f"{i+1}. {d}")
            selection = int(input("请选择你要载入的对话文件序号")) - 1
            try:
                filename = dialogues[selection]
                with open(filename, 'r') as f:
                    dialogue = json.load(f)
                print(f"加载对话文件 {filename} 成功。")
                break
            except:
                print("选择无效，请重新选择。")
        else:
            print("当前目录下没有对话文件。")
            # 如果当前目录下没有对话文件，则让用户输入对话文件名，并创建空的对话列表
            filename = input("请输入对话文件名：")
            if not filename.endswith('.json'):
                filename += '.json'
            dialogue = []
            print(f"创建新的对话文件 {filename} 成功。")
            break

    else:
        print("无效的输入，请重新输入。")

while True:
    input_content = input("输入对话内容\输入退出即可退出对话：")
    if input_content == "退出":
        break
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

    try:
        print("请求中...耐心等待")
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
        with open(filename, "w") as f:
            json.dump(dialogue, f, indent=4, ensure_ascii=False)

    except requests.exceptions.SSLError as e:
        raise SSLError(e, request=request)
