# import-open-meteo-history

Imports weather history data from Open-Meteo.


## Outputs
* weather_time (string): timestamp of weather data in ISO 8601 format
* temperature_2m (float)
* pressure_msl (float)
* precipitation (float)
* cloudcover (float)
* cloudcover_low (float)
* cloudcover_mid (float)
* cloudcover_high (float)
* shortwave_radiation (float)
* direct_radiation (float)
* diffuse_radiation (float)
* windspeed_10m (float)
* winddirection_10m (float)
* instant_wind_speed_of_gust (float)
* units (structure):
  * temperature_2m (string)
  * relativehumidity_2m (string)
  * pressure_msl (string)
  * precipitation (string)
  * cloudcover (string)
  * cloudcover_low (string)
  * cloudcover_mid (string)
  * cloudcover_high (string)
  * shortwave_radiation (string)
  * direct_radiation (string)
  * diffuse_radiation (string)
  * windspeed_10m (string)
  * winddirection_10m (string)


## Configs
* lat (float): latitude selected. Default: 51.34
* long (float): longitude selected. Default: 12.38
* start (string): start date of imported weather data in the format YYYY-MM-DD
---

This tool uses publicly available data provided by Open-Meteo.com.
Their archive of historical weather data is available [here](https://open-meteo.com/en/docs/historical-weather-api).

