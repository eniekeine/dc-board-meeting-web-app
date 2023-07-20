from data_make import make_corpus_txt
from extract_word import make_word_score_table, save_to_excel, save_to_csv, load_word_score_data_frame_csv
from examine_word_score import examine
import pandas as pd
raw_filename            = "./data/corpus/raw01.txt"
table_filename_csv      = "./report/extract/word_score_table.csv"
word_candidate_filename = "./report/extract/word_candidate.csv"

# -- 코퍼스 txt 파일 만들기
# print(f"- 코퍼스 생성중 {raw_filename}...")
# strs = make_corpus_txt()
# with open(raw_filename, "wt", encoding='utf-8') as file:
#     file.writelines(strs)

# # -- 워드 스코어 테이블 엑셀 파일 만들기
# print(f"- 단어 추출 중...")
# -- 추출
# table = make_word_score_table(strs)
# save_to_csv(table, table_filename_csv)
# -- 파일에서 로드
df : pd.DataFrame = load_word_score_data_frame_csv(table_filename_csv)

# -- 데이터 확인하기
print(f"- 생성중 {word_candidate_filename}...")
df2 = examine(df)
df2.to_csv(word_candidate_filename, index=False)
