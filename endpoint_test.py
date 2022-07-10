from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    return "Welcome to the Future!"

@app.route('/indicator=<indicator>&country=<country>&year=<year>', methods=['GET'])
def indicator_checker(indicator, country, year):
    userRequests = [indicator, country, year]
    result = "Indicator: " + userRequests[0] + ", Country: " + userRequests[1] + ", Year: " + userRequests[2]
    return result


app.run(host="0.0.0.0", port=81)