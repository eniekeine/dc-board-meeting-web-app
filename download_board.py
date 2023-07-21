import sys
import asyncio
import sqlite3
from dc_api import dc_api

last_id = sys.maxsize
board_id = "programming"
db_file_name = "dcinside_corpus.db"
db_table_name = "board_programming"
db_insert_query = f"INSERT INTO {db_table_name} (document_id, author, title, content, view_count, voteup_count, votedown_count, time) values (?, ?, ?, ?, ?, ?, ?, ?)"

async def run(id_begin = -1, id_end = -1):
    with sqlite3.connect(db_file_name) as conn:
        cursor = conn.cursor()
        if id_begin == -1: # id_beign이 -1인 경우 데이터베이스에서 마지막으로 저장한 문서 아이디에서 출발한다.
            cursor.execute(f"SELECT MAX(document_id) FROM {db_table_name}")
            id_begin = cursor.fetchone()[0] + 1
        async with dc_api.API() as api:
            if id_end == -1: # id_end가 -1인 경우 갤러리에 올라온 가장 최신 글까지 다운받는다.
                documentIndex : dc_api.DocumentIndex = await api.board(board_id).__anext__()
                id_end = int(documentIndex.id)
            for document_id in range(id_begin, id_end+1):
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

asyncio.run(run(-1, -1))
