from soynlp.word import WordExtractor
from soynlp.utils import DoublespaceLineCorpus
import pandas as pd

def word_score_table_to_datafarme(word_score_table):
    rows = [
        (
            word,
            score.cohesion_forward,
            score.cohesion_backward,
            score.left_branching_entropy,
            score.right_branching_entropy,
            score.left_accessor_variety,
            score.right_accessor_variety,
            score.leftside_frequency,
            score.rightside_frequency
        ) for word, score in word_score_table.items()
    ]

    columns = [
        "word",
        "cohesion_forward",
        "cohesion_backward",
        "left_branching_entropy",
        "right_branching_entropy",
        "left_accessor_variety",
        "right_accessor_variety",
        "leftside_frequency",
        "rightside_frequency"
    ]

    # Create a sample DataFrame
    return pd.DataFrame(rows, columns=columns)

def save_to_csv(word_score_table, output_filename):
    word_score_table_to_datafarme(word_score_table).to_csv(output_filename, index=False)

def make_word_score_table(strs):
    word_extractor = WordExtractor(
        min_frequency=100,
        min_cohesion_forward=0.05, 
        min_right_branching_entropy=0.0
    )
    word_extractor.train(strs)
    return word_extractor.extract()

def load_word_score_data_frame_csv(filename):
    df : pd.DataFrame = pd.read_csv(filename,keep_default_na=False)
    return df