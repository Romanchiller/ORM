import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
import tables as t


if __name__ == '__main__':

    DSN = input('Введите DSN: ')
    engine = sq.create_engine(DSN)
    t.create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', encoding="utf-8") as f:
        data = json.load(f)
        for el in data:
            if el['model'] == 'publisher':
                obj = t.Publisher(name=el['fields']['name'])
                session.add(obj)
            if el['model'] == 'book':
                obj = t.Book(name=el['fields']['title'], id_publisher=el['fields']['id_publisher'])
                session.add(obj)
            if el['model'] == 'stock':
                obj = t.Stock(id_book=el['fields']['id_book'], id_shop=el['fields']['id_shop'], count=el['fields']['count'])
                session.add(obj)
            if el['model'] == 'sale':
                obj = t.Sale(price=el['fields']['price'], date_sale=el['fields']['date_sale'], count=el['fields']['count'], id_stock=el['fields']['id_stock'])
                session.add(obj)
            if el['model'] == 'shop':
                obj = t.Shop(name=el['fields']['name'])
                session.add(obj)
    session.commit()

    find_name = input("Введите имя издателя:")

    for book, shop, price, count, date_sale in session.query(t.Book.name, t.Shop.name, t.Sale.price, t.Sale.count, t.Sale.date_sale).join(t.Publisher.book).join(t.Stock).join(t.Sale).join(t.Shop).filter(t.Publisher.name == 'Pearson').all():
        print(f'{book} | {shop} | {price*count} | {date_sale}')

    session.close()


