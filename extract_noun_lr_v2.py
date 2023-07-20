# 참고: https://github.com/lovit/soynlp/blob/master/tutorials/nounextractor-v2_usage.ipynb
# 참고: https://lovit.github.io/nlp/2018/05/08/noun_extraction_ver2/
from soynlp.noun import LRNounExtractor_v2
import pandas as pd

def noun_score_table_to_dataframe(nouns):
    columns =["word", "frequency", "score"]
    rows = [(noun, scores[0], scores[1]) for noun, scores in nouns.items()]
    df = pd.DataFrame(rows, columns=columns)

def make_noun_score_table(strs):
    noun_extractor = LRNounExtractor_v2(verbose=True, extract_compound=True)
    nouns : dict [str, (int, float)] = noun_extractor.train_extract(strs)
    return nouns

def save_noun_score_table_df(df_nouns, output_filename):
    df_nouns.to_csv(output_filename, index=False)

def load_noun_score_table(filename):
    df : pd.DataFrame = pd.read_csv(filename, keep_default_na=False)
    return df
    