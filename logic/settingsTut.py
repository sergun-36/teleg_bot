movies = {"World" : 
				{"Cobra": {"time":["9:00", "10:00"],
							"description": None},
				"Cobra 2": {"time":["11:00", "19:00"],
							"description": None}},
			"Hell" : {"Rembo": {"time":["14:00", "20:00"],
									"description": None},
						"Rembo 1": {"time":["11:00", "21:00"],
									"description": None},
						"Rembo 2": {"time":["12:00", "22:00"],
									"description": None}}}


"""
{"World" : 
				{"Cobra": {"time":["9:00", "10:00"],
							"description": None},
				"Cobra 2": {"time":["11:00", "19:00"],
							"description": None}
"""
from ParserTut import ParserTut 
import bs4
import requests

html = requests.get("https://afisha.tut.by/film/").text




def get_seanses_in_cinemas_today(seanses_raw_html):
	movie_info = {}
	for cinema in seanses_raw_html:
		cinema_name =cinema.find("div", {"class":"item-header-i"}).a.get_text()
		seanses = cinema.find("ul", {"class":"b-shedule__list js-shedule-list"})
		times = [time.get_text()[0:5] for time in seanses.find_all("a")]
		movie_info[cinema_name] = times

	return movie_info

def get_func(html):
	name_film = html.find("div", {"class":"event-header-i"}).get_text()

	seanses_raw_html = html.find_all("div", {"class":"js-film-list__li"})
	seanses =get_seanses_in_cinemas_today(seanses_raw_html)
	film_info = {name_film: seanses}
	return film_info


movies_raw_list = bs4.BeautifulSoup(html, 'html.parser').find_all("div", {"class":"a-event-i"})
for x in movies_raw_list:
	print(get_func(x))


