from .evt_flag import *

def handleEvtFlagError(flags, timeSec, lowerLimit, upperLimit):
	if FLAG_TIME&flags and not timeSec:
		raise Exception('eventFlag require time')
	if FLAG_LOWER&flags and not lowerLimit:
		raise Exception('eventFlag require lowerLimit')
	if FLAG_UPPER&flags and not upperLimit:
		raise Exception('eventFlag require upperLimit')

def handleResponseError(res):
	if isinstance(res, dict):
		if res.get('error'):
			if isinstance(res.get('error'), dict):
				raise Exception(res.get('error').get('message'))
			elif isinstance(res, dict) and res.get('Error'):
				raise Exception(res.get('Error'))
			else:
				raise Exception(res.get('error'))
		elif res.get('code') == 404 or res.get('code') == 401:
			raise Exception(res.get('message'))
		else:
			return res
	else:
		return res
