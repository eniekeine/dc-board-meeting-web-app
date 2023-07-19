import sqlite3
import pandas as pd
import re

board_id = "programming"
db_file_name = "dcinside_corpus.db"
db_table_name = "board_programming"
with sqlite3.connect(db_file_name) as conn:
    cursor = conn.cursor()
    # columns : 'document_id', 'author', 'title', 'content', 'view_count', 'voteup_count', 'votedown_count', 'time'
    # DB에 저장할 때 실수로 author와 title의 순서를 바꿔먹었으므로 다음 줄은 사실 title, content를 가져오는 내용임
    cursor.execute(f"SELECT author, content FROM {db_table_name} WHERE document_id <= 200000")
    records : list[tuple] = cursor.fetchall()
    print("records : ", len(records))
    df = pd.DataFrame(records, columns =['title', 'content'])
    # 제목과 내용을 결합
    strs = df['title'] + ' ' + df['content']
    # URL 제거
    strs = [re.sub("https?://(?:\w+\.)+\w+(?:/\S*)?", " ", line) for line in strs]
    # ㅋㅋㅋ 이상은 전부 ㅋㅋ로 변경
    strs = [re.sub("ㅋ{3,}", "ㅋㅋ", line) for line in strs]
    # , 문장부호 제거
    strs = [re.sub(",", " ", line) for line in strs]
    # 모두 소문자로
    strs = [line.lower() for line in strs]
    # 파일로 추출
    with open("corpus_merged.txt", "wt", encoding='utf-8') as file:
        file.writelines(strs)
