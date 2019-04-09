import logging
from .clouds.meshblu import Meshblu
from .clouds.fiware import Fiware
from .clouds.knot_cloud import KnotCloud

class CloudFactory(object):
    @staticmethod
    def init(platform, protocol):
        logging.info('Selecting cloud %s', platform)
        return {
            'MESHBLU': lambda: Meshblu(protocol, use_parent_conn=True),
            'FIWARE': lambda: Fiware(protocol),
            'KNOT_CLOUD': lambda: KnotCloud(protocol),
        }.get(platform.upper())()
