import time
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_sign', methods=['POST'])
def get_sign():
    # 获取请求中的时间戳和输入内容
    timestamp_ms = request.form.get('timestamp_ms')
    input_content = request.form.get('input_content')
    # 拼接字符串
    r = f"{timestamp_ms}:{input_content}:undefined"
    # 计算 SHA256 哈希值
    sign = hashlib.sha256(r.encode('utf-8')).hexdigest()
    # 返回 JSON 格式的响应
    return jsonify({'sign': sign})

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(threaded=True)

