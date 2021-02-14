import paho.mqtt.client as paho
import json
import time
import math
import random

from model.Job import Job
from core.ContainerAware import ContainerAware

class MqttManager(ContainerAware):

	def __init__(self):
		self._disconnectedSince = None
		self._client = None

		self.init()

	def init(self):
		self._client = paho.Client(self.BagManager.MQTT_CLIENT_NAME + '_' + str(time.time()) + '_' + str(random.getrandbits(32)))
		self._client.on_connect = self.onConnect
		self._client.on_disconnect = self.onDisconnect
		self._client.on_message = self.onMessage
		self._client.on_log = self.onLog

	def onLog(self, client, userdata, level, buf):
		if level != 16:
			self.LogManager.debug(buf)

	def onConnect(self, client, userdata, flags, rc):
		self.LogManager.info("[MqttServer] Connected to MQTT server")
		self.subscribe(self.BagManager.MQTT_TOPIC_PREFIX + "/#")

		if self._disconnectedSince is not None:
			self.LogManager.info("[MqttServer] Lost connection for '"+str(math.floor(time.time() - self._disconnectedSince))+"' seconds")
			self._disconnectedSince = None

	def onDisconnect(self, client, userdata, rc):
		self.LogManager.info("[MqttServer] Disconnected from MQTT server")
		self._disconnectedSince = time.time()

	def start(self, forever=True):
		self.LogManager.info("[MqttServer] Trying to Connect on MQTT server...")
		self._disconnectedSince = None

		self._client.username_pw_set(username=self.BagManager.MQTT_USERNAME, password=self.BagManager.MQTT_PASSWORD)
		self._client.connect(self.BagManager.MQTT_HOST, self.BagManager.MQTT_PORT)
		self.LogManager.info("[MqttServer] Coordinator ready...")

		if forever:
			self._client.loop_forever()

	def subscribe(self, topic):
		self.LogManager.info("[MqttServer] Subscribe on topic '"+str(topic)+"'")
		self._client.subscribe(topic)

	def unsubscribe(self, topic):
		self.LogManager.info("[MqttServer] Unsubscribe on topic '"+str(topic)+"'")
		self._client.unsubscribe(topic)



	def publish(self, topic:str, payload, json:bool = False, noTopicPrefix:bool = False):
		if not noTopicPrefix:
			topic = self.BagManager.MQTT_TOPIC_PREFIX + '/' + topic

		if json:
			payload = json.dumps(payload)

		self._client.publish(topic=topic, payload=payload)


	def onMessage(self, client, data, mqttMessage):
		topic = mqttMessage.topic

		msg = str(mqttMessage.payload.decode("utf-8", "ignore"))
		msgJson = None

		try:
			msgJson = json.loads(msg)
		except:
			msgJson = dict()

		[root, channelName, actionName] = topic.split('/', 2)

		if actionName in ['register', 'finished', 'aborted', 'concurrency/set', 'infos']:
			self.LogManager.debug('[MqttManager] ' + topic + ' => ' + msg)
		else:
			return

		channel = self.QueueManager.checkChannel(channelName)

		if actionName == 'register':
			job = Job(uid=str(msgJson['uid']), ttl=int(msgJson['timeout']))
			self.QueueManager.register(channel, job)
		elif actionName == 'finished':
			self.QueueManager.finished(channel, jobUid=msg)
		elif actionName == 'aborted':
			self.QueueManager.aborted(channel, jobUid=msg)
		elif actionName == 'concurrency/set':
			self.LogManager.debug("[Channel] concurrency set to {}".format(msg))
			channel.maxConcurrentJobs = int(msg)

		self.QueueManager.infos(channel)
