from datetime import datetime
import time


def format_timestamp(timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')


if __name__ == '__main__':
    print(format_timestamp())
