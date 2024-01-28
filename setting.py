import os
from dotenv import load_dotenv
load_dotenv()

API_HOST = os.getenv('API_HOST', 'localhost')
DB_HOST = os.getenv('DB_HOST', 'localhost')

STORE_DB = os.getenv('STORE_DB', 'omnivore')
STORE_COLLECTION = os.getenv('STORE_COLLECTION', 'store')

LOG_DB = os.getenv('LOG_DB', 'log')
LOG_COLLECTION = os.getenv('LOG_COLLECTION', 'time')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')