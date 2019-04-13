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
c = conn.cursor(buffered=True)

@app.route('/')
def web_application():
    pass

@app.route('/api/setaction/<MSISDN>&<dealer_id>&<stock_id>')
def setStock(MSISDN, dealer_id, stock_id):
    checkConditions(MSISDN, dealer_id, stock_id)

def checkConditions(MSISDN, stock_id):
    cmd = 'SELECT conditions FROM Stocks WHERE stock_id = %d' % stock_id
    c.execute(cmd)
    cond = json.loads(c.fetchone()[0])
    ks = cond.keys()
    for obj in ks:
        cmd = "SELECT %s FROM users WHERE MSISDN=%d" % (str(obj), MSISDN)
        c.execute(cmd)
        print(obj)
        print(c.fetchone()[0])
        #if cond[str(obj)]

checkConditions(9096758988,11)

if __name__ == '__main__':
    app.run(debug=True)