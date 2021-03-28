from . import settings
#import settings
#import settingsTut

logger=settings.logger

class PreparerText():

	"""
	prepare text message for rates of currency on date.It extracts data from dict currency_on_date_by_abbr 
	"""
	def do_courses_on_date_text(self, currs_on_date_by_abbr={"ok": False, "error_message": None}):
		if currs_on_date_by_abbr["ok"]:
			scale=currs_on_date_by_abbr["curr"]["Cur_Scale"]
			rate=currs_on_date_by_abbr["curr"]["Cur_OfficialRate"]
			date=currs_on_date_by_abbr["curr"]["Date"][0:10]
			curr_abbr=currs_on_date_by_abbr["curr"]["Cur_Abbreviation"]
			text=f"{scale} {curr_abbr} costs {rate} BYN on {date}"
			logger.info(f"Text {curr_abbr} on {date} is prepared")
		else:
			logger.warning(f"Text   is not prepared. There is no data of currs")
			text=currs_on_date_by_abbr["error_message"]
		return text


	"""
	prepare text message. format {date} {rate}. date extract dict
	"""			
	def do_courses_dynamics_text(self, curr_dynamic_data={"ok": False, "error_message": None}):
		if curr_dynamic_data["ok"]:
			scale= curr_dynamic_data["scale"]
			curr_abbr= curr_dynamic_data["curr_abbr"]
			text=f"Dynamic {scale} {curr_abbr} in BYN:"
			for curr in curr_dynamic_data["curr_dynamic"]:
				date=curr["Date"][0:10]
				rate=curr["Cur_OfficialRate"]
				text+=f"\n{date} : {rate}"
			logger.info(f"Dynamic {curr_abbr} text is prepared")

		else:
			logger.warning(f"Dynamic text is not prepared.Error - {curr_dynamic_data['error_message']}")
			text=curr_dynamic_data['error_message']

		return text
		
	"""
	prepare text format date: change from now_day to prev_day
	"""
	def do_courses_changes_text(self, curr_dynamic_data={"ok": False, "error_message": None}):
		if curr_dynamic_data["ok"]:
			scale= curr_dynamic_data["scale"]
			curr_abbr= curr_dynamic_data["curr_abbr"]
			text=f"Changes {scale} {curr_abbr} in BYN:"
			currs=curr_dynamic_data["curr_dynamic"]
			for i in range(len(currs)-1, 0, -1):
				date=currs[i]["Date"][0:10]
				change=round(currs[i]["Cur_OfficialRate"]-currs[i-1]["Cur_OfficialRate"], 4)
				text+=f"\n{date} : {change}"
			logger.info(f"Changes {curr_abbr} text is prepared")
		else:
			logger.warning(f"Changes text is prepared.{curr_dynamic_data['error_message']}")
			text=curr_dynamic_data['error_message']

		return text


	"""
	Prepare movies text from dict with cinemas and films. It returns str
	"""
	def do_movies_text(self, movies_info=""):
		if movies_info["ok"]:
			text = "List of cinemas:"
			for cinema in movies:
				text += f"\n{cinema}"
				
				for film in movies[cinema]:
					text +=f"\n 	{film}: "
					for time in movies[cinema][film]["time"]:
						text += f"({time}), "
			text +="."
			logger.info("Movies text is prepared")

		else:
			logger.warning(f"There are no movies.{movies_info['error_message']}")
			text = f"{movies_info['error_message']}"
		return text	





"""
preparator=PreparerText()
text=preparator.do_movies_text(settingsTut.movies)
print(text)
"""