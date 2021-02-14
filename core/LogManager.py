import logging

from core.ContainerAware import ContainerAware

class LogManager(ContainerAware):

	def __init__(self, name="main", level=logging.DEBUG):
		logging.basicConfig(
			filename="var/log/%s.log" % name,
			level=level,
			format='[%(asctime)s]:%(name)s:%(levelname)s:%(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)

	def info(self, msg):
		print(msg)
		logging.info(msg)

	def debug(self, msg):
		print(msg)
		logging.debug(msg)

	def error(self, msg):
		msg = "[Error] " + msg
		print(msg)
		logging.error(msg)

	def fatal(self, msg):
		print(msg)
		logging.fatal(msg)

	def critical(self, msg):
		print(msg)
		logging.critical(msg)

	def warning(self, msg):
		print(msg)
		logging.warning(msg)

