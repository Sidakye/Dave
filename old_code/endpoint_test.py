from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        return jsonify({'message':'Welcome to the Sidakye Indicator Forecastor'})

class Indicators(Resource):
    def get(self, indicator, country):
        forecast = "Generated forecast from model"  # This portion would be replaced with the result from the model
        return jsonify({'Forecast for '+indicator+' about '+country:forecast})

api.add_resource(Home, '/')
api.add_resource(Indicators, '/indicator/<string:indicator>&<string:country>')

app.run(host="0.0.0.0", port=81)