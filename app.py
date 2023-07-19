import json
from flask import Flask, render_template, jsonify
from data_read import get_keywords, get_keyword_record

app = Flask(__name__) # __name__을 사용하면 Flask에서 필요한 경로 설정과 설정 로딩을 수행가능

@app.route('/')
def app_index():
    return render_template('index.html')

@app.route('/keyword')
def app_keyword():
    return render_template('keyword.html', keywords=get_keywords())
    
@app.route('/keyword/records/<string:keyword>')
def app_get_records_for_keyword(keyword : str):
    return jsonify(get_keyword_record(keyword))
if __name__ == '__main__':
    app.run()
