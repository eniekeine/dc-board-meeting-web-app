import os
import json
from data_make import make_corpus_txt
from extract_word import make_word_score_table, save_to_csv, load_word_score_data_frame_csv, word_score_table_to_datafarme
from extract_noun_lr_v2 import make_noun_score_table, save_noun_score_table_df, load_noun_score_table, noun_score_table_to_dataframe
from soynlp.tokenizer import LTokenizer
from soynlp.vectorizer import BaseVectorizer, sent_to_word_contexts_matrix
from soynlp.word import pmi as pmi_func
from soynlp.utils import most_similar
import numpy as np
from scipy import sparse
import pandas as pd
from pprint import pprint
raw_folder              = "./data/corpus/"
raw_filename            = "./data/corpus/raw01.txt"
extract_folder          = "./report/extract/"
noun_filename_csv       = "./report/extract/noun_score_table.csv"
table_filename_csv      = "./report/extract/word_score_table.csv"
word_candidate_filename = "./report/extract/word_candidate.csv"
vectorize_folder        = "./report/extract/"
vectorized_filename     = "./report/vectorize/sentence_vectorized"
matrix_filename         = "./report/vectorize/matrix.npz"
idx2vocab_filename      = "./report/vectorize/idx2vocab.json"
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
    os.makedirs(raw_folder)
    os.makedirs(extract_folder)
    os.makedirs(vectorize_folder)
    strs = cache_or_get_corpus()
    df_noun_table : pd.DataFrame = cache_or_get_noun_table(strs)
    df_word_table : pd.DataFrame = cache_or_get_word_table(strs)
    df_merged_table = pd.merge(df_noun_table, df_word_table)
    df_merged_table["final_score"] = df_merged_table["cohesion_forward"] * df_merged_table["right_branching_entropy"] + df_merged_table["score"]
    word_to_final_score : dict[str, float] = dict(zip(df_merged_table['word'], df_merged_table["final_score"]))
    tokenizer = LTokenizer(word_to_final_score)
    tokenized_sentence : list[str]  = tokenizer.tokenize("""개발자로 구직활동 하려고 C언어를 배웠다. Java도 연습했다. 
그런데 취업이 잘 되지 않는다.
프로그래밍 잘 하고 프로그램 잘 설계한다고 소프트웨어 개발자가 될 수 있는 건 아닌 것 같다.
요즘 시대에는 웹 개발이 더 중요하단 걸 깨달았다. 
프론트엔드도 백엔드도 공부해서 풀스택 개발자가 돼야겠다. 
아무래도 나는 javascript보다는 python이 더 쉽다. 그래서 nodejs말고 Flask와 Django로 백엔드를 공부했다. 
인공지능도 미리 공부해놔야지. 딥러닝 잘 아는 사람 있나?
C/C++는 어떤가?""")
    print(tokenized_sentence)
    # POS 태깅은 각 단어의 품사를 직접 지정해야 하는 과정이 어려워 보여서 나중으로 미룬다.
    # 참고: https://github.com/lovit/soynlp/blob/master/tutorials/tagger_usage.ipynb
    vectorizer = BaseVectorizer(tokenizer)
    x : sparse.csr_matrix
    idx2vocab : list
    x, idx2vocab = None, None
    if not (os.path.exists(matrix_filename) and os.path.exists(idx2vocab_filename)):
        x, idx2vocab = sent_to_word_contexts_matrix(
            strs,
            windows = 3,
            min_tf = 10,
            tokenizer = tokenizer, # (default) lambda x:x.split(),
            dynamic_weight = False,
            verbose = True
        )
        with open(matrix_filename, "wb") as file:
            sparse.save_npz(file, x)
        with open(idx2vocab_filename, "wt", encoding="UTF-8") as file:
            json.dump(idx2vocab, file, ensure_ascii=False)
    else:
        with open(matrix_filename, "rb") as file:
            x = sparse.load_npz(file)
        with open(idx2vocab_filename, "rt", encoding="UTF-8") as file:
            idx2vocab = json.load(file)    
    np.save(matrix_filename, x)
    pmi, px, py = pmi_func(
        x,
        min_pmi = 0,
        alpha = 0.0,
        beta = 0.75
    )
    vocab2idx = {vocab:idx for idx, vocab in enumerate(idx2vocab)}
    query = vocab2idx['C++']
    
    submatrix = pmi[query,:].tocsr() # get the row of query
    contexts = submatrix.nonzero()[1] # nonzero() return (rows, columns)
    pmi_i = submatrix.data

    most_relateds = [(idx, pmi_ij) for idx, pmi_ij in zip(contexts, pmi_i)]
    most_relateds = sorted(most_relateds, key=lambda x:-x[1])[:10]
    most_relateds = [(idx2vocab[idx], pmi_ij) for idx, pmi_ij in most_relateds]

    pprint(most_relateds)
    
    # most_smillar
    print(most_similar('C/C++', pmi, vocab2idx, idx2vocab))
    print(most_similar('땔감', pmi, vocab2idx, idx2vocab))
    print(most_similar('국비', pmi, vocab2idx, idx2vocab))
    print(most_similar('객체', pmi, vocab2idx, idx2vocab))
