import requests
from . import settings
import logging

logger=logging.getLogger(__name__)
logging.basicConfig(filename="log.txt",format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class TelegBot():
	root_url=f"{settings.teleg_root_url}{settings.bot_token}"
	
	def get_updates(self):
		try:
			response=requests.get(f"{self.root_url}/getUpdates")
			status_code=response.status_code

			if status_code in settings.ok_codes:
				result=response.json()
				logger.warning(f"Updates was successful. Status {status_code}")
			else:
				result={"ok" : False,
						"error_message" : f"Response code: {status_code}"}
				print(f"Updates was not get successful. Status {status_code}")

			return result

		except Exception as e:
			raise Exception(f"Request was failed: {e}")


	def send_message(self, chat_id="", text=""):
		data={"chat_id" : chat_id,
				"text" : text}
		try:
			res=requests.post(f"{self.root_url}/sendMessage", data)
			print(res)
			if res.status_code in settings.ok_codes:
				print(f"Message was sent successful with status {res.status_code}")
			else:
				print(f"Message was not sent with status {res.status_code}")

		except Exception as e:
			raise Exception(f"Request was failed: {e}")



	def polling(self):
		last_message_id=0

		while True:
			updates=self.get_updates()

			if updates["ok"]:
				if updates["result"]:
					dynamic_last_message_id=updates["result"][-1]["message"]["message_id"]
					if dynamic_last_message_id > last_message_id:
						self.send_message(chat_id=167233877, text="I am working")
						last_message_id=dynamic_last_message_id
			else:
				print(f"Can\'t take updates : {updates['error_message']}")

