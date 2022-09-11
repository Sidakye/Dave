from flask import Flask, jsonify
from ..services.gdp_services import *

BASE_ROUTE_GDP = '/gdp'

use_all_gdp()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Dave GDP Forecast'

@app.route(('/gdp/all'), methods=['GET'])
def gdpAll():
    data = use_all_gdp()

    if data != None and len(data) > 0:
        payload = {
            'message': 'success',
            'code': 200,
            'body': data
        }
    else:
        payload = {
            'message': 'failed',
            'code': 404,
            'body': None
        }

    return jsonify(payload)
 
if __name__ == '__main__':
    app.run()