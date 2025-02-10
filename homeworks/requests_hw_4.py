from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()
engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)



class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, nullable=False, default=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    product = relationship(Product, backref='category')





Base.metadata.create_all(engine)

with Session() as session:
    electronic = Category(name='electronic', description='Gadgets and devices')
    book = Category(name='book', description='"Print books and e-books')
    clothes = Category(name='clothes', description='Clothes for men and women')

    session.add_all([electronic, book, clothes])
    session.commit()


    smartphone = Product(name='Smartphone', price=299.99, in_stock=True, category_id=electronic.id)
    notebook = Product(name='Notebook', price=499.99, in_stock=True, category_id=electronic.id)
    sci_fi = Product(name='Sci-Fi', price=15.99, in_stock=True, category_id=book.id)
    jeans = Product(name='Jeans', price=40.50, in_stock=True, category_id=clothes.id)
    t_shirt = Product(name='T-shirt', price=20, in_stock=True, category_id=clothes.id)

    session.add_all([smartphone, notebook, sci_fi, jeans])
    session.commit()


    products = session.query(Category).all()
    for category in products:
        print(category.name, [prod.name for prod in category.product])
    print()


    phone = session.query(Product).filter(Product.name == 'Smartphone').first()
    if phone:
        phone.price = 349.99

    print(session.query(Product).filter(Product.name == 'Smartphone').first().price)
    print()

    count_by_category = session.query(Category.name, func.count(Product.id)).join(Product).group_by(Category.name).all()
    for a in count_by_category:
        print(a[0], a[1])
    print()

    count_by_category = session.query(Category.name, func.count(Product.id)).join(Product).group_by(Category.name).having(func.count(Product.id) > 1).all()
    for a in count_by_category:
        print(a[0], a[1])


