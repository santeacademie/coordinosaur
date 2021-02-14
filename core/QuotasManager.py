
from core.ContainerAware import ContainerAware

from typing import Optional
from model.Channel import Channel
from model.QuotasTracker import QuotasTracker
from model.QuotasInterval import QuotasInterval
import time

class QuotasManager(ContainerAware):


	def __init__(self):
		pass



	def track(self, channel:Channel, timeToTrack: Optional[int], disableIntervals: Optional[list] = None):
		if not timeToTrack:
			return

		quotasTracker: QuotasTracker = channel.quotasTracker

		for quotasInterval in quotasTracker.quotas.values():
			if quotasInterval.limit <= 0 or (disableIntervals and quotasInterval.name in disableIntervals):
				continue

			quotasInterval.addFutureExpiration(timeToTrack + quotasInterval.duration)

	def getQuotasIntervalHit(self, channel: Channel, disableIntervals: Optional[list] = None) -> Optional[QuotasInterval]:
		quotasTracker: QuotasTracker = channel.quotasTracker

		now = time.time()
		intervalHit = None

		for quotasInterval in quotasTracker.quotas.values():
			if quotasInterval.limit <= 0 or (disableIntervals and quotasInterval.name in disableIntervals):
				continue

			firstHitIndex = None
			counter = 0

			for futureExpiration in quotasInterval.futureExpirations:
				if now <= futureExpiration:
					firstHitIndex = counter
					break

				counter += 1

			quotasInterval.shiftFutureExpirations(newStartingIndex=firstHitIndex)

			hit = 0
			remainingTimeOnFirstHit = -1

			for futureExpiration in quotasInterval.futureExpirations:
				if now <= futureExpiration:
					hit += 1

					if remainingTimeOnFirstHit == -1:
						remainingTimeOnFirstHit = futureExpiration - now

			if hit >= quotasInterval.limit:
				quotasInterval.remainingTime = remainingTimeOnFirstHit
				intervalHit = quotasInterval
				break

		quotasTracker.lastIntervalHit = intervalHit

		return intervalHit


	def logInterval(self, channelName:str, quotasInterval: QuotasInterval):
		if quotasInterval.loggingLevel() == 'v' or quotasInterval.loggingLevel() == 'vv':
			self.LogManager.debug('[QuotasManager:%s] Hit rate limit: %s every %s (remaining time: %s)' % (
				channelName,
				quotasInterval.limit,
				quotasInterval.name,
				quotasInterval.remainingTime
			))