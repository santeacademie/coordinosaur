import re

from typing import Optional
from model.Channel import Channel
from core.ContainerAware import ContainerAware

class ChannelManager(ContainerAware):

	OPTION_TIMEOUT_OFFSET = 'TIMEOUT_OFFSET'
	OPTION_MAX_CONCURRENT_JOBS = 'MAX_CONCURRENT_JOBS'
	OPTION_QUOTAS_PER_INTERVAL = 'QUOTAS_PER_INTERVAL'

	def __init__(self):
		self._channels = dict()

	def getDefaultOptions(self) -> dict:
		return {
			self.OPTION_TIMEOUT_OFFSET: self.BagManager.DEFAULT_TIMEOUT_OFFSET,
			self.OPTION_MAX_CONCURRENT_JOBS: self.BagManager.DEFAULT_MAX_CONCURRENT_JOBS,
			self.OPTION_QUOTAS_PER_INTERVAL: self.BagManager.DEFAULT_QUOTAS_PER_INTERVAL
		}

	def getMatchingOptions(self, channelName: str) -> dict:
		usingOptions = self.getDefaultOptions()

		for pattern, options in self.BagManager.CHANNEL_OPTIONS.items():
			if re.match(pattern, channelName):
				self.LogManager.debug('[ChannelManager] channel: '+channelName+' is matching pattern '+ str(pattern) + ' with following options:')
				self.LogManager.debug(options)

				for optionName, optionValue in options.items():
					usingOptions[optionName] = optionValue

		return usingOptions

	def findMaxConcurrentJobs(self, name:str) -> int:
		for pattern, maxConcurrentJobsValue in self.BagManager.CHANNEL_MAX_CONCURRENT_JOBS.items():
			if re.match(pattern, name):
				self.LogManager.debug('[ChannelManager] channel: '+name+' is matching concurrency pattern '+ str(pattern) + ' = ' + str(maxConcurrentJobsValue))

				return int(maxConcurrentJobsValue)

		return self.BagManager.DEFAULT_MAX_CONCURRENT_JOBS

	def addChannel(self, name:str) -> Channel:
		options = self.getMatchingOptions(channelName=name)

		self._channels[name] = Channel(
			name=name,
			maxConcurrentJobs=options[self.OPTION_MAX_CONCURRENT_JOBS],
			timeoutOffset=options[self.OPTION_TIMEOUT_OFFSET],
			quotasPerInterval=options[self.OPTION_QUOTAS_PER_INTERVAL]
		)

		return self._channels[name]

	def getChannels(self) -> dict:
		return self._channels

	def hasChannel(self, name:str) -> bool:
		return name in self._channels

	def getChannel(self, name:str, create:bool = True) -> Optional[Channel]:
		if self.hasChannel(name):
			return self._channels[name]

		if create:
			channel = self.addChannel(name)
			self.LogManager.debug('[ChannelManager] channel: ' + channel.name + ' registered with concurrency = ' + str(channel.maxConcurrentJobs))
			return channel

		return None

	def removeChannel(self, name: str):
		if not self.hasChannel(name):
			return False

		del self._channels[name]

		return True
