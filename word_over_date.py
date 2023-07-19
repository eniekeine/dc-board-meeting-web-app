import re
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

db_file_name = "dcinside_corpus.db"
db_table_name = "board_programming"
class WordOverDateContext:
    def __init__(self, group_pattern : str):
        """
        Args:
            group_pattern (str):
                - "%Y-%m-%d %H-%M-%S" : 연-월-일 시:분:초 별로. 사실상 각 게시글 마다 항목이 생긴다.
                - "%Y-%m-%d" : 날짜별로
                - "%Y-%m" : 월별로
                - "%Y" : 연별로
        """
        self.group_pattern = group_pattern
WORD_OVER_DATE_DEFAULT_CONTEXT = WordOverDateContext("%Y-%m-%d")
class CounterTextMatch:
    def __init__(self, keyword):
        self.keyword = keyword
    def __call__(self, text : str):
        return text.count(self.keyword)
def word_over_date(
        keyword :str, 
        context : WordOverDateContext = WORD_OVER_DATE_DEFAULT_CONTEXT):
    return impl_word_over_date(CounterTextMatch(keyword), context)
class CounterRegexPattern:
    def __init__(self, re_pattern : re.Pattern):
        self.re_pattern = re_pattern
    def __call__(self, text : str):
        return len(self.re_pattern.findall(text))
def word_over_date_regex(
        re_pattern : re.Pattern, 
        context : WordOverDateContext = WORD_OVER_DATE_DEFAULT_CONTEXT):
    return impl_word_over_date(CounterRegexPattern(re_pattern), context)
def impl_word_over_date(
        fp_counter : callable, 
        context : WordOverDateContext = WORD_OVER_DATE_DEFAULT_CONTEXT):
    table = {}
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        # columns : 'document_id', 'author', 'title', 'content', 'view_count', 'voteup_count', 'votedown_count', 'time'
        # DB에 저장할 때 실수로 author와 title의 순서를 바꿔먹었으므로 다음 줄은 사실 time, title, content를 가져오는 내용임
        cursor.execute(f"SELECT time, author, content FROM {db_table_name} WHERE document_id <= 600000")
        records : list[tuple[str, str, str]] = cursor.fetchall()
        print("fetched record count : ", len(records))
        for time, title, content in records:
            parsed_time : datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            key = None
            if context and context.group_pattern:
                # 사용자가 그룹 기준을 제시한 경우 그 기준을 사용.
                key = parsed_time.strftime(context.group_pattern)
            else:    
                # 아니면 날별로 그룹
                key = parsed_time.strftime("%Y-%m-%d")
            count = 0 if key not in table else table[key]
            count = count + fp_counter(title)
            count = count + fp_counter(content)
            if count == 0:
                continue
            table[key] = count
    return table

if __name__ == "__main__":
    def test1():
        table = word_over_date("C++")
        print(table)
    def test2():
        pattern = re.compile("c\+\+|C\+\+")
        table2 = word_over_date_regex(pattern)
        print(table2)
    def plot_table(table):
            plt.style.use('_mpl-gallery')
            fig, ax = plt.subplots()
            # ax.bar(table.keys(), table.values(), width=1, edgecolor="white", linewidth=0.7)
            ax.plot(table.keys(), table.values())
            # set plot title
            plt.title('C++ appearances', fontsize=10)
            # set x-axis label
            plt.xlabel('year', fontsize=8)
            # set y-axis label
            plt.ylabel('count', fontsize=8)
            # alternate option without .gcf
            plt.subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.9)
            plt.show()
    def test3():
        pattern = re.compile("c\+\+|C\+\+")
        context = WordOverDateContext(group_pattern="%Y")
        table2 = word_over_date_regex(pattern, context)
        plot_table(table2)
    test3()
