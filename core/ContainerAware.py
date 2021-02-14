import core.Container as ContainerPackage

class ContainerAware():

	@property
	def Container(self):
		return ContainerPackage.Container.getInstance()

	@property
	def BagManager(self):
		return ContainerPackage.Container.getInstance().bagManager

	@property
	def QueueManager(self):
		return ContainerPackage.Container.getInstance().queueManager

	@property
	def QuotasManager(self):
		return ContainerPackage.Container.getInstance().quotasManager

	@property
	def ChannelManager(self):
		return ContainerPackage.Container.getInstance().channelManager

	@property
	def MqttManager(self):
		return ContainerPackage.Container.getInstance().mqttManager

	@property
	def LogManager(self):
		return ContainerPackage.Container.getInstance().logManager

	def broadcast(self, method: str, exceptions: list = None, manager = None, searchRuler = False, **kwargs):
		if not exceptions:
			exceptions = list()

		if isinstance(exceptions, str):
			exceptions = [exceptions]

		if not exceptions and not manager:
			# Prevent infinite loop of broadcaster being broadcasted to re broadcasting
			self.LogManager.error('Cannot broadcast to itself, the calling method has to be put in exceptions')
			return

		# if 'MainClass' not in exceptions:
		# 	exceptions.append('MainClass')

		if not method.startswith('on'):
			method = 'on' + (method[0].capitalize() + method[1:])

		deadManagers = list()

		rulerFound = False

		for name, instance in ContainerPackage.Container.getInstance().managers.items():
			if not instance:
				deadManagers.append(name)
				continue

			if (manager and instance.__class__.__name__ != manager.__class__.__name__) or instance.__class__.__name__ in exceptions:
				continue

			try:
				func = getattr(instance, method, None)

				if func:
					ret = func(**kwargs)

					if searchRuler and ret:
						rulerFound = True

			except TypeError as e:
				self.LogManager.error('- Failed to broadcast global event %s to %s: %s' % (
					method,
					instance.__class__.__name__,
					e
				))

		for name in deadManagers:
			del ContainerPackage.Container.getInstance().managers[name]

		if searchRuler:
			return rulerFound

