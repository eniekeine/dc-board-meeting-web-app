import json
import re
import sqlite3
import pandas as pd
from word_over_date import WordOverDateContext, word_over_date_regex
from data_config import get_data_keyword_config, get_keywords

config : dict = get_data_keyword_config()
keywords = get_keywords()
db_file_name = "dcinside_corpus.db"
db_table_name = "board_programming"

# data/keyword/*.json 파일을 생성한다.
def make_keyword_file(keyword : dict):
    displayname : str = keyword["displayname"]
    pattern : str = keyword["pattern"]
    compiled_pattern : re.Pattern = re.compile(pattern)
    context = WordOverDateContext(group_pattern="%Y")
    table = word_over_date_regex(compiled_pattern, context)
    with open(f"./data/keyword/{displayname}.json", "wt", encoding="utf-8") as file:
        json.dump(table, file)

class PreprocStrategy:
    def convert(self, line):
        return line
class RemoveUrl(PreprocStrategy):
    def __init__(self):
        self.pattern = re.compile(r"https?://(?:\w+\.)+\w+(?:/\S*)?")
    def convert(self, line):
        return self.pattern.sub(" ", line)
class RemoveLaugh(PreprocStrategy):
    def convert(self, line):
        return re.sub("ㅋ{3,}", "ㅋㅋ", line)
class RemoveComma(PreprocStrategy):
    def convert(self, line):
        return re.sub(',', ' ', line)
class RemoveInprintable(PreprocStrategy):
    def convert(self, line):
        return re.sub(r'[\x00-\x1F]', ' ', line)
class RemoveWhitespace(PreprocStrategy):
    def convert(self, line):
        return re.sub("\s{2,}", " ", line)
def make_corpus_txt(id_begin : int = 1, id_end : int = -1, strategy : list[PreprocStrategy] = [
    RemoveLaugh(),
    # RemoveComma(),
    RemoveUrl(),
    RemoveWhitespace()]):
    """
    db 파일에서 제목과 글의 내용을 읽어들여 코퍼스 파일을 생성한다.
    """
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        # columns : 'document_id', 'author', 'title', 'content', 'view_count', 'voteup_count', 'votedown_count', 'time'
        # DB에 저장할 때 실수로 author와 title의 순서를 바꿔먹었으므로 다음 줄은 사실 title, content를 가져오는 내용임
        if id_end == -1:
            cursor.execute(f"SELECT author, content FROM {db_table_name} WHERE document_id >= {id_begin}")
        else:
            cursor.execute(f"SELECT author, content FROM {db_table_name} WHERE document_id >= {id_begin} and document_id <= {id_end}")
        records : list[tuple] = cursor.fetchall()
        print("records : ", len(records))
        df = pd.DataFrame(records, columns =['title', 'content'])
        # 제목과 내용을 결합
        strs = df['title'] + ' ' + df['content']
        for preproc in strategy:
            strs = [preproc.convert(line) for line in strs]
        return strs
def make_keyword_files():
    for keyword in config["keywords"]:
        make_keyword_file(keyword)
if __name__ == "__main__":
    # make_keyword_files()
    make_corpus_txt("data/corpus/raw.txt")
