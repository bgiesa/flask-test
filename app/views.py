import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_login import login_required, logout_user, login_user
from flask_admin import helpers, expose
from app import app, login_manager
from .forms import LoginForm
from .models import User


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
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/admin_user')
@login_required
def show_user():
    users = User.query.all()
    return (render_template('admin/show_user.html',users=users))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()

    if form.validate_on_submit():
        user = form.user
        login_user(user)
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('index'))
    else:
        flash_errors(form)        

    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))    