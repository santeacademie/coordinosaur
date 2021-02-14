from config import parameters

from core.ContainerAware import ContainerAware
import inspect

class BagManager(ContainerAware):

	MQTT_TOPIC_PREFIX = "coordinosaur"
	MQTT_CLIENT_NAME = "coordinosaur"
	MQTT_HOST = "localhost"
	MQTT_PORT = 1883
	MQTT_USERNAME = ""
	MQTT_PASSWORD = ""
	DEFAULT_TIMEOUT_OFFSET = 1
	DEFAULT_MAX_CONCURRENT_JOBS = 1
	DEFAULT_QUOTAS_PER_INTERVAL = {}
	CHANNEL_OPTIONS = {}

	def __init__(self):
		for member in (inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))):
			attrName = member[0]
			attrVal = member[1]

			if attrName.isupper() and attrName not in []:
				if attrName.upper() in parameters:
					setattr(self, attrName, parameters[attrName.upper()])
					# self.LogManager.info("[BagManager] Conf '"+str(attrName)+"' loaded with value '"+str(getattr(self, attrName))+"'")
				else:
					self.LogManager.info("[BagManager] Conf '"+str(attrName)+"' is invalid, using default: '"+str(attrVal)+"'")

