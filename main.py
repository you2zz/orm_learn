import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import create_tables, Publisher, Stock, Book, Shop, Sale

load_dotenv()

login = os.getenv('LOGIN_POSTGRESQL')
password = os.getenv('PASSWORD_POSTGRESQL')
data_base = os.getenv('DATA_BASE_NAME')

DSN = f'postgresql://{login}:{password}@localhost:5432/{data_base}'
engine = sqlalchemy.create_engine(DSN)

if __name__ == "__main__":
    # создаем таблицы
    create_tables(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # заполняем данными
    with open('files/tests_data.json', 'r') as fd:
        data = json.load(fd)
    
    for record in data:       
        model = {
            'publisher': Publisher,
            'book': Book,
            'shop': Shop,            
            'stock': Stock,
            'sale': Sale
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
 
    session.commit()

    # ишем факты покупки книг у издателя
    search_pub_id = int(input()) # вводится id издателя 

    subq = session.query(Publisher).filter(Publisher.id == search_pub_id).subquery()
    subq_1 = session.query(Book).join(subq).subquery()
    subq_2 = session.query(Stock).join(subq_1, Stock.id_book == subq_1.c.id).subquery()
    subq_3 = session.query(Shop).join(subq_2, Shop.id == subq_2.c.id_shop).subquery()
    search_res = session.query(Sale, subq_1.c.title, subq_3.c.name).join(subq_2, Sale.id_stock == subq_2.c.id).join(subq_1). join(subq_3)
    
    for s in search_res:
        print(f'{s[1]} | {s[2]} | {s[0]}')

    session.close()