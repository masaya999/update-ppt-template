from flask import Flask, render_template, request
import csv
import copy
from pptx import Presentation

app = Flask(__name__)

core_text = {}
custom_text = {}
csv_file_path = 'sample.csv'
pptx_file_path = 'sample.pptx'

@app.route('/')
def index():
    # CSVファイルを開いて読み込む
    with open(csv_file_path, mode='r', encoding='cp932') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            # 1列目をキー、2列目を値として辞書に格納
            key = row[0]
            value = row[1]
            core_text[key] = value
            custom_text[key] = value

    #custom_text = copy.deepcopy(core_text)
    #custom_text = {key: value for key, value in core_text.items()}
    print(core_text)
    print(custom_text)
    return render_template('index.html', data=custom_text)

@app.route('/update', methods=['POST'])
def update():
    # テキストボックスからの新しいデータを受け取り、dictを更新
    for key in custom_text.keys():
        custom_text[key] = request.get(key)
    
    # PowerPointファイルを更新する関数を呼び出す
    update_pptx_with_custom_text()
    
    return render_template('index.html', data=custom_text, filename='customized_'+pptx_file_path)

def update_pptx_with_custom_text():
    prs = Presentation(pptx_file_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        for key, value in core_text.items():
                            if value in run.text and custom_text[key] != value:
                                run.text = run.text.replace(value, custom_text[key])
    prs.save('customized_'+pptx_file_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
