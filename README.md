# import-open-meteo-history

Imports weather history data from Open-Meteo.

<!---
## Outputs
* forecasted_for (string): timestamp of forecast in rfc3339
* instant_air_pressure_at_sea_level (float)
* instant_air_temperature (float)
* instant_cloud_area_fraction (float)
* instant_cloud_area_fraction_high (float)
* instant_cloud_area_fraction_low (float)
* instant_cloud_area_fraction_medium (float)
* instant_dew_point_temperature (float)
* instant_fog_area_fraction (float)
* instant_relative_humidity (float)
* instant_ultraviolet_index_clear_sky (float)
* instant_wind_from_direction (float)
* instant_wind_speed (float)
* instant_wind_speed_of_gust (float)
* 12_hours_probability_of_precipitation (float
* 1_hours_precipitation_amount (float)
* 1_hours_precipitation_amount_max (float)
* 1_hours_precipitation_amount_min (float)
* 1_hours_probability_of_precipitation (float)
* 1_hours_probability_of_thunder (float)
* 6_hours_air_temperature_max (float)
* 6_hours_air_temperature_min (float)
* 6_hours_precipitation_amount (float)
* 6_hours_precipitation_amount_max (float)
* 6_hours_precipitation_amount_min (float)
* 6_hours_probability_of_precipitation (float)
* units (structure):
  * air_pressure_at_sea_level (string)
  * air_temperature (string)
  * air_temperature_max (string)
  * air_temperature_min (string)
  * cloud_area_fraction (string)
  * cloud_area_fraction_high (string)
  * cloud_area_fraction_low (string)
  * cloud_area_fraction_medium (string)
  * dew_point_temperature (string)
  * fog_area_fraction (string)
  * precipitation_amount (string)
  * precipitation_amount_max (string)
  * precipitation_amount_min (string)
  * probability_of_precipitation (string)
  * probability_of_thunder (string)
  * relative_humidity (string)
  * ultraviolet_index_clear_sky (string)
  * wind_from_direction (string)
  * wind_speed (string)
  * wind_speed_of_gust (string)

## Configs
* lat (float): latitude selected. Default: 51.34
* long (float); longitude selected. Default: 12.38
  
---

This tool uses publicly available data provided by the Norwegian Meteorological Institute released 
under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Their forecasts are available [here](https://www.yr.no/en).

-->
