import requests
from . import settings

from .TextAnalyzer import TextAnalyzer

logger=settings.logger

class TelegBot(TextAnalyzer):
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
						chat_id = updates["result"][-1]["message"]["chat"]["id"]
						text = updates["result"][-1]["message"]["text"]
						text_answer=self.do_analys_text(text)
						self.send_message(chat_id=chat_id, text=text_answer)
						last_message_id=dynamic_last_message_id
				else:
					pass
					#logger.info("Bot hasn't new message while")
			else:
				print(f"Can\'t take updates : {updates['error_message']}")
				logger.warning(f"Can\'t take updates : {updates['error_message']}")

	def webhook(self, url):
		response = requests.post(f"{self.root_url}/setWebhook", {"url":url})
		if response.status_code in settings.OK_CODES:
			return True
		else:
			return False

	def get_webhook_info(self, url):
		return requests.get(f"{self.root_url}/getWebhookInfo", {"url":url}).json()


