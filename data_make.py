import json
import re
from word_over_date import WordOverDateContext, word_over_date_regex
from data_config import get_data_keyword_config, get_keywords

config : dict = get_data_keyword_config()
keywords = get_keywords()

def make_keyword_file(keyword : dict):
    displayname : str = keyword["displayname"]
    pattern : str = keyword["pattern"]
    compiled_pattern : re.Pattern = re.compile(pattern)
    context = WordOverDateContext(group_pattern="%Y")
    table = word_over_date_regex(compiled_pattern, context)
    with open(f"./data/keyword/{displayname}.json", "wt", encoding="utf-8") as file:
        json.dump(table, file)

for keyword in config["keywords"]:
    make_keyword_file(keyword)
