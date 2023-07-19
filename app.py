from flask import Flask, render_template, jsonify
from data_config import get_keywords
from data_read import get_keyword_file

app = Flask(__name__)

@app.route('/')
def app_index():
    return render_template('index.html')

@app.route('/keyword')
def app_keyword():
    return render_template('keyword.html', keywords=get_keywords())
    
@app.route('/keyword/records/<string:keyword>')
def app_get_records_for_keyword(keyword : str):
    return jsonify(get_keyword_file(keyword))
if __name__ == '__main__':
    app.run()
