#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, send_from_directory
from contextlib import closing
from datetime import datetime, timedelta
import sqlite3
import os
from werkzeug.utils import secure_filename
import json

# Custom
from parse_json import parse_json

# Create application instance
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config.py')

# Define


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config[
               'ALLOWED_EXTENSIONS']


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response

# Placeholder: View function
@app.route('/', methods=['GET', 'POST'])
def inputfile():
    cur = g.db.execute(
        'select filename,desc,created,id from file_entries order by created desc')
    entries = [dict(filename=row[0], desc=row[1], created=row[
                    2], id=row[3]) for row in cur.fetchall()]

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('inputfile'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('inputfile'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current = datetime.now()
            g.db.execute('insert into file_entries (filename,desc,created) values (?, ?, ?)',
                         [file.filename, request.form['desc'], current])
            g.db.commit()
            message = "File upload finished successfully."
            return redirect(url_for('inputfile', message=message))

    current = datetime.now().strftime('%Y/%m/%d %H:%M')
    message = request.args.get('message', '')
    if not message:
        message = "Current time is " + current
    return render_template('inputfile.html', message=message, entries=entries)


@app.route('/output')
def output():
    fname = request.args.get('value').replace(' ','_')
    fpath = app.config['UPLOAD_FOLDER'] + fname
    jsonfile = open(fpath,'r')
    config = json.load(jsonfile)
    output = parse_json(config)

    return render_template('output.html', entries=output)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    id = request.args.get('value')
    g.db.execute("delete from file_entries where id = ?", [id])
    g.db.commit()
    return redirect(url_for('inputfile'))


# Start application
if __name__ == '__main__':
    app.run(host='0.0.0.0')
