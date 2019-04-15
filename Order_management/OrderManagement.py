import mysql.connector
from datetime import datetime
from flask import Flask
from flask_cors import CORS

import random, threading

conn = mysql.connector.connect(
    host='192.168.10.53',
    database= 'case2',
    user='sergey',
    password='IttC79QvArAKoeDe')

c = conn.cursor()

orders = []

app = Flask(__name__)
CORS(app,  supports_credentials=True)
@app.route('/api/addordertoquerry/usernumber=<usernumber>&dealer_id=<dealer_id>&orderinfo=<orderinfo>')
def addOrderToQuerry(usernumber, dealer_id, orderinfo):
    curDate = datetime.strftime(datetime.now(), "%Y.%m.%d")
    orders.append([curDate, usernumber, dealer_id, orderinfo])
    return '{"type": "success"}'


def Inserter():
    while True:
        for obj in orders:
            failChance = random.randint(0,9)
            if failChance == 1:
                status = 'error'
            else:
                status = 'success'

            cmd = "INSERT INTO OrdersInfo(getDate, usernumber, dealer_id, orderInfo, result, finishDate) VALUES ('%s', '%s', %d, '%s', '%s', '%s')" % (
                obj[0], obj[1], int(obj[2]), obj[3], status, datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
            )
            c.execute(cmd)
            cmd = "SELECT result FROM OrdersInfo WHERE getDate='%s' and usernumber='%s' and orderInfo='%s'" % (
                obj[0], obj[1], obj[3]
            )
            c.execute(cmd)
            conn.commit()
            result = c.fetchone()[0]
            if result == 'success':
                del orders[orders.index(obj)]
            else:
                return

inserterProcess = threading.Thread(target=Inserter, name= 123)
inserterProcess.start()

if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.53', port=5002)