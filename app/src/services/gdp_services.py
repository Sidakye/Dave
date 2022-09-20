from os import error
from ..models.gdp_models import *
from ..models.inflation_models import *
from ..models.unemployment_models import *
from keras.models import load_model

MODEL_PATH_DICT= {
    'low': '../../../saved_models/gdp/v1/low_income_v1.h5',
    'lower-middle': '../../../saved_models/gdp/v1/low_mid_income_v1.h5',
    'upper-middle': '../../../saved_models/gdp/v1/upp_mid_income_v1.h5',
    'high': '../../../saved_models/gdp/v1/high_income_v1.h5'
}

def make_prediction_by_name(country_name: str, prev_year: int):
    prediction = None
    try:
        country_details = get_country_details_by_name(country_name)
        economic_level = country_details[2]
        
        model = load_model(MODEL_PATH_DICT[economic_level])
        
        inflation = get_inflation_by_year(country_name, prev_year)
        unemployment = get_unemployment_by_year(country_name, prev_year)

        if inflation == None:
            print('Cannot forecast, inflation data unavailable')
            return prediction
        if unemployment == None:
            print('Cannot forecast, unemployment data unavailable')
            return prediction
        
        # prediction = model.predict((inflation, unemployment))
        prediction = model.predict(((12.34, 9.05),))


        if prediction == None:
            return prediction
        
        print(type(prediction), prediction)
        # insert_new_prediction(country_details, prev_year+1, prediction)
    except error as e:
        print('Failed to make prediction', e)

    return prediction


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
                
                # get prediction for year after last actual gdp
                new_prediction = None
                if len(country_dict['gdp_actual']['years']) > 0:
                    prev_year = country_dict['gdp_actual']['years'][-1]
                    new_prediction = make_prediction_by_name(country[1], prev_year)
                
                if new_prediction is not None:
                    country_dict['gdp_predict']['years'].append(prev_year+1)
                    country_dict['gdp_predict']['gdp'].append(new_prediction)
                
                data.append(country_dict)
        else:
            countries = None
    except error as e:
        print('Failed to get all gdp', e)
    
    return data
