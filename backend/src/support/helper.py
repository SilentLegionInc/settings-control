import datetime


def ceil_datetime_up_to_minutes(value):
    temp = value.replace(second=0, microsecond=0)
    if temp == value:
        return value
    else:
        return temp + datetime.timedelta(minutes=1)


def floor_datetime_up_to_minutes(value):
    return value.replace(second=0, microsecond=0)
