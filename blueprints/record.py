import logging
import pathlib
import threading
import time
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
import cv2

from blueprints.auth import login_required
from utils import format_timestamp
from database import is_true, user_data_db, UserdataDatabaseConnection

bp = Blueprint("record", __name__, url_prefix='/record')


def record_thread(user_id: int, location: str):
    connection = UserdataDatabaseConnection(location)

    url = connection.get(user_id=user_id)['url']
    prefix = connection.get(user_id=user_id)['prefix']

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

    connection.update(user_id=user_id, recording=True)
    while is_true(connection.get(user_id=user_id)['recording']):
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

            if is_true(connection.get(user_id=user_id)['flip']):
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
    user_id = session.get('user_id')
    if is_true(user_data_db().get(user_id=user_id)['recording']):
        return redirect(url_for('index'))

    url = request.form['url']
    prefix = request.form['prefix']

    db = user_data_db()
    db.update(user_id=user_id, url=url, prefix=prefix)

    threading.Thread(target=record_thread,
                     args=(user_id, current_app.config['DATABASE'])).start()

    return redirect(url_for('index'))


@ bp.route('/stop', methods=("POST", ))
@ login_required
def stop_record():
    user_id = session.get('user_id')
    user_data_db().update(user_id=user_id, recording=False)
    return redirect(url_for('index'))


@ bp.route('/flip', methods=('POST', ))
def toggle_flip_image():
    user_id = session.get('user_id')
    flip = is_true(user_data_db().get(user_id=user_id)['flip'])
    user_data_db().update(user_id=user_id, flip=not flip)

    return "Success"
