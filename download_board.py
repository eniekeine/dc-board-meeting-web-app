import sys
import asyncio
import random
import re
import sqlite3
sys.path.insert(0, 'C:/Dropbox/Notes/컴퓨터/스크립팅 언어/파이선/라이브러리/dcinside-python3-api/repo')
import dc_api

last_id = sys.maxsize
board_id = "programming"
db_file_name = "dcinside_corpus.db"
db_table_name = "board_programming"
db_insert_query = f"INSERT INTO {db_table_name} (document_id, title, author, content, view_count, voteup_count, votedown_count, time) values (?, ?, ?, ?, ?, ?, ?, ?)"

strs = []
conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()
cursor.execute(f"SELECT MAX(document_id) FROM {db_table_name}")
document_id_begin = cursor.fetchone()[0]
if document_id_begin == None:
    document_id_begin = 1
else:
    document_id_begin = document_id_begin + 1
article_id_end = 2500000
i = 0

async def run(document_id_begin, count):
    async with dc_api.API() as api:
        for document_id in range(document_id_begin, article_id_end):
            global cursor
            global conn
            global i
            document = await api.document(board_id, document_id)
            if not document:
                continue
            print(document_id, document.title)
            cursor.execute(db_insert_query, (
                document_id, 
                document.author,
                document.title,
                document.contents, 
                document.view_count,
                document.voteup_count,
                document.votedown_count,
                document.time
                ))
            conn.commit()
            i += 1
            if count != -1 and i == count:
                break       

asyncio.run(run(document_id_begin, -1))

conn.close()
