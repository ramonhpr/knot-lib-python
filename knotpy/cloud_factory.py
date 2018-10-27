import logging
from .Meshblu import Meshblu
from .Fiware import Fiware

class CloudFactory(object):
	@staticmethod
	def init(platform, protocol):
		logging.info('Selecting cloud ' + platform)
		return {
			'MESHBLU': lambda: Meshblu(protocol),
			'FIWARE': lambda: Fiware(protocol),
		}.get(platform.upper())()
