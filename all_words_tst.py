import requests
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from time import sleep

# engine = create_engine("sqlite+pysqlite:///allwords.db", echo=True)
# with Session(engine) as connect:
# with engine.connect() as connect:
    # selections = connect.execute(text("SELECT words from all_words ORDER BY RANDOM() LIMIT 1"))
    # print(selections)
    # print(type(selections))
    # for row in selections:
    #     y = row.words
    #     print(y)


    # connect.execute(text("CREATE TABLE IF NOT EXISTS all_words (words TEXT(55))"))
headers = {"content-type": "application/json"}
words = requests.get("https://random-word-api.herokuapp.com/all", headers=headers).json()
words = str(words)[1:-1]
words = words.replace(',','\n')
f = open('./data.txt', 'w')
f.write(words)
f.close()
# for word in words:
#     sleep(1)
#     connect.execute(text(f"INSERT INTO all_words VALUES (:word)"), {"word": word})
# connect.commit()
