# coding: utf-8

import sqlite3

db_name = 'test_sqlite.db'

def insert_one():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS
        stocks (date text, trans text, symbol text, qty real, price real)
        ''')
    cur.execute('''
        INSERT INTO stocks VALUES ('2006-01-06','SELL','RHAT',100,35.14)
        ''')
    conn.commit()
    conn.close


def select_all():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM stocks ORDER BY date'):
        print(row)


def select_test():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM stocks WHERE price > 10000 ORDER BY date')
    print(res.fetchone())
    res = cur.execute('SELECT * FROM stocks WHERE price = 35.14 ORDER BY date')
    print(res.fetchall())
    res = cur.execute('SELECT qty FROM stocks WHERE date = "2006-01-06" ORDER BY date')
    print(res.fetchone())


def update_one():
    pass


def main():
    # insert_one()
    # select_all()
    select_test()


if __name__ == '__main__':
    main()
