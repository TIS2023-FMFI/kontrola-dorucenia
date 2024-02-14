import os
from dotenv import load_dotenv
PATH_TO_ENV = 'website/env'
load_dotenv(PATH_TO_ENV)

def get_env(key):
    return os.environ[key] if key in os.environ else None
