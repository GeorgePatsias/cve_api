import json
import nvdlib
import requests
import lxml.html
from datetime import datetime
from urllib.parse import quote
from modules.Shared.Logger import logger
from modules.Shared.MongoClient import mongoClient
from config import API_URL, API_TOKEN, MONGO_DB, MONGO_CVE_TRENDS_COLLECTION, MONGO_CVE_NVD_COLLECTION, NVD_API_KEY, CWE_URL, USER_AGENT


def get_github(cve_id):
    try:
        github_data = requests.get(f'{API_URL}/github/cve?q={cve_id}&sort=relevance', headers={'x-api-token': API_TOKEN}).json()

        if not github_data:
            return []

        github_items = github_data.get('items', None)
        if not github_items:
            return []

        github_posts_list = []
        for github_post in github_items:
            try:
                github_posts_list.append({
                    'created': github_post.get('created_at', ''),
                    'description': github_post.get('description', ''),
                    'language': github_post.get('language', ''),
                    'name': github_post.get('name', ''),
                    'topics': github_post.get('topics', ''),
                    'updated': github_post.get('updated_at', ''),
                    'stars': github_post.get('stargazers_count', ''),
                    'forks': github_post.get('forks_count', ''),
                    'watchers': github_post.get('watchers_count', ''),
                    'url': github_post.get('html_url', ''),
                    'owner': github_post.get('owner').get('login', ''),
                    'owner_logo': github_post.get('owner').get('avatar_url', ''),
                    'owner_url': github_post.get('owner').get('html_url', '')
                })
            except Exception as e:
                logger.exception(e)
                continue

        return github_posts_list

    except Exception as e:
        logger.exception(e)
        return []


def get_reddit(cve_id):
    try:
        reddit_data = requests.get(f'{API_URL}/reddit?q={cve_id}&sort=relevance', headers={'x-api-token': API_TOKEN}).json()

        if not reddit_data:
            return []

        reddit_documents = reddit_data.get('data', {}).get('children', {})

        if not reddit_documents:
            return []

        reddit_posts = []
        for reddit_doc in reddit_documents:
            try:
                reddit_doc = reddit_doc.get('data')

                reddit_posts.append({
                    'author': reddit_doc.get('author', ''),
                    'created': datetime.fromtimestamp(reddit_doc.get('created', '0')),
                    'is_self': reddit_doc.get('is_self', ''),
                    'num_comments': reddit_doc.get('num_comments', ''),
                    'permalink': f"https://reddit.com{quote(reddit_doc.get('permalink', ''))}",
                    'url': reddit_doc.get('url', ''),
                    'subreddit': reddit_doc.get('subreddit', ''),
                    'subreddit_subscribers': reddit_doc.get('subreddit_subscribers', ''),
                    'title': reddit_doc.get('title', ''),
                    'upvotes': reddit_doc.get('ups', ''),
                    'text': reddit_doc.get('selftext', ''),
                    'text_html': reddit_doc.get('selftext_html', ''),
                    'thumbnail': reddit_doc.get('thumbnail', ''),
                })
            except Exception as e:
                logger.exception(e)

        return reddit_posts

    except Exception as e:
        logger.exception(e)
        return []


def get_twitter(cve_id):
    try:
        # TODO Connection with Twitter API, ONLY CVE trends for now

        mongo_client = mongoClient()
        col_cve_trends = mongo_client[MONGO_DB][MONGO_CVE_TRENDS_COLLECTION]

        twitter_data = col_cve_trends.find_one({'data.cve': cve_id}, {'_id': 0})
        if not twitter_data:
            return []

        twitter_data = twitter_data.get('data')[0].get('tweets', [])

        return twitter_data

    except Exception as e:
        logger.exception(e)
        return []


