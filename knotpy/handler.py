from .evt_flag import *
import re
base64Pattern= re.compile('(?:[A-Za-z0-9+/]{4}){1,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)')

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
def handleRequestSetDataValue(value):
	if isinstance(value, str) and isBase64(value):
		return
	elif isinstance(value, int) or isinstance(value, float) or \
		isinstance(value, bool):
		return
	else:
		raise TypeError('Value must be string in base 64, number or bool')
def isBase64(s):
	return re.match(base64Pattern, s) != None
