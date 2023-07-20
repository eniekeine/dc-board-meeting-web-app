import os
from data_make import make_corpus_txt
from extract_word import make_word_score_table, save_to_csv, load_word_score_data_frame_csv, word_score_table_to_datafarme
from extract_noun_lr_v2 import make_noun_score_table, save_noun_score_table_df, load_noun_score_table, noun_score_table_to_dataframe
from tokenize_lr import tokenize_lr_sent
import pandas as pd
raw_filename            = "./data/corpus/raw01.txt"
noun_filename_csv       = "./report/extract/noun_score_table.csv"
table_filename_csv      = "./report/extract/word_score_table.csv"
word_candidate_filename = "./report/extract/word_candidate.csv"
def cache_or_get_corpus():
    strs = []
    if not os.path.exists(raw_filename):
        strs = make_corpus_txt()
        with open(raw_filename, "wt", encoding='utf-8') as file:
            file.writelines(strs)
    else:    
        with open(raw_filename, "rt", encoding='utf-8') as file:
            strs = file.readlines()
    return strs
def cache_or_get_noun_table(strs):
    if not os.path.exists(noun_filename_csv):
        noun_table = make_noun_score_table(strs)
        df_noun = noun_score_table_to_dataframe(noun_table)
        save_noun_score_table_df(df_noun, noun_filename_csv)
        return df_noun
    else:
        return load_noun_score_table(noun_filename_csv)
def cache_or_get_word_table(strs):
    if not os.path.exists(table_filename_csv):
        table = make_word_score_table(strs)
        save_to_csv(table, table_filename_csv)
        return word_score_table_to_datafarme(table)
    else:
        return load_word_score_data_frame_csv(table_filename_csv)
if __name__ == "__main__":
    strs = cache_or_get_corpus()
    df_noun_table : pd.DataFrame = cache_or_get_noun_table(strs)
    df_word_table : pd.DataFrame = cache_or_get_word_table(strs)
    df_merged_table = pd.merge(df_noun_table, df_word_table)
    df_merged_table["final_score"] = df_merged_table["cohesion_forward"] * df_merged_table["right_branching_entropy"] + df_merged_table["score"]
    word_to_final_score = dict(zip(df_merged_table['word'], df_merged_table["final_score"]))
    tokenized : list = tokenize_lr_sent(word_to_final_score, """
개발자로 구직활동 하려고 C언어를 배웠다. Java도 연습했다. 
그런데 취업이 잘 되지 않는다.
프로그래밍 잘 하고 프로그램 잘 설계한다고 소프트웨어 개발자가 될 수 있는 건 아닌 것 같다.
요즘 시대에는 웹 개발이 더 중요하단 걸 깨달았다. 
프론트엔드도 백엔드도 공부해서 풀스택 개발자가 돼야겠다. 
아무래도 나는 javascript보다는 python이 더 쉽다. 그래서 nodejs말고 Flask로 백엔드를 공부했다. 
인공지능도 미리 공부해놔야지. 딥러닝 잘 아는 사람 있나?
C/C++는 어떤가?
""")
    print(tokenized)
    
    
    