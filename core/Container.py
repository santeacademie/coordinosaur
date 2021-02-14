class Container():

	_INSTANCE = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(Container._INSTANCE, Container):
			Container._INSTANCE = object.__new__(cls)

		return Container._INSTANCE


	def __init__(self):
		super().__init__()

		Container._INSTANCE = self
		self._managers = dict()

		self.logManager = None
		self.bagManager = None
		self.queueManager = None
		self.channelManager = None
		self.mqttManager = None
		self.quotasManager = None

	def stop(self):
		for k,m in self.managers.items():
			try:
				m.stop()
			except AttributeError:
				pass

	@staticmethod
	def getInstance():
		return Container._INSTANCE

	def getManager(self, managerName: str):
		return self._managers.get(managerName, None)

	@property
	def managers(self) -> dict:
		return self._managers

	def setManager(self, managerInstance):
		lcFirstFunc = lambda s: s[:1].lower() + s[1:] if s else ''
		managerName = lcFirstFunc(managerInstance.__class__.__name__)

		self._managers[managerName] = managerInstance
		setattr(self, managerName, managerInstance)