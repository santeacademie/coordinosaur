
from typing import Optional

class Job():

    INDEX_ROLL = 0

    def __init__(self, uid:str, ttl: int, channel: Optional['Channel'] = None):
        self._uid = uid
        self._ttl = ttl
        self._channel = channel
        self._startedAt = None
        self._index = Job.INDEX_ROLL

        Job.INDEX_ROLL += 1

    def loguid(self):
        return self.uid + '___(#'+str(self._index)+')'

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @property
    def index(self) -> int:
        return self._index

    @property
    def channel(self) -> Optional['Channel']:
        return self._channel

    @channel.setter
    def channel(self, channel:'Channel'):
        self._channel = channel

    @property
    def ttl(self) -> int:
        return self._ttl

    @property
    def startedAt(self) -> Optional[int]:
        return self._startedAt

    @startedAt.setter
    def startedAt(self, value):
        self._startedAt = value

