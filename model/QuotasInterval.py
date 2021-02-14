

class QuotasInterval():

    def __init__(self, name:str, duration:int = 0, limit:int = 0, log = True):
        self._futureExpirations = list()
        self._log = log
        self._name = name
        self._duration = duration
        self._limit = limit
        self._remainingTime = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def loggingLevel(self) -> str:
        if self._log == False or self._log is None or self._log == 0:
            return 'q'
        elif self._log == True or self._log == 'v'  or self._log == 1:
            return 'v'
        elif self._log == 'vv'  or self._log == 2:
            return 'vv'

        return 'q'

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        self._log = value

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, value: int):
        self._duration = value

    @property
    def limit(self) -> int:
        return self._limit

    @limit.setter
    def limit(self, value: int):
        self._limit = value

    @property
    def remainingTime(self) -> int:
        return self._remainingTime

    @remainingTime.setter
    def remainingTime(self, value: int):
        self._remainingTime = value

    @property
    def futureExpirations(self) -> list:
        return self._futureExpirations

    def addFutureExpiration(self, timeToTrack: int):
        self._futureExpirations.append(timeToTrack)

    def shiftFutureExpirations(self, newStartingIndex: int):
        self._futureExpirations = self._futureExpirations[newStartingIndex:]