from enum import IntEnum

class EvtFlagsEnum(IntEnum):
	FLAG_TIME=1
	FLAG_LOWER=2
	FLAG_UPPER=4
	FLAG_CHANGE=8
	FLAG_MAX=1+2+4+8