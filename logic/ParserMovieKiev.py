import requests
from bs4 import BeautifulSoup

import settings
#from . import settings

logger = settings.logger


class ParserMovieKiev():
	movie_url = settings.KIEV_MOVIES_URL

	"""
	get movie html from link 
	"""
	def get_movies_html(self):
		try:
			res = requests.get(self.movie_url)
			status_code = res.status_code
			if status_code in settings.OK_CODES:
				movie_html_text = res.text
				movie_html = {"ok": True,
							"html": movie_html_text}
				logger.info(f"Movie html is recieved. Status {status_code}")
			else:
				logger.warning(f"Movie html didn't recieved. Status is {status_code}")
				movie_html = {"ok": False,
							"error_message": f"Movie html didn't recieved. Status is {status_code}"}

			return movie_html

		except Exception as ex:
			logger.error(f"Request movie is failed. Error - {ex}")
			raise Exception(f"Request movie is failed. Error - {ex}")


	"""
	get divs with movie info
	"""
	def get_divs(self, movie_html):
		if movie_html["ok"]:
			soup = BeautifulSoup(movie_html["html"], "lxml")
			all_divs = soup.find_all('div', class_= "movie__details")
			if all_divs:
				divs = {"ok": True,
						"divs": all_divs}
				logger.info("Divs is recieved successfull")
			else:
				divs = {"ok": False,
						"error_message": "Divs is an empty"}
				logger.warning("Divs is an empty")

		else:
			logger.warning(f"Divs is not gotten. There is no html")
			divs = {"ok":False,
					"error_message": f"Divs is not gotten. There is no html"}
		return divs


	def get_cinemas(self, div):
		if div:
			all_cinemas_tag = div.find_all("tr", class_="cinema-name")
			if all_cinemas_tag:
				cinemas = []
				for cinema_tag in all_cinemas_tag:
					cinemas.append(cinema_tag.td.span.a.string)
				return cinemas
		else:
			logger.warning(f"div is empty")


	def get_times(self, cinema):
		parent_elem = cinema.parent.parent.parent.parent.parent
		divs_wrap = parent_elem.find_all("div", class_="timewrap")
		times = []
		for div_wrap in divs_wrap:
			if div_wrap:
				times.append(str(div_wrap.string))
		return times

	def get_film(self, div):
		if div:
			film = div.find("a", class_="movie__title")
			print(film)
			film = film.next_element
			return film


	def get_movie_info(self):
		movies_html = self.get_movies_html()
		if movies_html["ok"]:
			divs = self.get_divs(movies_html)
			if divs["ok"]:
				cinema_name = {}
				for div in divs["divs"]:
					cinemas_tag = self.get_cinemas(div)
					if cinemas_tag:
						for cinema in cinemas_tag:
							if cinema:
								if not str(cinema) in cinema_name:
									cinema_name[str(cinema)] = {}
									
								times = self.get_times(cinema)
								film = self.get_film(div)
								cinema_name[str(cinema)][str(film)] = times

								
				return cinema_name



			else:
				logger.warning(f"Movie info is not got. {divs['error_message']}")
				movie_info = {"ok": False,
							"error_message": f"Movie info empty. {divs['error_message']}"}

		else:
			logger.warning(f"Movie info is not got. {movie_html['error_message']}")
			movie_info = {"ok": False,
							"error_message": f"Movie info empty. {movie_html['error_message']}"}	
	
		return movies_info

parser = ParserMovieKiev()
movie_info = parser.get_movie_info()
print(movie_info)
