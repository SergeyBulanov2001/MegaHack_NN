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

@app.route('/api/setaction/<MSISDN>&<dealer_id>&<stock_id>')
def setStock(MSISDN, dealer_id, stock_id):
    checkConditions(MSISDN, dealer_id, stock_id)

def checkConditions(MSISDN, dealer_id, stock_id):
    cmd = "SELECT conditions FROM %s WHERE id=%d" % ('stock_'+str(dealer_id), stock_id)
    c.execute(cmd)
    condition = c.fetchone()[0]
    print(condition)
    cmd = "SELECT tariff_id FROM users WHERE MSISDN='%s'" % (MSISDN)
    c.execute(cmd)
    tariff_id = c.fetchone()[0]
    cmd = "SELECT * FROM tariffs WHERE tariff_id = %d" % (tariff_id)
    c.execute(cmd)
    tariff_conditions = c.fetchone()
    print(tariff_conditions)

if __name__ == '__main__':
    app.run(debug=True)