def milliseconds_to_hms(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def milliseconds_to_ms(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def hms_to_milliseconds(hms):
    hms_list = hms.split(":")
    hours, minutes, seconds = map(int, hms_list)
    return ((hours * 60 + minutes) * 60 + seconds) * 1000

def ms_to_milliseconds(ms):
    ms_list = ms.split(":")
    minutes, seconds = map(int, ms_list)
    return (minutes * 60 + seconds) * 1000
