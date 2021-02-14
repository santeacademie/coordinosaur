import threading
import time
from typing import Optional

from model.Job import Job
from model.Channel import Channel
from core.ContainerAware import ContainerAware


class QueueManager(ContainerAware):

	def __init__(self):
		self._runEvent = threading.Event()
		self._runEvent.set()
		self._threads = dict()
		self.init()

	def init(self):
		self._threads['__jobTimeout'] = threading.Thread(target=self.timeout, args=())
		self._threads['__jobTimeout'].start()

	def stop(self):
		self._runEvent.clear()

		for channelName, thread in self._threads.items():
			thread.join()

	def checkChannel(self, channelName:str) -> Channel:
		channel = self.ChannelManager.getChannel(channelName, create=True)

		if channelName not in self._threads:
			self._threads[channelName] = threading.Thread(target=self.loop, args=(channel,))
			self._threads[channelName].start()

		return channel


	def kill(self, job: Job, killedBy:str = None):
		wasWorking = job.channel.removeWorkingJob(job=job)
		wasRegistered = job.channel.removeJob(uid=job.uid)

		self.LogManager.debug('[QueueManager:' + str(job.channel.name) + '] job: ' + job.loguid() + ' killed by: ' + killedBy.upper() +
							  ' (wasWorking: '+('yes' if wasWorking else 'no')+', wasRegistered: '+('yes' if wasRegistered else 'no')+')')

	def timeout(self):
		while self._runEvent.is_set():
			for channelName, channel in self.ChannelManager.getChannels().items():
				uids = channel.getWorkingJobsUids()

				for uid in uids:
					job = channel.getJob(uid)

					if time.time() - job.startedAt >= job.ttl + job.channel.timeoutOffset:
						self.LogManager.debug('[QueueManager:'+str(job.channel.name)+'] job: ' + job.loguid()+ ' timeout (offset:'+str(job.channel.timeoutOffset)+')')
						self.kill(job, killedBy='timeout')

			time.sleep(1)

	def loop(self, channel: Channel):
		while self._runEvent.is_set():
			time.sleep(.5)

			while channel.isFillable() and self._runEvent.is_set():
				quotasInterval = self.QuotasManager.getQuotasIntervalHit(channel=channel)

				if quotasInterval:
					self.QuotasManager.logInterval(channel.name, quotasInterval)
					time.sleep(1)
					continue

				job = channel.popNextWaitingJob()

				if not job:
					continue

				self.LogManager.debug('[QueueManager:%s] job: %s GO' % (channel.name, job.loguid()))

				channel.pushWorkingJob(job)
				self.MqttManager.publish(topic='%s/go/%s' % (channel.name, job.uid), payload=job.uid)
				job.startedAt = time.time()

				self.QuotasManager.track(channel=channel, timeToTrack=job.startedAt)

	def infos(self, channel: Channel):
		self.LogManager.info('[QueueManager:%s] Waiting jobs: %s, Working jobs: %s' % (channel.name, channel.countWaitingJobs(), channel.countWorkingJobs()))

	def register(self, channel: Channel, job: Job) -> bool:
		if not channel.addJob(job):
			self.LogManager.debug('[QueueManager:'+str(channel.name)+'] job: ' + str(job.loguid()) + ' already registered')
			return False

		self.LogManager.debug('[QueueManager:'+str(channel.name)+'] job: ' + str(job.loguid())+ ' registered successfully')

		channel.pushWaitingJob(job)

	def finished(self, channel: Channel, jobUid: str):
		job = channel.getJob(uid=jobUid)

		if job:
			self.kill(job, 'finished')

	def aborted(self, channel: Channel, jobUid: str):
		job = channel.getJob(uid=jobUid)

		if job:
			self.kill(job, 'aborted')


