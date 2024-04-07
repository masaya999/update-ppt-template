from flask import Flask, render_template, request

app = Flask(__name__)

# 初期のPythonのdict型変数
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
    # 任意の初期データを追加
}

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    # テキストボックスからの新しいデータを受け取り、dictを更新
    for key in data.keys():
        data[key] = request.form[key]
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
