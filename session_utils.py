
from flask import redirect, request, session, url_for


DEFAULT_URL = 'http://192.168.178.20:5000/video_feed/pi2'
DEFAULT_PREFIX = ''
DEFAULT_FLIP = False
DEFAULT_RECORDING = False


def get_url():
    return session.get('url', DEFAULT_URL)


def get_prefix():
    return session.get('prefix', DEFAULT_PREFIX)


def get_flip():
    return bool(session.get('flip', DEFAULT_FLIP))


def get_user_id():
    return session.get('user_id')


def set_url(value):
    session['url'] = str(value)


def set_prefix(value):
    session['prefix'] = str(value)


def set_flip(value):
    session['flip'] = value


def toggle_flip():
    old_flip = get_flip()
    set_flip(not old_flip)
