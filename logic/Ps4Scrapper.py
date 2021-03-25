from bs4 import BeautifulSoup
import requests
import settings

logger=settings.logger

class ParsesPs4():
	url_ps4 = settings.URL_PS4

	def get_discount_row(self):
		try:
			res = requests.get(self.url_ps4)
			status_code = res.status_code
			if status_code in settings.OK_CODES:
				all_disc_text = res.text
				logger.info(f"Request on ps4 is succsesfull. Status is {status_code}")
			else:
				all_disc_text = {"ok" : False,
								"error_message" : f"Response code: {status_code}"}
				logger.info(f"Request on ps4 is failed. Status is {status_code}")

		except Exception as e:
			logger.error(f"Request on ps4 is failed. Error - {e}")
			raise Exception(f"Request on ps4 is failed. Error - {e}")

		return all_disc_text

	def get_title(self, all_text=""):
		soup = BeautifulSoup(all_text, "lxml")
		links = soup.find_all('a')
		text=[]
		for link in links:
			text.append(link['class'])#data-telemetry-meta

		return text




pers=ParsesPs4()
all_text = pers.get_discount_row()
xml = pers.get_title(all_text)
print(xml)