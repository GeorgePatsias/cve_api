FLASK_HOST = "0.0.0.0"
FLASK_PORT = "8080"
FLASK_DEBUG = "True"
FLASK_THREADED = "True"
FLASK_SECRET = "dl7kWU9leuy5i2I6bCdTrJPBouxvCoQ18uXKZD65AB0WvQOjdjntCvjwsJbK"
LOGGER_PATH = "./logs/app.log"
SESSION_EXPIRE = 86400
CSRF_TIME_TO_LIVE = 10

MONITORING_SCHEDULING_TIME = 1  # Minutes

API_URL = ""
API_TOKEN = ""

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"  # Chrome

MONGO_CONNECTION = "mongodb://{}:{}@localhost:27017/"
MONGO_CONNECT_TIMEOUT = 5000
MONGO_USER = "root"
MONGO_PASS = "MkWTWPM8IMnncaX99S0eLR7DztFUhkqhgtylfeOJIOoVM04k6llo66R8B0Ce"
MONGO_DB = "db_cve_app"
MONGO_CSRF_COLLECTION = "col_csrf"
MONGO_ADMINS_COLLECTION = "col_admins"
MONGO_CVE_NVD_COLLECTION = "col_cve_nvd"
MONGO_CVE_TRENDS_COLLECTION = "col_cve_trends"
MONGO_MONITORING_COLLECTION = "col_monitoring"
MONGO_NOTIFICATIONS_COLLECTION = "col_notifications"


NVD_API_KEY = ""

TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""

GITHUB_URL = "https://api.github.com/search/repositories"

CWE_URL = "https://cwe.mitre.org/data/definitions"
