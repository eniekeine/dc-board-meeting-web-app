import json
import pandas as pd

# https://github.com/lovit/soynlp/blob/master/tutorials/wordextractor_lecture.ipynb
#   ...즐겨쓰는 방법 중 하나는 cohesion_forward에 right_branching_entropy를 곱하는 것으로,
#   (1) 주어진 글자가 유기적으로 연결되어 함께 자주 나타나고, 
#   (2) 그 단어의 우측에 다양한 조사, 어미, 혹은 다른 단어가 등장...
def examine(df : pd.DataFrame):
    df['score'] = df['cohesion_forward'] * df['right_branching_entropy']
    df = df.sort_values(
        by='score',
        ascending=False)
    return df