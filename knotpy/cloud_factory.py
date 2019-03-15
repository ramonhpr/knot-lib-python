import logging
from .meshblu import Meshblu
from .fiware import Fiware

class CloudFactory(object):
    @staticmethod
    def init(platform, protocol):
        logging.info('Selecting cloud %s', platform)
        return {
            'MESHBLU': lambda: Meshblu(protocol, use_parent_conn=True),
            'FIWARE': lambda: Fiware(protocol),
        }.get(platform.upper())()
