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
	def get_movie_html(self):
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
			lis = soup.find_all('li', class_= "movie__block")
			print(len(lis))
			for li in lis:
				if li:
					cinema = li.find_all('td', class_="cinema")
					for ci in cinema:
						if ci:
							#ci = cinema.string
							return ci.span.a.string#.prettify()

		else:
			logger.warning(f"Divs is not gotten. There is no html")
			lis = {"ok":False,
					"error_message": f"Divs is not gotten. There is no html"}

parser = ParserMovieKiev()
html = parser.get_movie_html()
li = parser.get_divs(html)
print(li)
