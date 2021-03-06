import requests
from . import settings

logger=settings.logger

class TelegBot():
	root_url=settings.TELEG_ROOT_URL
	
	def get_updates(self):
		try:
			response=requests.get(f"{self.root_url}/getUpdates")
			status_code=response.status_code

			if status_code in settings.OK_CODES:
				result=response.json()
				logger.info(f"Updates was successfull. Status {status_code}")
			else:
				result={"ok" : False,
						"error_message" : f"Response code: {status_code}"}
				logger.warning(f"Updates didn't get. Status {status_code}")

			return result

		except Exception as e:
			logger.error(f"Request was failed: {e}")
			raise Exception(f"Request was failed: {e}")


	def send_message(self, chat_id="", text=""):
		data={"chat_id" : chat_id,
				"text" : text}
		try:
			res=requests.post(f"{self.root_url}/sendMessage", data)
			if res.status_code in settings.OK_CODES:
				logger.info(f"Message was sent successful with status {res.status_code}")
			else:
				logger.warning(f"Message was not sent with status {res.status_code}")
				
		except Exception as e:
			logger.error(f"Request was failed: {e}")
			raise Exception(f"Request was failed: {e}")



	def polling(self):
		last_message_id=0

		while True:
			updates=self.get_updates()

			if updates["ok"]:
				if updates["result"]:
					dynamic_last_message_id=updates["result"][-1]["message"]["message_id"]
					if dynamic_last_message_id > last_message_id:
						self.send_message(chat_id=465377698, text="I am working")
						last_message_id=dynamic_last_message_id
				else:
					logger.info("Bot haven't updates while")
			else:
				print(f"Can\'t take updates : {updates['error_message']}")
				logger.warning(f"Can\'t take updates : {updates['error_message']}")

