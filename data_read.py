import json

def get_keyword_file(keyword):
    with open(f"./data/keyword/{keyword}.json", "rt", encoding="utf-8") as file:
        table : dict = json.load(file)
        return table
