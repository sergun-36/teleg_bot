import requests
from bs4 import BeautifulSoup
#import settings
from . import settings


logger = settings.logger

class ParserTut():
	movies_url = settings.TUT_MOVIES_URL


	"""
	Get html from url and return it
	"""
	def get_movies_html(self):
		try:
			res = requests.get(self.movies_url)
			status_code = res.status_code
			if status_code in settings.OK_CODES:
				movies_html = res.text
				movies_html = {"ok": True,
								"html": movies_html}

				logger.info(f"Request of movies is successfull. Status - {status_code}")
			else:
				logger.warning(f"Requests of movies is failed. Status - {status_code}")
				movies_html = {"ok": False,
								"error_message": f"Requests of movies is failed. Status - {status_code}"}
		except Exception as ex:
			logger.error(f"Request of movies is failed. Error - {ex}")
			raise Exception(f"Request of movies is failed. Error - {ex}")

		return movies_html


	"""
	get all commun divs with cinema, films and times info from html
	"""
	def get_comun_divs(self, movies_html):
		if movies_html["ok"]:
			soup_html = BeautifulSoup(movies_html["html"], "lxml")
			divs = soup_html.find_all("div", class_="a-event-i")
			if divs:
				logger.info("Divs with info get success")
				divs = {"ok": True,
						"divs": divs}
			else:
				logger.warning("Divs are empty")
				divs = {"ok": False,
						"error_message": "Divs are empty"}
		else:
			logger.warning(f"{movies_html['error_message']}")
			divs = {"ok": False,
					"error_message": "Divs don't get because html is empty "}
		return divs
		

	"""
	get cinema from one div with info. return one cinema 
	"""
	def get_cinemas_info(self, div):
		if div:
			cinemas_tag = div.find_all("a", class_="header__link", title=True)
			for cinema in cinemas_tag:
				if cinema.string:
					logger.info(f"Cinema is parsed")
				return cinema.string
		
		else:
			logger.warning("Cinema is not founded. Div is empty")

	"""
	get all films from one div with  info
	"""
	def get_films_info(self, div):
		if div:
			films_tag = div.find_all('span', itemprop="name")
			films = {"ok":True,
					"films":[]}
			for film in films_tag:
				if film.string:
					films["films"].append(film.string)
			logger.info("Films was parsed")
			if films["films"]:
				logger.info("Films get success")
			else:
				logger.info("Films are not founded")
				films = {"ok":False,
						"error_message":"Films was not founded"}
		else:
			films = {"ok":False,
					"error_message": "Films are not founded - div is empty"}

		return films


	"""
	get all times for one films. return list with times
	"""
	def get_time_film(self, film):
		times = []

		times_tag = film.parent.parent.parent.find_all('time')# warning
		for time in times_tag:
			if time:
				times.append(time["datetime"][11:16])
		logger.info(f"Times is parsed")
		return times
		


	"""
	get all movies info and transform it to dict
	"""
	def get_movies_info_minsk(self):
		movies_html = self.get_movies_html()
		if movies_html:
			movies_info={"ok": True}
			divs = self.get_comun_divs(movies_html)
			if divs["ok"]:
				for div in divs["divs"]:
					cinema = self.get_cinemas_info(div)
					if cinema:
						movies_info[str(cinema)]={}
						films = self.get_films_info(div)
						if films["ok"]:
							for film in films["films"]:
								movies_info[str(cinema)][str(film)] = {}
								times = self.get_time_film(film)
								movies_info[str(cinema)][str(film)]["time"] = times
						else:
							logger.warning(f"{films['error_message']}")
					else:
						pass
			else:
				logger.warning(f"Movies info did not get.{divs['error_message']}")
				movies_info = {"ok": False,
								"error_message": f"Movies info did not get.{divs['error_message']}"}
		else:
			logger.warning(f"Movies info did not get. {movies_html['error_message']}")
			movies_info = {"ok": False,
							"error_message":f"Movies info did not get. {movies_html['error_message']}"}
		return movies_info





"""
	
parser = ParserTut()
movies_html = parser.get_all_info_movies()

movies = parser.get_movies_info(movies_html)
print(movies)

div = parser.get_comun_divs(movies_html)
films = parser.get_films_info(div)
for film in films:
	print(film.parent)
	times = parser.get_time_film(film)
print(times)
#cinemas = parser.get_movies_info(div)
#links=parser.get_links_info(movies_html)
"""