import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

WORDS_TABLE_NAME = 'words'
WORD_LEXICONS_TABLE_NAME = 'word_lexicons'

def ingest_word_list(source: str, lexicon: str):

    words = read_word_list(source)
    insert_words(words, lexicon, WORDS_TABLE_NAME, WORD_LEXICONS_TABLE_NAME)


def read_word_list(source: str) -> list:

    words = []
    with open(source, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip().upper()
            if not line:
                continue
            words.append(line)


    return words


def insert_words(words: list, lexicon: str, words_table: str, word_lexicons_table: str):
    conn = psycopg2.connect(
        host='localhost',
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )

    try:
        with conn:
            with conn.cursor() as cur:
                for word in words:
                    cur.execute(
                        f"""
                        INSERT INTO {words_table} (word, word_length) VALUES (%s, %s)
                        ON CONFLICT (word) DO NOTHING
                        """, (word, len(word))
                    )

                    cur.execute(
                        f"""
                        SELECT word_id FROM {words_table}
                        WHERE word = %s
                        """, (word,)
                    )

                    word_id = cur.fetchone()[0]
                    cur.execute(
                        f"""
                        INSERT INTO {word_lexicons_table} (word_id, lexicon) VALUES (%s, %s)
                        ON CONFLICT (word_id, lexicon) DO NOTHING
                        """, (word_id, lexicon)
                    )

    finally:
        conn.close()



if __name__ == '__main__':
    ingest_word_list('data/test_words.txt', 'test')
