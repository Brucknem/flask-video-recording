from datetime import datetime
import time


def get_timestamp():
    now = time.time()
    return datetime.fromtimestamp(now).strftime('%Y-%m-%d_%H-%M-%S')


if __name__ == '__main__':
    print(get_timestamp())
