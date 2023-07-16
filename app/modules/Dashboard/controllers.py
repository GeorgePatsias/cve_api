import requests
from datetime import datetime
from config import API_URL, API_TOKEN
from modules.Shared.Logger import logger


def get_latest_cves():
    try:
        response = requests.get(f'{API_URL}/cve-trends/24h', headers={'x-api-token': API_TOKEN})

        if not response or response.status_code != 200:
            return None

        data = response.json()
        data['created_at'] = datetime.now()

        return data

    except Exception as e:
        logger.exception(e)
        return None


def get_latest_7d_cves():
    try:
        response = requests.get(f'{API_URL}/cve-trends/7d', headers={'x-api-token': API_TOKEN})

        if not response or response.status_code != 200:
            return None

        data = response.json()
        data['created_at'] = datetime.now()

        return data

    except Exception as e:
        logger.exception(e)
        return None
