import json
from flask import Flask
from modules.Shared.Logger import logger
from werkzeug.exceptions import HTTPException

from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, FLASK_THREADED, FLASK_SECRET

import modules.NVD.routes
import modules.Github.routes
import modules.Reddit.routes
import modules.Twitter.routes
import modules.CVETrends.routes

app = Flask(__name__)
app.secret_key = FLASK_SECRET

app.register_blueprint(modules.NVD.routes.app)
app.register_blueprint(modules.Github.routes.app)
app.register_blueprint(modules.Reddit.routes.app)
app.register_blueprint(modules.Twitter.routes.app)
app.register_blueprint(modules.CVETrends.routes.app)


@app.errorhandler(HTTPException)
def page_not_found(e):
    logger.info(f'{e.code} - {e.name} - {e.description}')
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':
    logger.info('Application started')
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG,
        threaded=FLASK_THREADED
    )
