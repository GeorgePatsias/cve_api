import requests
from modules.Shared.Logger import logger
from config import REDDIT_OAUTH_URL, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_BASIC_TOKEN


def request_oauth():
    try:
        response_data = requests.post(REDDIT_OAUTH_URL,  headers={'Authorization': REDDIT_BASIC_TOKEN}, data={
            'grant_type': 'password',
            'username': REDDIT_USERNAME,
            'password': REDDIT_PASSWORD
        })

        return response_data.json().get('access_token', None)

    except Exception as e:
        logger.exception(e)
        return None
