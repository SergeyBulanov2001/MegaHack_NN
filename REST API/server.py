from flask import Flask
from flask_cors import CORS

import mysql.connector, json, urllib

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

@app.route('/api/setstock/<MSISDN>&<dealer_id>&<stock_id>')
def setStock(MSISDN, dealer_id,stock_id):
    cc = checkConditions(MSISDN, stock_id)
    ce = checkExistence(MSISDN)
    if cc and ce:
        response = urllib.request.urlopen('http://192.168.10.53:5002/api/addordertoquerry/usernumber=%s&dealer_id=%s&orderinfo=%s'%(MSISDN, dealer_id, 'Wht?'))
        return(response.read())
    else:
        return('{"type": error, "message": "Данные пользователя не совпадают с условиями услуги или он уе зарегистрирован"}')

@app.route('/api/checkstock/<MSISDN>')
def checkStock(MSISDN):
    cmd = "SELECT * FROM OrdersInfo WHERE usernumber = %d" % str(MSISDN)
    c.execute(cmd)
    data = c.fetchall()
    answer = []
    for obj in data:
        answer.append({"id": obj[0], "creationDate": obj[1], "MSISDN": int(obj[2]), "dealer_id": obj[3], "result": obj[5], "finishDate": obj[6]})
    print(str(answer).replace("'", '"'))
    return (str(answer).replace("'", '"'))

def checkConditions(MSISDN, stock_id):
    cmd = 'SELECT conditions FROM Stocks WHERE stock_id = %d' % int(stock_id)
    c.execute(cmd)
    cond = json.loads(c.fetchone()[0])
    ks = cond.keys()
    for obj in ks:
        cmd = "SELECT %s FROM users WHERE MSISDN=%d" % (str(obj), int(MSISDN))
        c.execute(cmd)
        bd = c.fetchone()[0]
        if obj == 'lifetime':
            s = bd + str(cond[obj])
            if eval(s):
                continue
            else:
                return False
        else:
            if bd >= cond[obj]:
                continue
            else:
                return False
    return True

def checkExistence(MSISDN):
    cmd = 'SELECT usernumber FROM OrdersInfo WHERE usernumber = %d' % int(MSISDN)
    c.execute(cmd)
    if c.fetchone() == ():
        return False
    else:
        return True

if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.53')