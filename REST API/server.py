from flask import Flask
from flask_cors import CORS

import mysql.connector, json, urllib
from datetime import datetime

app = Flask(__name__)
CORS(app,  supports_credentials=True)

conn = mysql.connector.connect(
            host='192.168.10.53',
            database='case2',
            user='sergey',
            password='IttC79QvArAKoeDe')
c = conn.cursor()

@app.route('/')
def web_application():
    pass

@app.route('/api/stock/add/<MSISDN>&<dealer_id>&<stock_id>')
def setStock(MSISDN, dealer_id,stock_id):
    conn.cmd_reset_connection()
    orderInfo = GetStockName(stock_id)
    cc = checkConditions(MSISDN, stock_id)
    print(cc)
    ce = checkExistence(MSISDN, orderInfo)
    print(ce)
    cd = checkDealer(MSISDN, dealer_id)
    print(cd)
    if cc and ce and cd:
        response = urllib.request.urlopen('http://192.168.10.53:5002/api/addordertoquerry/usernumber=%s&dealer_id=%s&orderinfo=%s'%(MSISDN, dealer_id, str(orderInfo).encode('utf-8')))
        addStocksToUser(MSISDN,stock_id)
        print(response)
        return ('{"type": "success", "message": "Пользователь успешно создан"}')
    else:
        return('{"type": "error", "message": "Данные пользователя не совпадают с условиями услуги/Он уже зарегистрирован/Выбран не ваш диллер"}')

@app.route('/api/stock/status/<MSISDN>')
def checkStock(MSISDN):
    conn.cmd_reset_connection()
    cmd = "SELECT * FROM OrdersInfo WHERE usernumber = %d" % str(MSISDN)
    c.execute(cmd)
    data = c.fetchall()
    answer = []
    for obj in data:
        answer.append({"id": obj[0], "creationDate": obj[1], "MSISDN": int(obj[2]), "dealer_id": obj[3],"orderInfo": obj[4], "result": obj[5], "finishDate": obj[6]})
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
            time = datetime.strptime(bd, '%Y.%m.%d') - datetime.strptime(datetime.today().strftime('%Y.%m.%d'), '%Y.%m.%d')
            s = str(time.days)
            if eval(s):
                continue
            else:
                return False
        else:
            if bd >= cond[obj]:
                continue
            else:
                print(obj)
                print(str(bd) + '  ' + str(cond[obj]))
                return False
    return True

def addStocksToUser(MSISDN, stock_id):
    conn.cmd_reset_connection()
    cmd = "SELECT connected_stocks FROM users WHERE MSISDN=%d" % int(MSISDN)
    c.execute(cmd)
    connected_stocks = c.fetchone()
    print(connected_stocks[0])
    if connected_stocks[0] == 'null':
        toadd = "{'stocks': [%d]}" % int(stock_id)
        toadd = str(toadd).replace("'", '"')
        print(json.dumps(toadd))
        cmd = "UPDATE users SET connected_stocks='%s' WHERE MSISDN = %d" % (toadd, int(MSISDN))
        c.execute(cmd)
        conn.commit()
        return '{"type": "success", "message":"Пользователь успешно зарегистрирован"}'
    else:
        connected_stocks = connected_stocks[0]
        arr = json.loads(str(connected_stocks))['stocks']
        if stock_id in arr:
            return 'error'

        arr.append(int(stock_id))
        toadd = '{"stocks": %s}' % arr
        cmd = "UPDATE users SET connected_stocks='%s' WHERE MSISDN = %d" % (toadd, int(MSISDN))
        c.execute(cmd)
        conn.commit()
        return '{"type": "success", "message":"Пользователь успешно зарегистрирован"}'

@app.route('/api/stock/get/<MSISDN>')
def getUserStocks(MSISDN):
    conn.cmd_reset_connection()
    cmd = "SELECT connected_stocks FROM users WHERE MSISDN=%d" % int(MSISDN)
    c.execute(cmd)
    matching = c.fetchone()
    if matching[0] == 'null':
        return '{"type": "error", "message": "У пользователя нет подключеныйх акций"}'
    answer = json.loads(matching[0])
    return '{"type": "success", "message": %s}' % answer["stocks"]

def checkExistence(MSISDN, orderInfo):
    cmd = 'SELECT usernumber FROM OrdersInfo WHERE usernumber = %d AND orderInfo = "%s"' % (int(MSISDN), orderInfo)
    c.execute(cmd)
    if c.fetchone() == ():
        return False
    else:
        return True

def checkDealer(MSISDN, dealer_id):
    cmd = 'SELECT dealer FROM users WHERE MSISDN = %d' % int(MSISDN)
    c.execute(cmd)
    id = c.fetchone()[0]
    print(id)
    print(dealer_id)
    if int(id) == int(dealer_id):
        return True
    else:
        return False

def GetStockName(stock_id):
    cmd = 'SELECT stock_name FROM Stocks WHERE stock_id = %d' % int(stock_id)
    c.execute(cmd)
    return c.fetchone()

if __name__ == '__main__':
    app.run(debug=True, host='192.168.10.53')