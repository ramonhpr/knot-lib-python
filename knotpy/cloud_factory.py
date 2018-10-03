import logging
from .proto import KnotProtocol

class CloudFactory(object):
	@staticmethod
	def init(platform, protocol):
		logging.info('Selecting cloud ' + platform)
		return {
			'MESHBLU': KnotProtocol(protocol),
		}.get(platform)