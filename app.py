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
        elif self.size == 'duży' and self.rd != 'option1':
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
        if self.currency == 'EURO':
            self.value /= rate
        return lubuskie

    def wielkopolskie(self):
        if self.rd == 'option1' and self.size != 'mikro':
            naklady = 'nakladybr'
        elif self.size == 'duży' and self.rd != 'option1':
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
        cur = db.execute('select * from gminy where {} <= {} and wojewodztwo = "{}"'.format(naklady, self.value, 'wielkopolskie'))
        results = cur.fetchall()
        wielkopolskie = {}
        for i in range(len(results)):
            wielkopolskie[results[i]['gmina']] = results[i]['powiat']
        if self.currency == 'EURO':
            self.value /= rate
        return wielkopolskie

    def zachodniopomorskie(self):
        if self.rd == 'option1' and self.size != 'mikro':
            naklady = 'nakladybr'
        elif self.size == 'duży' and self.rd != 'option1':
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
        cur = db.execute('select * from gminy where {} <= {} and wojewodztwo = "{}"'.format(naklady, self.value, 'zachodniopomorskie'))
        results = cur.fetchall()
        zachodniopomorskie = {}
        for i in range(len(results)):
            zachodniopomorskie[results[i]['gmina']] = results[i]['powiat']
        if self.currency == 'EURO':
            self.value /= rate
        return zachodniopomorskie

    def gnl(self):
            db = get_db()
            cur = db.execute(
                'select * from gminy where wojewodztwo = "{}"'.format('lubuskie'))
            results = cur.fetchall()
            gminyl = {}
            if self.rd == 'option1' and self.size != 'mikro':
                for i in range(len(results)):
                    gminyl[results[i]['gmina']] = results[i]['nakladybr']
            elif self.size == 'duży' and self.rd != 'option1':
                for i in range(len(results)):
                    gminyl[results[i]['gmina']] = results[i]['naklady']
            elif self.size == 'średni' and self.rd != 'option1':
                for i in range(len(results)):
                    gminyl[results[i]['gmina']] = results[i]['nakladys']
            elif self.size == 'mały':
                for i in range(len(results)):
                    gminyl[results[i]['gmina']] = results[i]['nakladyma']
            else:
                for i in range(len(results)):
                    gminyl[results[i]['gmina']] = results[i]['nakladym']
            return gminyl

    def gnw(self):
            db = get_db()
            cur = db.execute(
                'select * from gminy where wojewodztwo = "{}"'.format('wielkopolskie'))
            results = cur.fetchall()
            gminyw = {}
            if self.rd == 'option1' and self.size != 'mikro':
                for i in range(len(results)):
                    gminyw[results[i]['gmina']] = results[i]['nakladybr']
            elif self.size == 'duży' and self.rd != 'option1':
                for i in range(len(results)):
                    gminyw[results[i]['gmina']] = results[i]['naklady']
            elif self.size == 'średni' and self.rd != 'option1':
                for i in range(len(results)):
                    gminyw[results[i]['gmina']] = results[i]['nakladys']
            elif self.size == 'mały':
                for i in range(len(results)):
                    gminyw[results[i]['gmina']] = results[i]['nakladyma']
            else:
                for i in range(len(results)):
                    gminyw[results[i]['gmina']] = results[i]['nakladym']
            return gminyw

    def gnz(self):
            db = get_db()
            cur = db.execute(
                'select * from gminy where wojewodztwo = "{}"'.format('zachodniopomorskie'))
            results = cur.fetchall()
            gminyz = {}
            if self.rd == 'option1' and self.size != 'mikro':
                for i in range(len(results)):
                    gminyz[results[i]['gmina']] = results[i]['nakladybr']
            elif self.size == 'duży' and self.rd != 'option1':
                for i in range(len(results)):
                    gminyz[results[i]['gmina']] = results[i]['naklady']
            elif self.size == 'średni' and self.rd != 'option1':
                for i in range(len(results)):
                    gminyz[results[i]['gmina']] = results[i]['nakladys']
            elif self.size == 'mały':
                for i in range(len(results)):
                    gminyz[results[i]['gmina']] = results[i]['nakladyma']
            else:
                for i in range(len(results)):
                    gminyz[results[i]['gmina']] = results[i]['nakladym']
            return gminyz


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

        result = defaultdict(list)
        for k, v in sorted(lubuskie.items()):
            result[v].append(k)

        resultw = defaultdict(list)
        for k, v in sorted(wielkopolskie.items()):
            resultw[v].append(k)

        resultz = defaultdict(list)
        for k, v in sorted(zachodniopomorskie.items()):
            resultz[v].append(k)

        value = '{:,}'.format(int(round(places.value, 2))).replace(',', ' ')

        zach = places.gnz()
        lub = places.gnl()
        wlkp = places.gnw()

        return render_template('index.html', result=result, resultw=resultw, resultz=resultz, rd=rd, value=value,
                               currency=places.currency, zach=zach, size=size, lub=lub, wlkp=wlkp)


if __name__ == '__main__':
    app.run()
