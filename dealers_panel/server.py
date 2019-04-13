from flask import Flask, send_from_directory
from flask_cors import CORS

import mysql.connector


app = Flask(__name__)
CORS(app,  supports_credentials=True)

conn = mysql.connector.connect(
            host='192.168.10.53',
            database='case2',
            user='sergey',
            password='IttC79QvArAKoeDe')
c = conn.cursor(buffered=True)


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

    try:
        c.execute("""
                CREATE TABLE
                `stock_%s` (
                `name` TEXT NOT NULL,
                `services` TEXT NOT NULL,
                `conditions` TEXT NOT NULL,
                `state` TEXT NOT NULL,
                `id` INT(11) NOT NULL AUTO_INCREMENT,
                PRIMARY KEY(`id`)
            )""" % nickname[0])
        conn.commit()
    except:
        pass

    c.execute('INSERT INTO `stock_%s`(name, services, conditions, state) VALUES ("%s", "%s", "%s", "activist")' % (nickname[0], name, services, conditions))
    conn.commit()

    return '{"type": "success"}'


@app.route('/<token>/stock_request', methods=['GET'])
def stock_request(token):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'
    try:
        c.execute("SELECT * FROM stock_%s" % nickname[0])
        data = c.fetchall()
    except:
        return '[]'
    answer = []
    for i in data:
        answer.append({"name": i[0], "services": i[1], "conditions": i[2], "state": i[3], "id": i[4]})
    return str(answer).replace("'", '"')


if __name__ == '__main__':
    app.run(debug=True)