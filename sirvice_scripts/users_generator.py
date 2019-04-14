import random, mysql.connector
from datetime import datetime


def MSISDN_generator():
    alphabet = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    MSISDN = '9'
    for _ in range(9):
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
        cmd = "INSERT INTO users(MSISDN, tariff_id, lifetime, balance, dealer) VALUES(%s, %d, '%s', %s, %d)" % (
            MSISDN_generator(),
            random.randint(1,3),
            datetime.strftime(datetime.now(), "%Y.%m.%d"),
            round(random.random() * random.randint(500,5000), 2),
            random.randint(1,2)
        )
        c.execute(cmd)
    conn.commit()
    conn.close()

GenerateUsers()