import requests
from . import settings

class TelegBot():
	root_url=f"{settings.teleg_root_url}{settings.bot_token}"
	ok_codes=(200, 201, 202)


	def get_updates(self):
		response=requests.get(f"{self.root_url}/getUpdates")
		status_code=response.status_code
		if status_code in self.ok_codes:
			return response.json()
		else:
			raise Exception(f"Connection failes. Status {status_code}")


	def send_message(self, chat_id="", text=""):
		data={"chat_id":chat_id,
				"text":text}
		requests.post(f"{self.root_url}/sendMessage", data)


	def polling(self):
		last_message_id=0

		while True:
			updates=self.get_updates()

			if updates["result"]:
				dynamic_last_message_id=updates["result"][-1]["message"]["message_id"]
				if dynamic_last_message_id > last_message_id:
					self.send_message(chat_id=465377698, text="I am working")
					last_message_id=dynamic_last_message_id

