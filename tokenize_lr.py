from soynlp.tokenizer import LTokenizer
import pandas as pd

def tokenize_lr_sent(scores : dict[str, float], sent, flatten=False):
    tokenizer = LTokenizer(scores=scores)
    return tokenizer.tokenize(sent, flatten)
