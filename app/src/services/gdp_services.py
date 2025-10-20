import sys
from os import path
from ..models.gdp_models import *
from ..models.inflation_models import *
from ..models.unemployment_models import *
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Resolve paths relative to this file so the service works when launched from repo root
BASE_DIR = path.abspath(path.join(path.dirname(__file__), '..', '..', '..'))
MODEL_PATH_DICT = {
    'low': path.join(BASE_DIR, 'saved_models', 'gdp', 'v1', 'low_income_v1.h5'),
    'lower-middle': path.join(BASE_DIR, 'saved_models', 'gdp', 'v1', 'low_mid_income_v1.h5'),
    'upper-middle': path.join(BASE_DIR, 'saved_models', 'gdp', 'v1', 'upp_mid_income_v1.h5'),
    'high': path.join(BASE_DIR, 'saved_models', 'gdp', 'v1', 'high_income_v1.h5')
}

DATA_PATH = path.join(BASE_DIR, 'data', 'gdp', 'gdp_data_complete_v2.xlsx')

# Simple caches to avoid re-loading models/scalers on every request
_MODEL_CACHE = {}
_SCALER_CACHE = {}

def get_scaler(income_level: str):
    if income_level in _SCALER_CACHE:
        return _SCALER_CACHE[income_level]

    if not path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

    data = pd.read_excel(DATA_PATH, sheet_name='data shift wout null', index_col='Year')
    df = data[data['IncomeLevel'] == income_level]

    scY = StandardScaler()
    scY.fit(df['GDP'].values.reshape(-1, 1))
    _SCALER_CACHE[income_level] = scY
    return scY


def make_prediction_by_name(country_name: str, prev_year: int, income_level: str):
    prediction = None
    try:
        # load model from cache or disk
        model_path = MODEL_PATH_DICT.get(income_level)
        if model_path is None or not path.exists(model_path):
            raise FileNotFoundError(f"Model for income level '{income_level}' not found at {model_path}")

        if income_level in _MODEL_CACHE:
            model = _MODEL_CACHE[income_level]
        else:
            model = load_model(model_path)
            _MODEL_CACHE[income_level] = model

        inflation = get_inflation_by_year(country_name, prev_year)
        unemployment = get_unemployment_by_year(country_name, prev_year)

        if inflation is None:
            print('Cannot forecast, inflation data unavailable', file=sys.stderr)
            return None

        if unemployment is None:
            print('Cannot forecast, unemployment data unavailable', file=sys.stderr)
            return None

        # Expecting scalars or arrays; ensure the shape matches what the model expects
        unscaled_prediction = model.predict(((inflation, unemployment),))

        if unscaled_prediction is not None:
            scY = get_scaler(income_level)
            # keras returns numpy arrays; extract scalar value
            pred_value = float(unscaled_prediction[0][0])
            # inverse transform expects 2D array
            pred_unscaled = scY.inverse_transform([[pred_value]])
            return float(pred_unscaled[0][0])
    except Exception as e:
        print('Failed to make prediction', e, file=sys.stderr)
        return None

def use_gdp_by_country_name(name: str) -> dict:
    data = {
        'country_id': 0,
        'country_name': '',
        'income_level': '',
        'gdp_actual': {
            'years': [],
            'gdp': [],
        },
        'gdp_predict': {
            'years': [],
            'gdp': [],
        },
    }
    try:
        country = get_country_details_by_name(name)
        if(country is not None):
            data['country_id'] = country[0]
            data['country_name'] = country[1]
            data['income_level'] = country[2]
        
        gdp_acutal_list = get_gdp_by_country_name(country[1])

        if(gdp_acutal_list is not None) and (len(gdp_acutal_list) > 0):
            for value in gdp_acutal_list:
                year = value[3]
                actual_gdp = value[5]
                predict_gdp = value[6]

                if(actual_gdp is not None):
                    data['gdp_actual']['years'].append(year)
                    data['gdp_actual']['gdp'].append(actual_gdp)

                if(predict_gdp is not None):
                    data['gdp_predict']['years'].append(year)
                    data['gdp_predict']['gdp'].append(predict_gdp)

        if len(data['gdp_actual']['years']) > 0:
            prev_year = data['gdp_actual']['years'][-1]

            if (len(data['gdp_predict']['years']) == 0) or ((prev_year+1) not in data['gdp_predict']['years']):
                prediction = make_prediction_by_name(data['country_name'], prev_year, data['income_level'])
                if prediction != None:
                    pred_year = prev_year + 1
                    data['gdp_predict']['years'].append(pred_year)
                    data['gdp_predict']['gdp'].append(prediction)
                    insert_new_prediction(country, pred_year, prediction)

        return data
    except error as e:
        print('Failed to get gdp by country', e)