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

c = conn.cursor(buffered=True)

orders = []

app = Flask(__name__)

@app.route('/api/addordertoquerry/usernumber=<usernumber>&dealer_id=<dealer_id>&orderinfo=<orderinfo>')
def addOrderToQuerry(usernumber, dealer_id, orderinfo):
    getDate = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    orders.append([getDate, usernumber, dealer_id, orderinfo])


def Inserter():
    while True:
        for obj in orders:
            failChance = random.randint(9)
            if failChance == 1:
                status = 'error!'
            else:
                status = 'succes!'

            cmd = "INSERT INTO OrdersInfo(getDate, usernumber, dealer_id, orderInfo, result) VALUES ('%s', '%s', %d, '%s', '%s')" % (
                obj[0], obj[1], obj[2], obj[3], obj[4]
            )
            c.execute(cmd)
            conn.commit()
            cmd = "SELECT result FROM OrdersInfo WHERE getDate='%s' and usernumber='%s' and orderInfo='%s'" % (
                obj[0], obj[1], obj[3]
            )
            c.execute(cmd)
            result = c.fetchone()[0]
            if result == 'succes!':
                del orders[orders.index(obj)]
            else:
                return

inserterProcess = threading.Thread(target=Inserter, name= 123)
inserterProcess.start()

if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.53', port=5002)