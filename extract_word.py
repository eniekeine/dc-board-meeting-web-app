from soynlp.word import WordExtractor
import pandas as pd

def save_to_excel(word_score_table):
    rows = []
    columns =["word",
    "cohesion_forward",
    "cohesion_backward",
    "left_branching_entropy",
    "right_branching_entropy",
    "left_accessor_variety",
    "right_accessor_variety",
    "leftside_frequency",
    "rightside_frequency"]
    for word, score in word_score_table.items():
        rows.append([word,
        str(score.cohesion_forward),
        str(score.cohesion_backward),
        str(score.left_branching_entropy),
        str(score.right_branching_entropy),
        str(score.left_accessor_variety),
        str(score.right_accessor_variety),
        str(score.leftside_frequency),
        str(score.rightside_frequency)])
    # Create a sample DataFrame
    df = pd.DataFrame(rows, columns=columns)
    # Save DataFrame to Excel
    df.to_excel('word_score_table.xlsx', index=False)

def convet_to_csv(word_score_table):
    # csv 파일로 전부 추출
    with open("word_score_table.csv", "wt", encoding="UTF-8") as file:
        # file.write(json.dumps(word_score_table, indent=4, ensure_ascii=False))
        file.write("word")
        file.write(", cohesion_forward")
        file.write(", cohesion_backward")
        file.write(", left_branching_entropy")
        file.write(", right_branching_entropy")
        file.write(", left_accessor_variety")
        file.write(", right_accessor_variety")
        file.write(", leftside_frequency")
        file.write(", rightside_frequency")
        file.write('\n')
        for word, score in word_score_table.items():
            file.write(word)
            file.write(', ')
            file.write(str(score.cohesion_forward))
            file.write(', ')
            file.write(str(score.cohesion_backward))
            file.write(', ')
            file.write(str(score.left_branching_entropy))
            file.write(', ')
            file.write(str(score.right_branching_entropy))
            file.write(', ')
            file.write(str(score.left_accessor_variety))
            file.write(', ')
            file.write(str(score.right_accessor_variety))
            file.write(', ')
            file.write(str(score.leftside_frequency))
            file.write(', ')
            file.write(str(score.rightside_frequency))
            file.write('\n')


board_id = "programming"
db_file_name = "dcinside_corpus.db"
db_table_name = "board_programming"
strs = None
# 파일로 추출
with open("corpus_merged.txt", "rt", encoding='utf-8') as file:
    strs=file.readlines()
# 훈련
word_extractor = WordExtractor(
    min_frequency=100,
    min_cohesion_forward=0.05, 
    min_right_branching_entropy=0.0
)
word_extractor.train(strs)
# 추출
word_score_table = word_extractor.extract()
# 저장
save_to_excel(word_score_table)
