import settings
from Courses import Courses


logger=settings.logger

class PreparerText():

	"""
	prepare text message for rates of currency on date.It extracts data from dict currency_on_date_by_abbr 
	"""
	def do_courses_on_date_text(self, currs_on_date_by_abbr):
		if currs_on_date_by_abbr["ok"]:
			scale=currs_on_date_by_abbr["curr"]["Cur_Scale"]
			rate=currs_on_date_by_abbr["curr"]["Cur_OfficialRate"]
			date=currs_on_date_by_abbr["curr"]["Date"][0:10]
			curr_abbr=currs_on_date_by_abbr["curr"]["Cur_Abbreviation"]
			text=f"{scale} {curr_abbr} costs {rate} BYN"
			logger.info(f"Text {curr_abbr} on {date} is prepared")
		else:
			logger.warning(f"Text   is not prepared. There is no data of currs")
			text=currs_on_date_by_abbr["error_message"]
		return text


	"""
	prepare text message. format {date} {rate}. date extract dict
	"""			
	def do_courses_dynamics_text(self, curr_dynamic_data):
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
	def do_courses_changes_text(self, curr_dynamic_data):
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


currs={'ok': True, 'curr_abbr': 'USD', 'scale': 1, 'curr_dynamic': [{'Cur_ID': 145, 'Date': '2021-03-04T00:00:00', 'Cur_OfficialRate': 2.6073}, {'Cur_ID': 145, 'Date': '2021-03-05T00:00:00', 'Cur_OfficialRate': 2.608}, {'Cur_ID': 145, 'Date': '2021-03-06T00:00:00', 'Cur_OfficialRate': 2.6105}, {'Cur_ID': 145, 'Date': '2021-03-07T00:00:00', 'Cur_OfficialRate': 2.6105}]}

courses=Courses()
currs=courses.get_dynamic_rate_by_perid_money_abbr("USD")

preparator=PreparerText()
text=preparator.do_courses_changes_text(currs)
print(text)