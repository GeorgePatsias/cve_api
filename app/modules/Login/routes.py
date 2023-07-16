# TODO RECAPTCHA https://python.plainenglish.io/how-to-use-google-recaptcha-with-flask-dbd79d5ea193
from uuid import uuid4
from modules.Shared.Logger import logger
from modules.Shared.CSRF import CSRFClass
from modules.Shared.UserClass import User
from modules.Login.controllers import valid_user
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from config import MONGO_DB, MONGO_ADMINS_COLLECTION
from flask import Blueprint, render_template, request, redirect, escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user


app = Blueprint('login', __name__)


@app.route('/login', methods=['GET'])
@server_headers
def login_view():
    try:
        if current_user.is_authenticated:
            return redirect('/dashboard', code=302)

        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='')

    except Exception as e:
        logger.exception(e)
        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Invalid credentials!')


@app.route('/login', methods=['POST'])
@server_headers
def login_submit():
    try:
        if not CSRFClass().is_valid_csrf(request.form['csrf_token']):
            return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Please refresh the page and try again!')

        if current_user.is_authenticated:
            return redirect('/dashboard', code=302)

        if valid_user(request.form['username'], request.form['password']):
            authenticated_user = User()
            authenticated_user.id = escape(request.form['username'])
            authenticated_user.token = uuid4()
            login_user(authenticated_user, remember=False)

            return redirect('/dashboard', code=302)

        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Invalid credentials!')

    except Exception as e:
        logger.exception(e)
        return render_template('login.html', csrf_token=CSRFClass().generate_CSRF(), error_message='Something went wrong, please try again!')


@app.route('/logout', methods=['GET'])
@server_headers
@login_required
def logout():
    try:
        logout_user()
        return redirect('/login', code=302)

    except Exception as e:
        logger.exception(e)
        return redirect('/login', code=302)


@app.route('/reset-password', methods=['POST'])
@server_headers
@login_required
def reset_password():
    try:
        username = escape(request.form['username'])
        current_password = escape(request.form['current-password'])
        new_password = escape(request.form['new-password'])
        confirm_password = escape(request.form['confirm-password'])

        if new_password != confirm_password:
            return redirect('/dashboard', code=302)

        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]

        admin_exists = col_admins.find_one({'username': username, 'locked': 'false'}, {'_id': 0, 'username': 1, 'password': 1})

        if not admin_exists:
            mongo_client.close()
            return redirect('/login', code=302)

        if not check_password_hash(admin_exists.get('password'), current_password):
            mongo_client.close()
            return redirect('/dashboard', code=302)

        col_admins.update_one({'username': username}, {'$set': {'password': generate_password_hash(new_password)}}, upsert=False)

        mongo_client.close()

        logout_user()
        return redirect('/login', code=302)

    except Exception as e:
        logger.exception(e)
        return redirect('/dashboard', code=302)
