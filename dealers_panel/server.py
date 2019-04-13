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


@app.route('/<token>/stock/name=<name>&<services>&<conditions>', methods=['POST', 'GET'])
def stock_add(token, name, services, conditions):
    nickname = check_token(token)
    if nickname == ():
        return '{"type": "error", "message": "token error"}'
    try:
        c.execute("""
            CREATE TABLE
            `stock_%s` (
            `id` INT(11) NOT NULL AUTO_INCREMENT,
            'name' TEXT NOT NULL
            
            PRIMARY KEY(`id`)
        )""" % nickname)
        conn.commit()
    except:
        pass

    c.execute('INSERT INTO `stock_%s` () VALUES ()' % (nickname))
    conn.commit()

    return '{"type": "success"}'




if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.53')