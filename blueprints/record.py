import pathlib
import threading
from flask import Blueprint, redirect, render_template, request, session, url_for
import cv2

from blueprints.auth import login_required
import session_utils
from utils import get_timestamp

bp = Blueprint("record", __name__, url_prefix='/record')

_recording = {}
_flip_image = {}


def is_recording(user_id: str):
    return _recording.get(user_id, False)


def stop_writer():
    global _writer
    if _writer is not None:
        _writer.release()


def record_thread(user_id: str, url: str, path: str):
    global _recording, _flip_image

    capture = cv2.VideoCapture(url)
    writer = None

    path: pathlib.Path = pathlib.Path("recordings").joinpath(
        str(user_id)).joinpath(f'{path}_{get_timestamp()}.mp4')
    path.parent.mkdir(exist_ok=True, parents=True)

    try:
        while _recording[user_id]:
            rval, frame = capture.read()
            if not rval:
                continue

            if writer == None:
                height, width, _ = frame.shape
                size = (width, height)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                writer = cv2.VideoWriter(str(path), fourcc, 20.0, size)

            if _flip_image.get(user_id, False):
                frame = cv2.flip(frame, 0)

            writer.write(frame)
    finally:
        _recording[user_id] = False
        if writer is not None:
            writer.release()


@ bp.route('/start', methods=("POST", ))
@ login_required
def start_record():
    user_id = session_utils.get_user_id()
    if is_recording(user_id):
        return redirect(url_for('index'))

    url = request.form['url']
    path = request.form['path']

    session_utils.set_url(url)
    session_utils.set_path(path)

    _recording[user_id] = True
    threading.Thread(target=record_thread,
                     args=(user_id, url, path)).start()

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

    return redirect(url_for('index'))
