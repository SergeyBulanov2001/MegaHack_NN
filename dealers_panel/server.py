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


@app.route('/<token>/stock_request', methods=['GET'])
def stock_request(token):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'

    try:
        c.execute("SELECT * FROM Stocks WHERE dealer_id=%s" % nickname[0])
        data = c.fetchall()
        print(data)

    except:
        return '[]'

    answer = '['
    for i in data:
        if answer != '[':
            answer += ','
        answer += '{"stock_id":' + str(i[0]) + ',"dealer_id":' + str(i[1]) + ',"stock_name":"' + str(i[2]) + '","services":' + str(i[3]) + ',"conditions":' + str(i[4]) + ',"status":"' + i[5] + '"}'
    answer += ']'

    return str(answer)


@app.route('/<token>/closing_stock/<id>', methods=['DELETE', 'GET'])
def closing_stock(token, id):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'

    c.execute('' % (nickname[0], id))






if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.53', port=5001)
