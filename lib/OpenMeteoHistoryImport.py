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

import sched
import json
from datetime import datetime, timedelta

import requests
import time

from import_lib.import_lib import get_logger, ImportLib

from lib.data.OpenMeteoHistoryDataFetcher import get_data as get_data_archive
from lib.data.OpenMeteoPastDaysForecastingDataFetcher import get_data as get_data_past_days_forecast

logger = get_logger(__name__)


class OpenMeteoHistoryImport:
    def __init__(self, lib: ImportLib, scheduler: sched.scheduler):
        self.__lib = lib
        self.__scheduler = scheduler
        self.__lat = self.__lib.get_config("lat", 51.34)
        self.__long = self.__lib.get_config("long", 12.38)
        self.__start_date = self.__lib.get_config('start', str(datetime.now().date() - timedelta(days=365)))
        self.__past_days = 6
        self.__forecast_days = 1
        self.import_current_with_retry()

    def import_current_with_retry(self, max_attempts: int = 5, base_sleep: float = 2.0) -> bool:
        for attempt in range(1, max_attempts + 1):
            try:
                self.import_current()
                return True

            except requests.exceptions.ConnectionError as e:
                print(f"Open-Meteo-Verbindungsfehler, Versuch {attempt}/{max_attempts}: {e}")

            except requests.exceptions.Timeout as e:
                print(f"Open-Meteo-Timeout, Versuch {attempt}/{max_attempts}: {e}")

            except requests.exceptions.HTTPError as e:
                print(f"Open-Meteo-HTTP-Fehler, kein weiterer Retry: {e}")
                return False

            if attempt < max_attempts:
                sleep_seconds = base_sleep * attempt
                time.sleep(sleep_seconds)

        print("Open-Meteo-Import nach mehreren Versuchen fehlgeschlagen. App läuft weiter.")
        return False

    def import_current(self):
        end_date = str(datetime.now().date() - timedelta(days=6))
        units, values_archive = get_data_archive(self.__lat, self.__long, self.__start_date, end_date)
        _, values_past_days_forecast = get_data_past_days_forecast(self.__lat, self.__long, self.__past_days, self.__forecast_days)
        all_values = values_archive + values_past_days_forecast
        for t, v in all_values:
            self.__lib.put(t, v.dict(units))
            logger.debug(json.dumps(v.dict(units)))
        logger.info("Imported " + str(len(all_values)) + " values")
        logger.info("Scheduling next run for " + str(datetime.now().date() + timedelta(days=1)))
        self.__scheduler.enterabs(datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time()).timestamp(), 1, self.import_current_with_retry)
