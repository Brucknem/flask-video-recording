from flask import current_app, send_file
import os
import pathlib
from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for

from blueprints.auth import login_required
from flask import session
from utils import get_recordings
from database import is_true, user_data_db

bp = Blueprint("index", __name__)


@bp.route('/', methods=("GET", "POST"))
@login_required
def index():
    user_id = session.get('user_id')
    values = user_data_db().get(user_id=user_id)

    recordings = get_recordings(user_id)
    return render_template('index.html',
                           url=values['url'],
                           prefix=values['prefix'],
                           flip=is_true(values['flip']),
                           recording=is_true(values['recording']),
                           my_recordings=recordings,
                           )


@ bp.route('/on_enter_in_text', methods=("POST", ))
@ login_required
def on_enter_in_text():
    user_id = session.get('user_id')
    user_data_db().update(user_id=user_id, url=request.form['url'])
    user_data_db().update(user_id=user_id, prefix=request.form['prefix'])
    return redirect(url_for('index'))


@ bp.route('/recordings/<path>', methods=['GET'])
@ login_required
def download(path):
    user_id = session.get('user_id')
    path = pathlib.Path(current_app.root_path) / \
        'recordings' / str(user_id) / path
    return send_file(str(path))