def get_cwe(cwe_data):
    try:
        if not cwe_data:
            return []

        cwe_list = []
        for cwe in cwe_data:
            cwe_id = cwe.get('value', None)

            if not cwe_id:
                cwe_id = cwe.get('cwe_id', None)

            if not cwe_id.startswith('CWE-'):
                continue

            cwe_url = f"{CWE_URL}/{cwe_id.split('-')[1]}.html"
            response = requests.get(cwe_url, headers={'User-Agent': USER_AGENT}).text

            try:
                html_tree = lxml.html.fromstring(response)
                cwe_description = html_tree.xpath("//*[@id='Contentpane']/div[2]/h2")[0].text_content()
                cwe_description = cwe_description.split(f'{cwe_id}: ')[1].strip()

                cwe_list.append({
                    'cwe_id': cwe_id,
                    'cwe_description': cwe_description,
                    'cwe_url': cwe_url
                })
            except Exception:
                logger.warning(f'Could not get CWE description: {cwe_id}')
                continue

        return cwe_list

    except Exception as e:
        logger.exception(e)
        return []


def get_nvd(cve_id=None, monitoring_data=None):
    try:
        response_data = monitoring_data

        if not monitoring_data:
            response_data = nvdlib.searchCVE(cveId=cve_id, key=NVD_API_KEY)
            if not response_data:
                return None

            response_data = json.loads(json.dumps(response_data, default=lambda o: o.__dict__, sort_keys=True))[0]

        cve_urls = []
        for doc in response_data.get('references', {}):
            cve_urls.append(doc.get('url', ''))

        logger.info(f"Monitoring - Investigating: {response_data.get('id')}")
        final_document = {
            'cve': response_data.get('id'),
            'cve_urls': cve_urls or [],
            'assigner': response_data.get('sourceIdentifier', ''),
            'publishedDate': response_data.get('published', ''),
            'lastModifiedDate': response_data.get('lastModified', ''),
            'description': response_data.get('descriptions')[0].get('value', 'Pending'),
            'cvssv2_base_score': response_data.get('v2score', 'Pending'),
            'cvssv2_severity': response_data.get('v2severity', 'Pending'),
            'cvssv3_base_score': response_data.get('v31score', 'Pending'),
            'cvssv3_base_severity': response_data.get('v31severity', 'Pending'),
            'epss_score': response_data.get('v31exploitability', 'Pending'),
            'score': response_data.get('v31impactScore', 'Pending'),
            'severity': response_data.get('v31severity', 'Pending'),
            'cwes': get_cwe(response_data.get('cwe', [])),
            'vendor_advisories': [],
            'vendors': [],
        }

        return final_document

    except Exception as e:
        logger.exception(e)
        return None


def get_final_result_cve(cve_id, monitoring_data=None):
    try:

        final_document = get_nvd(cve_id, monitoring_data)
        final_document['db_insert'] = datetime.now()
        final_document['reddit_posts'] = get_reddit(cve_id)
        final_document['github_repos'] = get_github(cve_id)
        final_document['audience_size'] = 0
        final_document['num_retweets'] = 0
        final_document['num_tweets'] = 0
        final_document['num_tweets_and_retweets'] = 0
        final_document['timegraph_data'] = []
        final_document['tweets'] = get_twitter(cve_id)

        return final_document

    except Exception as e:
        logger.exception(e)
        return None


def investigate_cve(cve_id):
    try:
        mongo_client = mongoClient()
        col_cve_nvd = mongo_client[MONGO_DB][MONGO_CVE_NVD_COLLECTION]

        # If CVE is present in CVE NIST
        cve_results = col_cve_nvd.find_one({'cve': cve_id}, {'_id': 0})

        if cve_results:
            cve_data_creation = cve_results.get('db_insert', None).date()

            if cve_data_creation == datetime.now().date():
                logger.info(f'CVE: {cve_id} exists in NVD.')
                return cve_results

        # Get fresh data from sources
        cve_results = get_final_result_cve(cve_id, None)
        if not cve_results:
            return {}

        col_cve_nvd.update_one({'cve': cve_id}, {'$set': cve_results}, upsert=True)

        # col_cve_nvd.insert_one(cve_results)

        return cve_results

    except Exception as e:
        logger.exception(e)
        return {}
