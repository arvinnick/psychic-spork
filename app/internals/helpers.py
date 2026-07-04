from datetime import datetime


def datetime_converter(date_time:str) -> datetime:
    """
    converts iso formatted string containing datetime to python datetime object
    """
    return datetime.fromisoformat(date_time)