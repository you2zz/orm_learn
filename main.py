import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import get_sales, create_tables, Publisher, Stock, Book, Shop, Sale

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
  
    q = input('Введите id или название издателя: ')
    if q.isdigit():
        get_sales(session=session, author_id=int(q))
    else:
        get_sales(session=session, publisher_name=q)
    
    session.close()