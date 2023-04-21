
import datetime

def parse_datetime_str(datetime_str):
    dt = datetime.datetime.fromisoformat(datetime_str[:-1])
    return dt.strftime('%Y-%m-%d %H:%M:%S')