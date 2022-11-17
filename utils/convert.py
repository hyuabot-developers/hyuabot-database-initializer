from datetime import datetime


def convert_string_to_time(time: str) -> datetime:
    return datetime.fromisoformat(f"{time}:00+09:00")
