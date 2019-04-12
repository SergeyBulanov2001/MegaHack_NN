import mysql.connector
from datetime import datetime
from flask import Flask
from flask_cors import CORS

conn = mysql.connector.connect(
    host='192.168.10.53',
    database= 'case2',
    user='sergey',
    password='IttC79QvArAKoeDe')

c = conn.cursor(buffered=True)

app = Flask(__name__)

@app.route('/api/addorder/usernumber=<usernumber>&order=<order>&status=<status>')
def addOrderToDB(usernumber, order, status):
    dInfo = datetime.strftime(datetime.now())
    cmd = "INSERT INTO OrdersInfo(getDate, usernumber, orderInfo, result) VALUES ('%s', '%s', '%s', '%s')" %(dInfo, usernumber, order, status)
    c.execute(cmd)
    cmd = "SELECT id FROM OrdersInfo WHERE getDate = '%s' AND usernumber = '%s' AND orderInfo = '%s'" %(dInfo, usernumber, order)
    c.execute(cmd)
    conn.commit()
    matching = c.fetchall()[-1][0]
    return matching

@app.route('/api/getorderinfo/id=<id>')
def checkOrder(id):
    cmd = "SELECT * FROM OrdersInfo WHERE id=%d" %(id)
    c.execute(cmd)
    result = c.fetchone()
    return result

def sdjfkdsj():
    cmd = "SELECT nickname FROM dealers WHERE token='%s'" % ('222')
    c.execute(cmd)
    print(c.fetchone())

sdjfkdsj()

