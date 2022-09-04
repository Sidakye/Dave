from flask import Flask, jsonify
from ..services.gdp_services import getAllGdp

BASE_ROUTE_GDP = '/gdp'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Dave GDP Forecast'

@app.route((BASE_ROUTE_GDP+'/all'), methods=['GET'])
def gdpAll():
    data = getAllGdp()
    payload = {
        'message': 'success',
        'code': 200,
        'body': data
    }

    return jsonify(payload)
 
if __name__ == '__main__':
    app.run()