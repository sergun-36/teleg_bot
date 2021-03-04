import logging.config
import yaml
import dotenv
import os

dotenv.load_dotenv(".env")
bot_token=os.environ['TOKEN']
TELEG_ROOT_URL=f"https://api.telegram.org/bot{bot_token}"
OK_CODES=(200, 201, 202)

with open("logging.yaml", "r") as file :
	log_yaml_conf = yaml.safe_load(file.read())

logging.config.dictConfig(log_yaml_conf)
logger=logging.getLogger('simpleExample')