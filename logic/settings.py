import logging.config
import yaml
import dotenv
import os

dotenv.load_dotenv(".env")
bot_token=os.environ['TOKEN']
teleg_root_url="https://api.telegram.org/bot"
ok_codes=(200, 201, 202)

with open("logging.yaml", "r") as file :
	log_yaml_conf = yaml.safe_load(file.read())

logging.config.dictConfig(log_yaml_conf)
logger=logging.getLogger('simpleExample')