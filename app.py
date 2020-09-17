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
        if self.rd == 'option1' and self.size != 'mikro':
            naklady = 'nakladybr'
        if self.size == 'duży' and self.rd != 'option1':
            naklady = 'naklady'
        elif self.size == 'średni' and self.rd != 'option1':
            naklady = 'nakladys'
        elif self.size == 'mały':
            naklady = 'nakladyma'
        else:
            naklady = 'nakladym'
        if self.currency == 'EURO':
            self.value *= rate
        db = get_db()
        cur = db.execute('select * from gminy where {} <= {} and wojewodztwo = "{}"'.format(naklady, self.value, 'lubuskie'))
        results = cur.fetchall()
        lubuskie = {}
        for i in range(len(results)):
            lubuskie[results[i]['gmina']] = results[i]['powiat']
        # if self.currency == 'EURO':
        #     self.value /= rate
        return lubuskie

    def wielkopolskie(self):
        if self.size == 'duży':
            naklady = 'naklady'
        elif self.size == 'średni':
            naklady = 'nakladys'
        elif self.size == 'mały':
            naklady = 'nakladma'
        elif self.rd == 'TAK':
            naklady = 'nakladybr'
        else:
            naklady = 'nakladym'
        # if self.currency == 'EURO':
        #     self.value *= rate
        db = get_db()
        cur = db.execute('select * from gminy where naklady <= ? and wojewodztwo = ?', [naklady, 'wielkopolskie'])
        results = cur.fetchall()
        wielkopolskie = {}
        for i in range(len(results)):
            wielkopolskie[results[i]['gmina']] = results[i]['powiat']
        # if self.currency == 'EURO':
        #     self.value /= rate
        return wielkopolskie

    def zachodniopomorskie(self):
        if self.size == 'duży' and self.rd == 'NIE':
            naklady = 'naklady'
        elif self.size == 'średni' and self.rd == 'NIE':
            naklady = 'nakladys'
        elif self.size == 'mały':
            naklady = 'nakladma'
        elif self.rd == 'TAK' and self.size != 'mikro':
            naklady = 'nakladybr'
        else:
            naklady = 'nakladym'
        # if self.currency == 'EURO':
        #     self.value *= rate
        db = get_db()
        cur = db.execute('select * from gminy where naklady <= ? and wojewodztwo = ?', [naklady, 'zachodniopomorskie'])
        results = cur.fetchall()
        zachodniopomorskie = {}
        for i in range(len(results)):
            zachodniopomorskie[results[i]['gmina']] = results[i]['powiat']
        if self.currency == 'EURO':
            self.value /= rate
        return zachodniopomorskie


rate = kurs()
rate = float(round(rate, 2))
date = data()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        currency = request.form['currency']
        value = float(request.form['value'])
        value = value * 1000000
        size = request.form['size']
        rd = request.form['options']
        places = Where(currency=currency, value=value, size=size, rd=rd)


        lubuskie = places.lubuskie()
        wielkopolskie = places.wielkopolskie()
        zachodniopomorskie = places.zachodniopomorskie()

        # dic = {}
        # for i in range(len(results)):
        #     dic[results[i]['gmina']] = results[i]['powiat']

        result = defaultdict(list)
        for k, v in sorted(lubuskie.items()):
            result[v].append(k)

        resultw = defaultdict(list)
        for k, v in sorted(wielkopolskie.items()):
            resultw[v].append(k)

        resultz = defaultdict(list)
        for k, v in sorted(zachodniopomorskie.items()):
            resultz[v].append(k)

        return render_template('results.html', result=result, resultw=resultw, resultz=resultz, rd=rd)


if __name__ == '__main__':
    app.run()
