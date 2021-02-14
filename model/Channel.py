
from typing import Optional
from model.Job import Job
from model.QuotasTracker import QuotasTracker

class Channel():

    def __init__(
        self,
        name:str,
        maxConcurrentJobs:int = 1,
        timeoutOffset:int = 0,
        quotasPerInterval:Optional[dict] = None
    ):
        self._name = name
        self._maxConcurrentJobs = maxConcurrentJobs
        self._timeoutOffset = timeoutOffset
        self._quotasPerInterval = quotasPerInterval
        self._jobs = dict()
        self._waitingJobs = list()
        self._workingJobs = dict()
        self._quotasTracker = QuotasTracker(quotasPerInterval=quotasPerInterval)

    @property
    def quotasTracker(self) -> QuotasTracker:
        return self._quotasTracker

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value

    @property
    def maxConcurrentJobs(self) -> int:
        return self._maxConcurrentJobs

    @maxConcurrentJobs.setter
    def maxConcurrentJobs(self, value: int):
        self._maxConcurrentJobs = value

    @property
    def timeoutOffset(self) -> int:
        return self._timeoutOffset

    @timeoutOffset.setter
    def timeoutOffset(self, value: int):
        self._timeoutOffset = value

    @property
    def quotasPerInterval(self) -> dict:
        return self._quotasPerInterval

    def getWorkingJobsUids(self) -> list:
        return list(self._workingJobs)

    def isWorkingJobFull(self) -> bool:
        return len(self._workingJobs) >= self._maxConcurrentJobs

    def removeWorkingJob(self, job: Job) -> bool:
        if job.uid not in self._workingJobs:
            return False

        del self._workingJobs[job.uid]

        return True

    def pushWorkingJob(self, job: Job) -> bool:
        if self.isWorkingJobFull():
            return False

        self._workingJobs[job.uid] = True

        return True

    def isFillable(self):
        return not self.isWaitingJobEmpty() and not self.isWorkingJobFull()

    def isWaitingJobEmpty(self) -> bool:
        return len(self._waitingJobs) == 0

    def popNextWaitingJob(self) -> Optional[Job]:        
        if len(self._waitingJobs) == 0:
            return None

        return self.getJob(self._waitingJobs.pop(0))

    def pushWaitingJob(self, job: Job):
        self._waitingJobs.append(job.uid)



    def addJob(self, job: Job) -> bool:
        if job.uid in self._jobs:
            return False
        
        job.channel = self

        self._jobs[job.uid] = job
        
        return True

    def hasJob(self, uid: str) -> bool:
        return uid in self._jobs

    def getJob(self, uid: str) -> Optional[Job]:
        if self.hasJob(uid):
            return self._jobs[uid]

        return None

    def removeJob(self, uid: str) -> bool:
        if not self.hasJob(uid):
            return False

        del self._jobs[uid]

        return True




    def countWorkingJobs(self):
        return len(self._workingJobs)

    def countWaitingJobs(self):
        return len(self._waitingJobs)

    def countJobs(self):
        return len(self._jobs)