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


	def get_comun_divs(self, movies_html):
		soup_html = BeautifulSoup(movies_html, "lxml")
		divs = soup_html.find_all("div", class_="a-event-i")
		logger.info(f"Printim links")
		for div in divs:
			#print(div)
			return div
			pass
		return divs
		


	def get_cinemas_info(self, div):
		cinemas_tag = div.find_all("a", class_="header__link", title= True)
		for cinema in cinemas_tag:
			if cinema.string:
				print(cinema.string)
				return cinema.string
		logger.info(f"Printim links")


	def get_films_info(self, div):
		films_tag = div.find_all('span', itemprop="name")
		films = []
		for film in films_tag:
			if film.string:
				films.append(film.string)
				#print(film.string)
		return films

	def get_time_film(self, film):
		times = []

		times_tag = film.parent.parent.parent.find_all('time')
		for time in times_tag:
			print(time["datetime"])
			times.append(time["datetime"])

		return times
		logger.info(f"Printim time")


	def get_movies_info(self, movies_html):
		movies={}
		div = self.get_comun_divs(movies_html)
		#loop for div in divs
		cinema = self.get_cinemas_info(div)
		movies[str(cinema)]={}
		films = self.get_films_info(div)
		for film in films:
			times = self.get_time_film(film)
			movies[str(cinema)][str(film)]= times
		return movies







	
parser = ParserTut()
movies_html = parser.get_all_info_movies()

movies = parser.get_movies_info(movies_html)
print(movies)
'''
div = parser.get_comun_divs(movies_html)
films = parser.get_films_info(div)
for film in films:
	print(film.parent)
	times = parser.get_time_film(film)
print(times)
#cinemas = parser.get_movies_info(div)
#links=parser.get_links_info(movies_html)
'''