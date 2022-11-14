from datetime import datetime


def convert_string_to_time(time: str) -> datetime:
    return datetime.fromisoformat(f"1998-12-12T{time}:00+09:00")
