from datetime import datetime


def none_if_empty(string):
    return None if string == '' else string.strip()


def to_date_components(date):
    date_components = date.split('-')
    if len(date_components) == 3:
        return {'year': date_components[0],
                'month': date_components[1],
                'day': date_components[2]}
    else: 
        return None


def to_time_components(time):
    time_components = time.split(':')
    if len(time_components) == 2:
        return {'hour': time_components[0],
                'minutes': time_components[1]}
    else: 
        return None


def to_datetime(date_components, time_components):
    return datetime(int(date_components['year']), 
                    int(date_components['month']), 
                    int(date_components['day']), 
                    int(time_components['hour']), 
                    int(time_components['minutes']))


def to_event_date(date, time):
    event_time = time.split(' ')
    date_components = to_date_components(date)
    start_time_components = to_time_components(event_time[1])
    end_time_components = to_time_components(event_time[3])
    if date_components is not None and start_time_components is not None and end_time_components is not None:
        return {'start_datetime': to_datetime(date_components, start_time_components), 
                'end_datetime': to_datetime(date_components, end_time_components)}
    else :
        return None
