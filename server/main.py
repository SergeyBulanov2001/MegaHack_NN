from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api


import mysql.connector


app = Flask(__name__)
cors = CORS(app,  supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
api = Api(app)





if __name__ == '__main__':
    app.run(debug=True)