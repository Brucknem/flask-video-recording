
from flask import redirect, request, session, url_for


DEFAULT_URL = 'http://192.168.178.20:5000/video_feed/pi2'
DEFAULT_PATH = 'video'
DEFAULT_FLIP = False
DEFAULT_RECORDING = False

RECORD_URL_COOKIE = 'URL'
RECORD_PATH_COOKIE = 'PATH'
RECORD_FLIP_COOKIE = 'FLIP'


def get_url():
    return session.get('url', DEFAULT_URL)


def get_path():
    return session.get('path', DEFAULT_PATH)


def get_flip():
    return bool(session.get('flip', DEFAULT_FLIP))


def get_user_id():
    return session.get('user_id')


def set_url(value):
    session['url'] = str(value)


def set_path(value):
    session['path'] = str(value)


def set_flip(value):
    session['flip'] = value


def toggle_flip():
    old_flip = get_flip()
    set_flip(not old_flip)
