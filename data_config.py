import json

def get_data_keyword_config():
    with open("./data/keyword_config.json", "rt", encoding="utf-8") as file:
        return json.load(file) # dictionary

def get_keywords():
    obj : dict = get_data_keyword_config()
    return [keyword["displayname"] for keyword in obj["keywords"]]
    
if __name__ == "__main__":
    print(get_data_keyword_config())
    print(get_keywords())
