from flask import Flask, render_template, request

app = Flask(__name__)

# 儲存留言嘅列表
messages = []

@app.route('/')
def index():
    # 將留言列表傳遞到 HTML 模板
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['POST'])
def post_message():
    # 獲取表單提交嘅留言
    message = request.form['message']
    # 把留言加入到 messages 列表
    messages.append(message)
    # 重新導向到首頁，顯示所有留言
    return index()

if __name__ == '__main__':
    app.run(debug=True)
