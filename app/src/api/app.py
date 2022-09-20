from flask import Flask, jsonify, request
from ..services.gdp_services import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Dave GDP Forecast'

@app.route('/gdp/one/')
def gdpOneByName():
    country_name = request.args.get('country_name')

    payload = None

    if country_name != None:
        data = use_gdp_by_country_name(country_name)

        payload = {
            'message': 'success',
            'code': 200,
            'body': data
        }
    else:
        data = use_gdp_by_country_name('Aruba')
        payload = {
            'message': 'success: no country selected, using default',
            'code': 200,
            'body': data
        }

    return jsonify(payload)
 
if __name__ == '__main__':
    app.run()