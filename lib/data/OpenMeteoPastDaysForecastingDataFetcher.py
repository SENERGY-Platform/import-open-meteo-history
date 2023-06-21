#  Copyright 2021 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import datetime
from typing import Tuple, List, Optional

import requests
from import_lib.import_lib import get_logger

from lib.data.Units import Units
from lib.data.Value import Value
from lib.util import extract

OPEN_METEO_BASE_URL = "https://api.open-meteo.com"
OPEN_METEO_FORECAST_URL = OPEN_METEO_BASE_URL + "/v1/forecast"

logger = get_logger(__name__)


def get_data(lat: float, long: float, past_days: int, forecast_days: int) -> Tuple[datetime, datetime, Optional[Units], List[Tuple[datetime, Value]]]:
    '''
    :param if_modified_since: Previously returned Last-Modified
    :param lat: Latitude
    :param long: Longitude
    :return: Units, Forecasts
    '''
    lat = round(lat, 4)
    long = round(long, 4)

    url = OPEN_METEO_FORECAST_URL
    params = {'latitude': lat, 'longitude': long, 'timezone': 'auto',  'past_days': past_days, 'forecast_days': forecast_days,
              'hourly': ['temperature_2m',
                        'relativehumidity_2m',
                        'pressure_msl',
                        'precipitation',
                        'cloudcover',
                        'cloudcover_low',
                        'cloudcover_mid',
                        'cloudcover_high',
                        'shortwave_radiation',
                        'direct_radiation',
                        'diffuse_radiation',
                        'windspeed_10m',
                        'winddirection_10m',
                        'weathercode']}
    r = requests.get(url, params = params)
    if not r.ok:
        raise RuntimeError("Error contacting Open-Meteo Api")

    j = r.json()
    if 'hourly_units' not in j:
        raise RuntimeError("Error: Invalid Open-Meteo Response")
    api_units = j['hourly_units']
    units = Units(
        temperature_2m=extract(api_units, 'temperature_2m'),
        relativehumidity_2m=extract(api_units, 'relativehumidity_2m'),
        pressure_msl=extract(api_units, 'pressure_msl'),
        precipitation=extract(api_units, 'precipitation'),
        cloudcover=extract(api_units, 'cloudcover'),
        cloudcover_low=extract(api_units, 'cloudcover_low'),
        cloudcover_mid=extract(api_units, 'cloudcover_mid'),
        cloudcover_high=extract(api_units, 'cloudcover_high'),
        shortwave_radiation=extract(api_units, 'shortwave_radiation'),
        direct_radiation=extract(api_units, 'direct_radiation'),
        diffuse_radiation=extract(api_units, 'diffuse_radiation'),
        windspeed_10m=extract(api_units, 'windspeed_10m'),
        winddirection_10m=extract(api_units, 'winddirection_10m'),
        weathercode=extract(api_units, 'weathercode')
    )
    values: List[Tuple[datetime, Value]] = []
    if 'hourly' not in j or 'time' not in j['hourly']:
        raise RuntimeError("Error: Invalid Open-Meteo Response")
    for value_type in j['hourly']:
        if len(j['hourly'][value_type]) != len(j['hourly']['time']):
            raise RuntimeError('Error: Invalid Open-Meteo Response')

    for i, time in enumerate(j['hourly']['time']):
        values.append((time, Value(
            temperature_2m=j['hourly']['temperature_2m'][i],
            relativehumidity_2m=j['hourly']['relativehumidity_2m'][i],
            pressure_msl=j['hourly']['pressure_msl'][i],
            precipitation=j['hourly']['precipitation'][i],
            cloudcover=j['hourly']['cloudcover'][i],
            cloudcover_low=j['hourly']['cloudcover_low'][i],
            cloudcover_mid=j['hourly']['cloudcover_mid'][i],
            cloudcover_high=j['hourly']['cloudcover_high'][i],
            shortwave_radiation=j['hourly']['shortwave_radiation'][i],
            direct_radiation=j['hourly']['direct_radiation'][i],
            diffuse_radiation=j['hourly']['diffuse_radiation'][i],
            windspeed_10m=j['hourly']['windspeed_10m'][i],
            winddirection_10m=j['hourly']['winddirection_10m'][i],
            weathercode=j['hourly']['weathercode'][i]
        )))
    return units, values
