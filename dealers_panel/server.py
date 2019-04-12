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
    pass


@app.route('/authorization/<nickname>&<password>')
def authorization(nickname, password):
    c.execute("SELECT  * FROM dealers WHERE (nickname=%s and passwd='%s')" % (nickname, password))
    data = c.fetchone()

    if data == None:
        return '{"type": "error", "message":"wrong login or password"}'

    return '{"type": "success", "token":"%s"}' % data[2]


def check_token(token):
    c.execute("SELECT nickname FROM dealers WHERE token='%s'" % token)
    data = c.fetchone()
    return data


@app.route('/<token>/stock/<options>', methods=['POST', 'GET'])
def stock_add(token, options):
    nickname = check_token(str(token))
    print(nickname)
    if nickname == ():
        return str({"type": "error", "message": "token error"})

    c.execute("CREATE TABLE '%s'()" % nickname)
    conn.commit()

    return None




if __name__ == '__main__':
    app.run(debug=True)