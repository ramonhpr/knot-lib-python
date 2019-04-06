from .evt_flag import FLAG_TIME, FLAG_LOWER, FLAG_UPPER

def handle_evt_flag_error(flags, time_sec, lower_limit, upper_limit):
    if FLAG_TIME&flags and not time_sec:
        raise Exception('event_flag requires time')
    if not FLAG_TIME&flags and time_sec:
        raise Exception('You must use FLAG_TIME in event_flag')

    if FLAG_LOWER&flags and not lower_limit:
        raise Exception('event_flag requires lower_limit')
    if not FLAG_LOWER&flags and lower_limit:
        raise Exception('You must use FLAG_LOWER in eventFlag')

    if FLAG_UPPER&flags and not upper_limit:
        raise Exception('eventFlag requires upper_limit')
    if not FLAG_UPPER&flags and upper_limit:
        raise Exception('You must use FLAG_UPPER in event_flag')
