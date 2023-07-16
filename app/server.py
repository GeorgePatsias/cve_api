import json
import atexit
from os import path
from datetime import datetime, timedelta
from modules.Shared.Logger import logger
from modules.Shared.UserClass import User
from werkzeug.exceptions import HTTPException
from modules.Shared.Headers import server_headers
from modules.Shared.MongoClient import mongoClient
from modules.Monitoring.controllers import monitoring_scheduler
from flask_login import LoginManager, login_manager, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, send_from_directory, session, redirect, render_template
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, FLASK_THREADED, FLASK_SECRET, SESSION_EXPIRE, MONGO_DB, MONGO_ADMINS_COLLECTION, MONITORING_SCHEDULING_TIME

import modules.Login.routes
import modules.CveDB.routes
import modules.Admins.routes
import modules.Events.routes
import modules.Dashboard.routes
import modules.Monitoring.routes
import modules.Investigate.routes
import modules.Notifications.routes

app = Flask(__name__)
app.secret_key = FLASK_SECRET

app.register_blueprint(modules.Login.routes.app)
app.register_blueprint(modules.CveDB.routes.app)
app.register_blueprint(modules.Admins.routes.app)
app.register_blueprint(modules.Events.routes.app)
app.register_blueprint(modules.Dashboard.routes.app)
app.register_blueprint(modules.Monitoring.routes.app)
app.register_blueprint(modules.Investigate.routes.app)
app.register_blueprint(modules.Notifications.routes.app)


@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


@app.errorhandler(HTTPException)
def page_not_found(e):
    logger.info(f'{e.code} - {e.name} - {e.description}')

    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description,
    })
    response.content_type = 'application/json'
    return response


@app.route('/favicon.ico', methods=['GET'])
@server_headers
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = (u'Session time out, please re-login')
login_manager.needs_refresh_message_category = 'info'


@login_manager.user_loader
def load_user(username):
    try:
        mongo_client = mongoClient()
        col_admins = mongo_client[MONGO_DB][MONGO_ADMINS_COLLECTION]
        admin_exists = col_admins.find_one({'username': username}, {'_id': 0, 'username': 1, 'locked': 1})
        if not admin_exists:
            mongo_client.close()
            return

        if admin_exists.get('locked') == 'true':
            return

        user = User()
        user.id = username

        col_admins.update_one({'username': username}, {'$set': {'last_activity': datetime.now()}})
        mongo_client.close()

        return user

    except Exception as e:
        logger.exception(e)
        mongo_client.close()
        return None


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=SESSION_EXPIRE)
    session.modified = True


@app.route('/', methods=['GET'])
@server_headers
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard', code=302)
    return redirect('/login', code=302)


# Scheduler for Monitoring
scheduler = BackgroundScheduler()
scheduler.add_job(func=monitoring_scheduler, trigger='interval', minutes=MONITORING_SCHEDULING_TIME)
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    logger.info(f'Application started at {FLASK_HOST}:{FLASK_PORT}')
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
        threaded=FLASK_THREADED,
        # use_reloader=False
    )
