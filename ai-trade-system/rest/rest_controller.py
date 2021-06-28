from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


class RestController():
    def getAPI(self):
        return api

    def run(self):
        app.run(debug=True, host="127.0.0.1", port=4080)
