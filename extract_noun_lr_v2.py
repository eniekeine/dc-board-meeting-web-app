# 참고: https://github.com/lovit/soynlp/blob/master/tutorials/nounextractor-v2_usage.ipynb
# 참고: https://lovit.github.io/nlp/2018/05/08/noun_extraction_ver2/
from soynlp.noun import LRNounExtractor_v2
from soynlp.utils import DoublespaceLineCorpus
import pandas as pd

if __name__ == "__main__":
    columns =["명사", "빈도수", "명사 가능 점수"]

    noun_extractor = LRNounExtractor_v2(verbose=True, extract_compound=True)

    corpus_fname = 'corpus_merged.txt'
    sentences = DoublespaceLineCorpus(corpus_fname, iter_sent=True)
    len(sentences)

    nouns : dict [str, (int, float)] = noun_extractor.train_extract(sentences)

    # Create a sample DataFrame
    df = pd.DataFrame([], columns=columns)
    for noun, scores in nouns.items():
        df.loc[len(df)] = (noun, ) + scores
    
    # Save DataFrame to Excel
    df.to_excel('noun_extract_lr_v2.xlsx', index=False)
