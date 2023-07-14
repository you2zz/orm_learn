import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

import or_

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)
    book = relationship("Book", backref="book")
    def __str__(self):
        return f'Publisher {self.id}: {self.name}'

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    sale = relationship("Sale", backref="sale")
    def __str__(self):
        return f'Stock {self.id}: {self.id_book}, {self.id_shop}, {self.count}'

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=250), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)    
    shop = relationship("Stock", backref="book")
    def __str__(self):
        return f'Book {self.id}: {self.title}'
    
class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True, nullable=False)
    book = relationship("Stock", backref="shop")
    def __str__(self):
        return f'Shop {self.id}: {self.name}'
    
class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(4, 2), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)    
    def __str__(self):
        return f'{self.price} | {self.date_sale}'

def create_tables(engine):
    Base.metadata.drop_all(engine) # удаляет данные из базы данных
    Base.metadata.create_all(engine) # создает таблицы

def get_sales(session, author_id = 0, publisher_name = ''):
    res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
          join(Publisher).join(Stock).join(Sale).join(Shop).\
          filter(or_(Publisher.id==author_id, Publisher.name.ilike(f'%{publisher_name}%')))

    for book, shop, price, count, date in res:
        print(f'{book: <40} | {shop: <10} | {price*count: <8} | {date.strftime("%d-%m-%Y")}')


# def get_sales(session, author_id = 0, publisher_name = ''):
#     if author_id != 0:
#         res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
#             join(Publisher).join(Stock).join(Sale).join(Shop).\
#             filter(Publisher.id==author_id)
#     else:
#         res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
#             join(Publisher).join(Stock).join(Sale).join(Shop).\
#             filter(Publisher.name.ilike(f'%{publisher_name}%'))
    

    for book, shop, price, count, date in res:
        print(f'{book: <40} | {shop: <10} | {price*count: <8} | {date.strftime("%d-%m-%Y")}')