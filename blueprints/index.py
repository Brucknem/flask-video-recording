import socket
import glob
import io
from zipfile import ZipFile
import zipfile
from flask import current_app, send_file
import os
import pathlib
from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for

from blueprints.auth import login_required
from flask import session
from utils import extract_host, get_recordings
from database import is_true, user_data_db


bp = Blueprint("index", __name__)


@bp.route('/', methods=("GET", "POST"))
@login_required
def index():
    user_id = session.get('user_id')
    values = user_data_db().get(user_id=user_id)

    preview_url = str(values['url'])
    if (host := extract_host(preview_url)) in ['0.0.0.0', '127.0.0.1']:
        external_ip = socket.gethostbyname(socket.gethostname())
        preview_url = preview_url.replace(host, external_ip)

    recordings = get_recordings(user_id)
    return render_template('index.html',
                           url=values['url'],
                           preview_url=preview_url,
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
    target = pathlib.Path(current_app.root_path) / \
        'recordings' / str(user_id) / path

    stream = io.BytesIO()
    with ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in glob.glob(os.path.join(target, '*.mp4')):
            zf.write(file, os.path.basename(file))
    stream.seek(0)
    return send_file(
        stream,
        as_attachment=True,
        download_name=f'{path}.zip')
