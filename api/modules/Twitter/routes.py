import requests
from modules.Shared.Logger import logger
from flask import Blueprint, jsonify, request
from modules.Shared.Headers import server_headers
from config import TWITTER_URL, TWITTER_BEARER_TOKEN
from modules.Shared.Authentication import auth_required

app = Blueprint('twitter', __name__)


@app.route('/twitter', methods=['GET'])
@auth_required
@server_headers
def twitter_api():
    try:
        response_data = requests.get(TWITTER_URL, params=request.args, headers={'Authorization': TWITTER_BEARER_TOKEN}).json()

        return jsonify(response_data.get('data', [{}])), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'status': 'Something went wrong.'}), 400


# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Tweet-Lookup/get_tweets_with_bearer_token.py

# https://twitter.com/{username}/status/{tweet_id}
