from flask import current_app, send_file
import os
import pathlib
from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for

from blueprints.auth import login_required
from flask import session
from blueprints.record import is_recording
import session_utils
from utils import get_recordings

bp = Blueprint("index", __name__)


@bp.route('/', methods=("GET", "POST"))
@login_required
def index():
    url = session_utils.get_url()
    flip = session_utils.get_flip()
    my_recordings = get_recordings(session_utils.get_user_id())
    # recordings_prefix = str(pathlib.Path('recordings').joinpath(
    # str(session_utils.get_user_id())).joinpath(''))
    return render_template('index.html',
                           url=url,
                           prefix=session_utils.get_prefix(),
                           flip=flip,
                           recording=is_recording(session_utils.get_user_id()),
                           my_recordings=my_recordings,
                           recordings_prefix=get_recordings(
                               session_utils.get_user_id())
                           )


@ bp.route('/on_enter_in_text', methods=("POST", ))
@ login_required
def on_enter_in_text():
    session_utils.set_url(request.form['url'])
    session_utils.set_prefix(request.form['prefix'])
    return redirect(url_for('index'))


@bp.route('/recordings/<path>', methods=['GET'])
@ login_required
def download(path):
    path = pathlib.Path(current_app.root_path).joinpath('recordings').joinpath(
        str(session_utils.get_user_id())).joinpath(path)
    return send_file(str(path))
