
from typing import Optional, Dict
from model.QuotasInterval import QuotasInterval
import uuid

class QuotasTracker():


    def __init__(self, quotasPerInterval:Optional[dict] = None):
        self._lastIntervalHit = None

        self._quotas = {}

        if quotasPerInterval:
            for duration, interval in quotasPerInterval.items():
                if 'limit' not in interval or interval['limit'] < 0:
                    continue

                self._quotas[interval['name']] = QuotasInterval(
                    name=interval['name'] if 'name' in interval else str(uuid.uuid4()),
                    duration=duration,
                    limit=interval['limit'],
                    log=interval['log'] if 'log' in interval else True
                )

    @property
    def lastIntervalHit(self) -> QuotasInterval:
        return self._lastIntervalHit

    @lastIntervalHit.setter
    def lastIntervalHit(self, lastIntervalHit:QuotasInterval):
        self._lastIntervalHit = lastIntervalHit

    @property
    def quotas(self) -> Dict[str, QuotasInterval]:
        return self._quotas


