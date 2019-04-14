from flask import Flask
from flask_cors import CORS

import mysql.connector, json,time


conn = mysql.connector.connect(
    host='192.168.10.53',
    database='case2',
    user='sergey',
    password='IttC79QvArAKoeDe')
c = conn.cursor(buffered=True)


app = Flask(__name__)
CORS(app,  supports_credentials=True)


def get_tariff_name(id):
    c.execute("SELECT tariff_name FROM Tariffs WHERE tariff_id=%s" % id)
    data = c.fetchone()
    return str(data[0])


@app.route('/stock_request/<dealer_id>')
def stock_request(dealer_id):
    try:
        c.execute("SELECT * FROM Stocks WHERE dealer_id=%s" % dealer_id)
        data = c.fetchall()
    except:
        return '[]'

    answer = []
    for i in data:
        answer.append(
            {'stock_id': i[0], 'dealer_id': i[1], 'stock_name': i[2], 'services': json.loads(i[3]), 'conditions': json.loads(i[4]), 'status': i[5], 'tariff_name': get_tariff_name(json.loads(i[4])['tariff_id']), 'description': i[6]}
        )
    return str(answer).replace("'", '"')


@app.route('/user_request/<MSISDN>', methods=['GET'])
def user_request(MSISDN):
    try:
        c.execute("SELECT * FROM users WHERE MSISDN=%s" % MSISDN)
        data = c.fetchone()

        if data == ():
            return '{"type": "error", "message": "Номер не найден"}'

        answer = {'tariff_name': get_tariff_name(data[1]), 'balance': data[3], 'dealer': data[4]}
        return str(answer).replace("'", '"')

    except:
        return '{"type": "error", "message": "Номер не найден"}'


if __name__ == '__main__':
    app.run(debug=True)