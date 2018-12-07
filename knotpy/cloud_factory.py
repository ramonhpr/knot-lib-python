import logging
from .Meshblu import Meshblu
from .Fiware import Fiware

class CloudFactory():
    @staticmethod
    def init(platform, protocol):
        logging.info('Selecting cloud %s', platform)
        return {
            'MESHBLU': lambda: Meshblu(protocol),
            'FIWARE': lambda: Fiware(protocol),
        }.get(platform.upper())()
