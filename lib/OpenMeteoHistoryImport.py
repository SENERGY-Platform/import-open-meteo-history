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
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import requests
import time

from import_lib.import_lib import get_logger, ImportLib

from lib.data.OpenMeteoHistoryDataFetcher import get_data as get_data_archive

logger = get_logger(__name__)


class OpenMeteoHistoryImport:
    def __init__(self, lib: ImportLib, scheduler: sched.scheduler):
        self.__lib = lib
        self.__scheduler = scheduler
        self.__lat = self.__lib.get_config("lat", 51.34)
        self.__long = self.__lib.get_config("long", 12.38)
        self.__start_date = date.fromisoformat(str(self.__lib.get_config('start', str(datetime.now().date() - timedelta(days=365))))[:10])
        self.import_current_with_retry()

    def __read_watermark(self) -> Optional[datetime]:
        last, message = self.__lib.get_last_published_datetime()
        if last is None:
            return None
        if not message:
            # import-lib answers with the epoch and an empty message when it cannot read the last message. Going on
            # would import everything since start again.
            raise RuntimeError("Could not read the last published message")
        # import-lib parses the time of the last message into a naive datetime in UTC
        return last.replace(tzinfo=timezone.utc) if last.tzinfo is None else last

    def import_current_with_retry(self, max_attempts: int = 5, base_sleep: float = 2.0) -> bool:
        for attempt in range(1, max_attempts + 1):
            try:
                self.import_current()
                return True

            except requests.exceptions.ConnectionError as e:
                logger.info(f"Open-Meteo-Verbindungsfehler, Versuch {attempt}/{max_attempts}: {e}")

            except requests.exceptions.Timeout as e:
                logger.info(f"Open-Meteo-Timeout, Versuch {attempt}/{max_attempts}: {e}")

            except requests.exceptions.HTTPError as e:
                logger.info(f"Open-Meteo-HTTP-Fehler, kein weiterer Retry: {e}")
                return False

            if attempt < max_attempts:
                sleep_seconds = base_sleep * attempt
                time.sleep(sleep_seconds)

        logger.info("Open-Meteo-Import nach mehreren Versuchen fehlgeschlagen. App läuft weiter.")
        return False

    def import_current(self):
        logger.info("Open-Meteo import_current started")

        # Read at every run, so that messages that were queued but never delivered are imported again
        watermark = self.__read_watermark()
        start_date = self.__start_date
        if watermark is not None:
            # The archive is queried by local date of the location, which can lie a day before the UTC date
            start_date = max(start_date, watermark.date() - timedelta(days=1))
        end_date = datetime.now().date() - timedelta(days=6)

        imported = 0
        if start_date <= end_date:
            logger.info(f"Fetching archive data from {start_date} to {end_date}")
            units, values = get_data_archive(self.__lat, self.__long, str(start_date), str(end_date))
            logger.info(f"Fetched archive data: {len(values)} values")
            for t, v in values:
                if watermark is not None and t <= watermark:
                    continue
                self.__lib.put(t, v.dict(units))
                logger.debug(json.dumps(v.dict(units)))
                imported += 1
        else:
            logger.info(f"Skipping archive data, start {start_date} is after {end_date}")
        logger.info("Imported " + str(imported) + " values")
        logger.info("Scheduling next run for " + str(datetime.now().date() + timedelta(days=1)))
        self.__scheduler.enterabs(datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time()).timestamp(), 1, self.import_current_with_retry)
