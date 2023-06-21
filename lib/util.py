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

from datetime import datetime, timezone
import time
from typing import Optional


def datetime_to_http(dt: datetime) -> str:
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(dt.timestamp()))


def http_to_datetime(s: str) -> datetime:
    return datetime.strptime(s, '%a, %d %b %Y %H:%M:%S GMT').replace(tzinfo=timezone.utc)


def extract(d: dict, path: str) -> Optional[any]:
    paths = path.split('.')
    element = d
    try:
        for p in paths:
            element = element[p]
    except KeyError:
        return None
    return element
