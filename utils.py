from datetime import datetime
import pathlib
import time
import re
import socket


def get_local_ip():
    def locals():
        return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]

    def others():
        return [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    return (((locals() or [others()]) + ["no IP found"])[0])


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
