from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Index Page
class Home(Resource):
    def get(self):
        return "Welcome to the Sidakye Indicator Forecastor"



# This class would first check if the file already exists and scan through the text file 
# to detect the country given by the user. 
# If the file does not exist, it would be created and then the model would run, 
# produce the result, and then write it to the file.
class Indicators(Resource):
    def get(self, country):
        try:
            with open('indicator.txt', 'x') as f:
                # --- Model runs here and outputs result to variable which is stored in file ---
                forecast = 50.2354
                f.write(str({country:forecast}) + "\n")
                return jsonify({country:forecast})
        except FileExistsError:
            trigger = 0
            with open('indicator.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.find(country) != -1:
                        trigger = 1
                        return line

                if (trigger==0):
                    # --- Model runs here and outputs result to variable which is stored in file ---
                    forecast = 50.2354
                    with open('indicator.txt', 'a') as g:
                        g.write(str({country:forecast})+"\n")
                        return jsonify({country:forecast})



api.add_resource(Home, '/')
api.add_resource(Indicators, '/indicator/<string:country>')

app.run(host="0.0.0.0", port=81)