from datetime import datetime
import pathlib
import time
import re


def extract_host(url: str):
    matcher = re.search('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', str(url))
    try:
        return matcher.group(0)
    except:
        return None


def format_timestamp(timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')


if __name__ == '__main__':
    print(format_timestamp())


def get_recordings(user_id):
    paths = [pathlib.Path(*p.parts[2:])
             for p in pathlib.Path("recordings").rglob(f"{user_id}/*")]
    return paths


if __name__ == '__main__':
    print(get_recordings(1))
