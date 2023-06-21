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


class Units(object):

    def __init__(self,
                 temperature_2m: str,
                 relativehumidity_2m: str,
                 pressure_msl: str,
                 precipitation: str,
                 cloudcover: str,
                 cloudcover_low: str,
                 cloudcover_mid: str,
                 cloudcover_high: str,
                 shortwave_radiation: str,
                 direct_radiation: str,
                 diffuse_radiation: str,
                 windspeed_10m: str,
                 winddirection_10m: str):
        self.temperature_2m = temperature_2m
        self.relativehumidity_2m = relativehumidity_2m
        self.pressure_msl = pressure_msl
        self.precipitation = precipitation
        self.cloudcover = cloudcover
        self.cloudcover_low = cloudcover_low
        self.cloudcover_mid = cloudcover_mid
        self.cloudcover_high = cloudcover_high
        self.shortwave_radiation = shortwave_radiation
        self.direct_radiation = direct_radiation
        self.diffuse_radiation = diffuse_radiation
        self.windspeed_10m = windspeed_10m
        self.winddirection_10m = winddirection_10m

    def dict(self) -> dict:
        d = {
            "temperature_2m": self.temperature_2m,
            "relativehumidity_2m": self.relativehumidity_2m,
            "pressure_msl": self.pressure_msl,
            "precipitation": self.precipitation,
            "cloudcover": self.cloudcover,
            "cloudcover_low": self.cloudcover_low,
            "cloudcover_mid": self.cloudcover_mid,
            "cloudcover_high": self.cloudcover_high,
            "shortwave_radiation": self.shortwave_radiation,
            "direct_radiation": self.direct_radiation,
            "diffuse_radiation": self.diffuse_radiation,
            "windspeed_10m": self.windspeed_10m,
            "winddirection_10m": self.winddirection_10m
        }
        return d
