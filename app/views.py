import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_login import login_required, logout_user, login_user
from app import app, login_manager
from .forms import LoginForm
from .models import User


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

@app.route('/')
@app.route('/index')
def show_entries():
    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # entries = cur.fetchall()
    # return render_template('show_entries.html', entries=entries)
    return render_template('layout.html')

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    # db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    # db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/admin_user')
@login_required
def show_user():    
    return (render_template('admin/show_user.html',users=users))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # error = None
    # if request.method == 'POST':
    #     if request.form['username'] != app.config['USERNAME']:
    #         error = 'Invalid username'
    #     elif request.form['password'] != app.config['PASSWORD']:
    #         error = 'Invalid password'
    #     else:
    #         session['logged_in'] = True
    #         flash('You were logged in')
    #         return redirect(url_for('show_entries'))
    error = None
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=request.form['username']).first()
        if user.password != request.form['password']:
            error = 'Invalid Password'
        else:
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('show_entries'))

    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    logout_user()
    # session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))