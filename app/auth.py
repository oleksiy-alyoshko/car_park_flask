import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db_session, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db = db_session
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.query(User).filter(User.email == email).first():
            error = 'User {} is already registered'.format(email)
        if error is None:
            user = User(email=email, password=generate_password_hash(password))
            db.add(user)
            db.commit()
            import pdb; pdb.set_trace()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db = db_session
        error = None
        user = db.query(User).filter(User.email == email).first()
        if not user:
            error = 'Incorrect email.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(User).filter(User.user_id == user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
