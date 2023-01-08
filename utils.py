from datetime import datetime
import pathlib
import time


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
