# 참고: https://github.com/lovit/soynlp/blob/master/tutorials/nounextractor-v1_usage.ipynb
from soynlp.noun import LRNounExtractor
from soynlp.utils import DoublespaceLineCorpus
import pandas as pd

if __name__ == "__main__":
    rows = []
    columns =["명사", "빈도수", "명사 가능 점수", "점수2"]

    noun_extractor = LRNounExtractor(
        max_left_length=10, 
        max_right_length=7,
        predictor_fnames=None,
        verbose=True
    )   

    corpus_fname = 'corpus_merged.txt'
    sentences = DoublespaceLineCorpus(corpus_fname, iter_sent=True)
    len(sentences)

    nouns : dict [str, (int, float, float)] = noun_extractor.train_extract(
        sentences,
        min_noun_score=0.3,
        min_noun_frequency=20
    )

    # Create a sample DataFrame
    df = pd.DataFrame(rows, columns=columns)
    for noun, scores in nouns.items():
        df.loc[len(df)] = (noun, ) + scores
    
    # Save DataFrame to Excel
    df.to_excel('noun_extract_lr.xlsx', index=False)
