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

@app.route('/api/addorder/usernumber=<usernumber>&order=<order>&status=<status>&dealer_id=<dealer_id>')
def addOrderToDB(usernumber, order, status, dealer_id):
    dInfo = datetime.strftime(datetime.now())
    cmd = "INSERT INTO OrdersInfo(getDate, usernumber, orderInfo, result,dealer_id) VALUES ('%s', '%s', '%s', '%s', %s)" %(dInfo, usernumber, order, status, dealer_id)
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

@app.route('/api/getorderinfo/token=<token>')
def orderListing(token):
    id = GetIdByToken(token)
    cmd = "SELECT * FROM OrdersInfo WHERE id='%s'" % id
    c.execute(cmd)
    matching = c.fetchall()
    result = '['
    for obj in matching:
        result = result+'{'+'id: '+ str(obj[0]) + ', date:' + str(obj[6]) + ', order: ' + str(obj[4]) + ', status:' + str(obj[5]) + '}, '
    result = result.replace(result[-2], '')
    result = result + ']'
    return result


def GetIdByToken(token):
    cmd = "SELECT nickname FROM dealers WHERE token='%s'" % str(token)
    c.execute(cmd)
    matching = c.fetchone()[0]
    return matching

orderListing('9a2RR8qlrf1i2fu74MJZKnJo5RiSwnV7')