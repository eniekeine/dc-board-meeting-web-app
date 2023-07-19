import json

def get_keywords():
    with open("./data/keyword_config.json", "rt", encoding="utf-8") as file:
        obj = json.load(file)
        return [keyword["displayname"] for keyword in obj["keywords"]]
def get_keyword_record(keyword):
    with open(f"./data/keyword/{keyword}.json", "rt", encoding="utf-8") as file:
        table : dict = json.load(file)
        return table
    
if __name__ == "__main__":
    print(get_keywords())
