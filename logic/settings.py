import logging.config
import yaml
import dotenv
import os

with open("logging.yaml", "r") as file :
	log_yaml_conf = yaml.safe_load(file.read())

logging.config.dictConfig(log_yaml_conf)
logger = logging.getLogger('simpleExample')

dotenv.load_dotenv(".env")
bot_token = os.environ['TOKEN']
webhook_url_root = os.environ['WEBHOOK_URL']

TELEG_ROOT_URL = f"https://api.telegram.org/bot{bot_token}"
WEBHOOK_URL = f"{webhook_url_root}/{bot_token}"

OK_CODES = (200, 201, 202)
RB_BANK_ROOT_URL = "https://www.nbrb.by/api/exrates/rates"





TUT_MOVIES_URL = "https://afisha.tut.by/film/"

KIEV_MOVIES_URL = "https://kinoafisha.ua/kinoafisha/"

MAX_LIMIT_TEXT = 4096

CITIES = ("Минск", "Киев", "Minsk", "Kiev")