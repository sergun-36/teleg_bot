import requests
from bs4 import BeautifulSoup

#import settings
from . import settings

logger = settings.logger


class ParserMovieKiev():
	movie_url = settings.KIEV_MOVIES_URL

	"""
	get movie html from link 
	"""
	def get_movies_html_kiev(self):
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
	def get_divs_kiev(self, movie_html):
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

	"""
	get cinemas tags from one div with info
	"""
	def get_cinemas_kiev(self, div):
		all_cinemas_tag = div.find_all("tr", class_="cinema-name")
		cinemas = []
		if all_cinemas_tag:
			for cinema_tag in all_cinemas_tag:
				cinemas.append(cinema_tag.td.span.a.string)
			logger.info("Cinemas tags is recieved")
		else:
			logger.warning("Cinemas tags is empty")

		return cinemas


	"""
	get all session times for each cinema. return list with string
	"""
	def get_times_kiev(self, cinema):
		parent_elem = cinema.parent.parent.parent.parent.parent
		divs_wrap = parent_elem.find_all("div", class_="timewrap")
		times = []
		for div_wrap in divs_wrap:
			if div_wrap:
				times.append(str(div_wrap.string))
		return times


	"""
	get name film from div with info. Return string with film name
	"""
	def get_film_kiev(self, div):
		film = div.find("a", class_="movie__title")
		film = str(film.next_element)
		return film



	def get_movies_info_kiev(self):
		movies_html = self.get_movies_html_kiev()
		divs = self.get_divs_kiev(movies_html)
		if divs["ok"]:
			movies_info = {"ok": True}
			for div in divs["divs"]:
				cinemas_tag = self.get_cinemas_kiev(div)
				if cinemas_tag:
					for cinema in cinemas_tag:
						if cinema:
							if not str(cinema) in movies_info:
								movies_info[str(cinema)] = {}
							times = self.get_times_kiev(cinema)
							film = self.get_film_kiev(div)
							movies_info[str(cinema)][film] = {}
							movies_info[str(cinema)][film]["time"] = times
							
		else:
			logger.warning(f"Movie info is not got. {divs['error_message']}")
			movies_info = {"ok": False,
						"error_message": f"Movie info empty. {divs['error_message']}"}


	
		return movies_info





"""
parser = ParserMovieKiev()
movie_info = parser.get_movies_info_kiev()
print(movie_info)
"""