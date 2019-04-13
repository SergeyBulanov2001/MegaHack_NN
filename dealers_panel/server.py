from flask import Flask, send_from_directory
from flask_cors import CORS

import mysql.connector, json


app = Flask(__name__)
CORS(app,  supports_credentials=True)

conn = mysql.connector.connect(
            host='192.168.10.53',
            database='case2',
            user='sergey',
            password='IttC79QvArAKoeDe')
c = conn.cursor()


@app.route('/')
def web_application():
    return ''


@app.route('/authorization/<nickname>&<password>')
def authorization(nickname, password):
    c.execute("SELECT  * FROM dealers WHERE (nickname=%s and passwd='%s')" % (nickname, password))
    data = c.fetchone()

    if data == None:
        return '{"type": "error", "message":"Неправильный логин или пароль"}'

    return '{"type": "success", "token":"%s"}' % data[2]


def check_token(token):
    c.execute("SELECT nickname FROM dealers WHERE token='%s'" % token)
    data = c.fetchone()
    return data


@app.route('/<token>/stock/<name>&<services>&<conditions>', methods=['POST', 'GET'])
def stock_add(token, name, services, conditions):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'

    c.execute('INSERT INTO Stocks(dealer_id, stock_name, services, conditions, stats) VALUES (%s, "%s", %s, %s, "available")' % (nickname[0], name, json.dumps(services), json.dumps(conditions)))
    conn.commit()

    return '{"type": "success"}'


def get_tariff_name(id):
    try:
        c.execute("SELECT tariff_name FROM Tariffs WHERE tariff_id=%s" % int(json.loads(id)['tariff_id']))
        data = c.fetchall()
        return str(data[0][0])

    except:
        return None


@app.route('/<token>/stock_request', methods=['GET'])
def stock_request(token):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'

    try:
        c.execute("SELECT * FROM Stocks WHERE dealer_id=%s" % nickname[0])
        data = c.fetchall()

    except:
        return '[]'

    answer = []
    for i in data:
        answer.append(
            {'stock_id': i[0], 'dealer_id': i[1], 'stock_name': i[2], 'services': json.loads(i[3]), 'conditions': json.loads(i[4]), 'status': i[5], 'tariff_name': get_tariff_name(i[4])}
        )

    return str(answer).replace("'", '"')


@app.route('/<token>/closing_stock/<id>', methods=['DELETE', 'GET'])
def closing_stock(token, id):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'

    c.execute("UPDATE Stocks SET stats='closed' WHERE dealer_id= %s and stock_id= %s" % (nickname[0], id))
    conn.commit()

    return '{"type": "success"}'


@app.route('/<token>/tariffs')
def tariffs(token):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'

    try:
        c.execute("SELECT tariff_id, tariff_name FROM Tariffs")
        data = c.fetchall()

    except:
        return '[]'
    answer = []

    for i in data:
        answer.append({"id": i[0], "tariff_name": i[1]})

    return str(answer).replace("'", '"')


@app.route('/<token>/orders')
def requestOrders(token):
    id = check_token(token)[0]
    if id == ():
        return '{"type": "error", "message": "token error"}'
    c.execute("SELECT * FROM OrdersInfo WHERE dealer_id = %d" % int(id))
    a = c.fetchall()
    answer = []
    for obj in a:
        answer.append({"id": obj[0], "getDate": obj[1], "usernumber": obj[2], "orderInfo": obj[4], "result": obj[5], "finishDate": obj[6]})
    return str(answer).replace("'", '"')


if __name__ == '__main__':
    app.run(debug=False)
