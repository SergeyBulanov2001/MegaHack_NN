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


if __name__ == '__main__':
    app.run(debug=True)