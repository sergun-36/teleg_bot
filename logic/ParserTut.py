import requests
from bs4 import BeautifulSoup
import settings


logger = settings.logger

class ParserTut():
	movies_url = settings.TUT_MOVIES_URL


	"""
	Get html from url and return it
	"""
	def get_all_info_movies(self):
		try:
			res = requests.get(self.movies_url)
			status_code = res.status_code
			if status_code in settings.OK_CODES:
				movies_html = res.text
				logger.info(f"Request of movies is successfull. Status - {status_code}")
			else:
				logger.warning(f"Requests of movies is success. Status - {status_code}")
				movies_html = {"ok": False,
								"error_message": f"Requests of movies is failed. Status - {status_code}"}
		except Exception as ex:
			logger.error(f"Request of movies is failed. Error - {ex}")
			raise Exception(f"Request of movies is failed. Error - {ex}")

		return movies_html

	def get_movies_info(self, movies_html):
		soup_html = BeautifulSoup(movies_html, "lxml")
		links = soup_html.find_all("a", class_="header__link", title= True)
		for link in links:
			if link.string:
				print(link.string)
		logger.info(f"Printim links")


	def get_links_info(self, movies_html):
		soup_html = BeautifulSoup(movies_html, "lxml")
		links = soup_html.find_all("div", class_="a-event-header")
		for link in links:
			link = link.next_sibling
			aes = link.find_all('a')
			for a in aes:
				print(a.string)
			
		logger.info(f"Printim links")	
		

parser = ParserTut()
movies_html = parser.get_all_info_movies()
links=parser.get_links_info(movies_html)