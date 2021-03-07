import settings

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

		

currs={'ok': True, 'curr': {'Cur_ID': 145, 'Date': '2021-03-07T00:00:00', 'Cur_Abbreviation': 'USD', 'Cur_Scale': 1, 'Cur_Name': '▒▒▒▒▒▒ ▒▒▒', 'Cur_OfficialRate': 2.6105}}
curres={'ok': False, 'error_message': "no curr data" }
preparator=PreparerText()
text=preparator.do_courses_on_date_text(curres)
print(text)