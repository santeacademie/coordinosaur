import signal
import sys

from core.LogManager import LogManager
from core.BagManager import BagManager
from core.QueueManager import QueueManager
from core.QuotasManager import QuotasManager
from core.ChannelManager import ChannelManager
from core.MqttManager import MqttManager
from core.Container import Container

container = Container()

logManager = LogManager(name="main")
container.setManager(logManager)

bagManager = BagManager()
container.setManager(bagManager)

quotasManager = QuotasManager()
container.setManager(quotasManager)

channelManager = ChannelManager()
container.setManager(channelManager)

queueManager = QueueManager()
container.setManager(queueManager)

mqttManager = MqttManager()
container.setManager(mqttManager)

def exitHandler(signalNumber = None, stackFrame = None):
    logManager.info('Exiting coordinosaur...')
    container.stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, exitHandler)

try:
    logManager.info('Starting coordinosaur...')
    mqttManager.start()
except KeyboardInterrupt:
    exitHandler()
