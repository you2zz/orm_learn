import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)
    def __str__(self):
        return f'Publisher {self.id}: {self.name}'

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    def __str__(self):
        return f'Stock {self.id}: {self.id_book}, {self.id_shop}, {self.count}'

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=250), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship("Publisher", backref="book")
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
    stock = relationship("Stock", backref="sale")
    def __str__(self):
        return f'{self.price} | {self.date_sale}'

def create_tables(engine):
    Base.metadata.drop_all(engine) # удаляет данные из базы данных
    Base.metadata.create_all(engine) # создает таблицы