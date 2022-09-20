from os import error
import sys
from ..models.gdp_models import *
from ..models.inflation_models import *
from ..models.unemployment_models import *
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd

MODEL_PATH_DICT= {
    'low': '../../../saved_models/gdp/v1/low_income_v1.h5',
    'lower-middle': '../../../saved_models/gdp/v1/low_mid_income_v1.h5',
    'upper-middle': '../../../saved_models/gdp/v1/upp_mid_income_v1.h5',
    'high': '../../../saved_models/gdp/v1/high_income_v1.h5'
}
DATA_PATH = '../../../data/gdp/gdp_data_complete_v2.xlsx';

def get_scaler(income_level: str):
    data = pd.read_excel(DATA_PATH, sheet_name='data shift wout null', index_col='Year')
    df = data[data['IncomeLevel'] == income_level]

    scY = StandardScaler()
    scY.fit_transform(df['GDP'].values.reshape(-1,1))
    
    return scY


def make_prediction_by_name(country_name: str, prev_year: int, income_level: str):
    prediction = None
    try:        
        model = load_model(MODEL_PATH_DICT[income_level])
        
        inflation = get_inflation_by_year(country_name, prev_year)
        unemployment = get_unemployment_by_year(country_name, prev_year)

        if inflation == None:
            print('Cannot forecast, inflation data unavailable', file=sys.stderr)
            return prediction

        if unemployment == None:
            print('Cannot forecast, unemployment data unavailable', file=sys.stderr)
            return prediction
        
        unscaled_prediction = model.predict(((inflation, unemployment),))

        if unscaled_prediction != None:
            scY = get_scaler(income_level)
            pred_df = pd.DataFrame({
                'Year': [prev_year],
                'GDP': [float(unscaled_prediction[0][0])]
                })
            pred_df = pred_df.set_index('Year')
            prediction = scY.inverse_transform(pred_df)

            return prediction[0][0]
    except error as e:
        print('Failed to make prediction', e)

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