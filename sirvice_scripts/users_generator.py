import random, mysql.connector
from datetime import datetime


def MSISDN_generator():
    alphabet = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    MSISDN = ''
    for _ in range(10):
        MSISDN += alphabet[random.randint(0, 9)]
    return MSISDN

def GenerateUsers():
    conn = mysql.connector.connect(
        host='192.168.10.53',
        database='case2',
        user='sergey',
        password='IttC79QvArAKoeDe')
    c = conn.cursor(buffered=True)

    for i in range(10):
        cmd = "INSERT INTO users(MSISDN, tariff_id, lifetime, balance) VALUES(%s, %d, '%s', %s)" % (
            MSISDN_generator(),
            random.randint(1,3),
            datetime.strftime(datetime.now(), "%Y.%m.%d"),
            random.random() * random.randint(50,500)
        )
        c.execute(cmd)
    conn.commit()
    conn.close()

GenerateUsers()