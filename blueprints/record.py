import logging
import pathlib
import threading
import time
from flask import Blueprint, redirect, render_template, request, session, url_for
import cv2

from blueprints.auth import login_required
from db import Database
import session_utils
from utils import format_timestamp
import db

bp = Blueprint("record", __name__, url_prefix='/record')

_recording = {}
_flip_image = {}


def is_recording(user_id: str):
    return _recording.get(user_id, False)


def record_thread(connection, user_id: str, url: str, prefix: str):
    global _recording, _flip_image

    url = db.get_url(user_id, connection)

    if prefix:
        prefix = pathlib.Path(prefix) / format_timestamp()
    else:
        prefix = format_timestamp()

    writer = None
    capture = None
    last_timestamp = 0

    def get_file(timestamp):
        path: pathlib.Path = pathlib.Path("recordings") /\
            str(user_id) / prefix / f'{format_timestamp(timestamp)}.mp4'
        path.parent.mkdir(exist_ok=True, parents=True)
        return str(path)

    def is_next_chunk(now):
        difference = now - last_timestamp
        return difference > (60 * 5)

    _recording[user_id] = True
    while _recording[user_id]:
        try:
            now = time.time()
            if capture is None or is_next_chunk(now):
                capture = cv2.VideoCapture(url)
                if not capture.isOpened():
                    raise ConnectionError(f"Couldn't connect to stream")

            rval, frame = capture.read()
            if not rval:
                raise ConnectionError(f"Couldn't read frame")

            if writer is None or is_next_chunk(now):
                path = get_file(now)

                height, width, _ = frame.shape
                size = (width, height)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                writer = cv2.VideoWriter(path, fourcc, 20.0, size)

            if _flip_image.get(user_id, False):
                frame = cv2.flip(frame, 0)

            if is_next_chunk(now):
                last_timestamp = now

            writer.write(frame)
        except Exception as e:
            logging.warn(f'Error while recording for user {user_id}: {e}')
            last_timestamp = 0

            if writer is not None:
                writer.release()
            writer = None

            if capture is not None:
                capture.release()
            capture = None


@ bp.route('/start', methods=("POST", ))
@ login_required
def start_record():
    user_id = session_utils.get_user_id()
    if is_recording(user_id):
        return redirect(url_for('index'))

    url = request.form['url']
    prefix = request.form['prefix']

    session_utils.set_url(url)
    session_utils.set_prefix(prefix)

    threading.Thread(target=record_thread,
                     args=(get_db(), user_id, url, prefix)).start()

    return redirect(url_for('index'))


@ bp.route('/stop', methods=("POST", ))
@ login_required
def stop_record():
    _recording[session_utils.get_user_id()] = False
    return redirect(url_for('index'))


@ bp.route('/flip', methods=('POST', ))
def toggle_flip_image():
    session_utils.toggle_flip()
    flip = session_utils.get_flip()
    _flip_image[session_utils.get_user_id()] = flip

    return "Success"
