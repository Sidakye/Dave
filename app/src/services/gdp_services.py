from os import error
from ..models.gdp_models import *

MODEL_PATH_DICT= {
    'low': '../../../saved_models/gdp/v1/low_income_v1.h5',
    'lower-middle': '../../../saved_models/gdp/v1/low_mid_income_v1.h5',
    'upper-middle': '../../../saved_models/gdp/v1/upp_mid_income_v1.h5',
    'high': '../../../saved_models/gdp/v1/high_income_v1.h5'
}

def make_prediction_by_name(country_name: str, pred_year: int):
    prediction = None
    try:
        # get country level
        print(prediction) # just a placeholder

    except error as e:
        print('Failed to make prediction for', country_name, e)


def use_all_gdp() -> list:
    data = []
    try:
        countries = get_all_countries()
        if len(countries) > 0:
            for country in countries:
                country_dict = {
                    'country_id': country[0],
                    'country_name': country[1],
                    'gdp_actual': {
                        'years': [],
                        'gdp': [],
                    },
                    'gdp_predict': {
                        'years': [],
                        'gdp': []
                    },
                }

                values = get_gdp_by_country_name(country[1])

                for value in values:
                    year = value[3]
                    actual_gdp = value[5]
                    predicted_gdp = value[6]

                    if(actual_gdp is not None):
                        country_dict['gdp_actual']['years'].append(year)
                        country_dict['gdp_actual']['gdp'].append(actual_gdp)

                    if(predicted_gdp is not None):
                        country_dict['gdp_predict']['years'].append(year)
                        country_dict['gdp_predict']['gdp'].append(predicted_gdp)
                    # else:
                        # Make prediction here, save to database & append to outgoing data
                        # print('No gdp prediction exists for ', year)
                data.append(country_dict)
        else:
            countries = None
    except error as e:
        print('Failed to get all gdp', e)
    
    return data
