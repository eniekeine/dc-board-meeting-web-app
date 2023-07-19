import json
import re
from word_over_date import WordOverDateContext, word_over_date, word_over_date_regex

pattern = re.compile("c\+\+|C\+\+")
context = WordOverDateContext(group_pattern="%Y")
table = word_over_date_regex(pattern, context)
with open("./data/keyword/c++.json", "wt", encoding="utf-8") as file:
    json.dump(table, file)
