from flask import Flask, g, render_template, request
import sqlite3
from collections import defaultdict
import requests


app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('gminy.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def kurs():
    global kurs
    response = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/")
    data = response.json()
    dane = data['rates']
    kurs = dane[0]['mid']
    kurs = float(kurs)
    return kurs


def data():
    response = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/eur/")
    data = response.json()
    dane = data['rates']
    date = dane[0]['effectiveDate']
    return date

class Where:

    def __init__(self, currency, value, size, rd):
        self.currency = currency
        self.value = value
        self.size = size
        self.rd = rd



    def lubuskie(self):
        if self.currency == 'EURO':
            self.value *= rate
        db = get_db()
        cur = db.execute('select * from gminy where naklady =<"{}" and wojewodztwo="{}}"'.format(self.value, 'lubuskie'))
        results = cur.fetchall()
        lubuskie = {}
        for i in range(len(results)):
            lubuskie[results[i]['gmina']] = results[i]['powiat']
        return lubuskie

rate = kurs()
date = data()

@app.route('/', methods=['GET', 'POST'])
def index():

    value = 1
    currency = 1

    if currency == 'EURO':
        value *= kurs

    db = get_db()
    cur = db.execute('select * from gminy where naklady < 120000000 and wojewodztwo="lubuskie"')
    results = cur.fetchall()

    dic = {}
    for i in range(len(results)):
        dic[results[i]['gmina']] = results[i]['powiat']

    result = defaultdict(list)
    for k, v in sorted(dic.items()):
        result[v].append(k)

    return render_template('index.html', result=result, results=results)


if __name__ == '__main__':
    app.run()
