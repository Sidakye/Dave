from os import error
from ..models.gdp_models import *

def use_all_gdp():
    data = []
    try:
        countries = get_all_countries()
        if len(countries) > 0:
            for country in countries:
                values = get_gdp_by_country_name(country[0])

                country_dict = {
                    'country_id': country[0],
                    'country_name': country[1],
                    'gdp_actual': [],
                    'gdp_predict': []
                }

                for value in values:
                    country_dict['gdp_actual'].append({
                        'Year': value[3], 'GDP': value[5]
                    })
                    country_dict['gdp_predict'].append({
                        'Year': value[3], 'GDP': value[6]
                    })
                
                data.append(country_dict)
        else:
            countries = None
    except error as e:
        print('Failed to get all gdp', e)
    
    return data
