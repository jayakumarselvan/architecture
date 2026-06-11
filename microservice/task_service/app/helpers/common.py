from datetime import datetime


def get_current_timestamp_iso_format():
    current_datetime = datetime.now()
    iso_format = current_datetime.isoformat()
    return iso_format

