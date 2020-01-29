import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_login import login_required, logout_user, login_user, current_user
from flask_admin import helpers
from flask_uploads import UploadSet
from app import app, db, login_manager, logUpload
from .forms import LoginForm, UploadForm
from .models import User, Upload


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route('/')
@app.route('/index')
def index():
    if session.get('logged_in'):
        return render_template('layout.html')
    else:
        return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    flash(u'New entry was successfully posted', 'info')
    return redirect(url_for('index'))


@app.route('/admin_user')
@login_required
def show_user():
    users = User.query.all()
    return render_template('admin/show_user.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()

    if form.validate_on_submit():
        user = form.user
        login_user(user)
        session['logged_in'] = True
        flash(u'You were logged in', 'success')
        return redirect(url_for('index'))
    else:
        flash_errors(form)

    return render_template('login.html', error=error, form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    error = None
    form = UploadForm()
    if form.validate_on_submit():
        if request.method == 'POST' and 'upload' in request.files:
            filename = logUpload.save(request.files['upload'])
            file = Upload(filename=filename, user_id=current_user.id)
            db.session.add(file)
            db.session.commit()

            flash('Log saved' ,'success')
            return redirect(url_for('show_uploads'))
    else:
        flash('something goes wrong!', 'danger')

    return render_template('upload.html', form=form)


@app.route('/show_uploads')
def show_uploads():
    files = Upload.query.all()

    return render_template('show_uploads.html', files=files)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash(u'You were logged out', 'success')
    return redirect(url_for('index'))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')