import requests
from . import settings
import datetime

logger=settings.logger


class Courses():
	rb_bank_root_url=settings.RB_BANK_ROOT_URL

	def set_country(self, country=""):
		self.country=country

	"""
	get rates on date(default today)  for all currenсies
	return list with data dictionaries. Date format - "yyyy-mm-dd"
	"""
	def get_currenсies_on_date(self, date=datetime.date.today()):
		url=f"{self.rb_bank_root_url}?ondate={date}&periodicity=0"
		try:
			res=requests.get(url)
			status=res.status_code
			if status in settings.OK_CODES:
				result={"ok" : True,
						"currencies_on_date" : res.json()}
				logger.info(f"Request on date {date} is successfull. Status {status}")
			else:
				result={"ok" : False,
						"error_message" : f"Request on date {date} is failed. Status {status}"}
				logger.warning(f"Request on date {date} is failed. Status {status}")
			return result
		except Exception as ex:
			logger.error(f"Error - {res}. Exception - {ex}")
			raise Exception(f"Error - {res}. Exception - {ex}")


	"""
	get rates all currencies on date(date format - "yyyy-mm-dd") and select needed by money abbreviation
	return dict with single currenсy data.
	"""
	def get_currencies_on_date_by_abbr(self, money_abbr="", date=datetime.date.today()):
		money_abbr=money_abbr.upper()
		currs_on_date=self.get_currenсies_on_date(date=date)
		
		if currs_on_date["ok"]:
			for curr in currs_on_date["currencies_on_date"]:
				if curr["Cur_Abbreviation"]== money_abbr:
					logger.info(f"Data for \'{money_abbr}\' is founded successfull")
					return {"ok" : True,
							"curr" : curr}
				
			logger.warning(f"Such currency as \'{money_abbr}\' in not founded")
			return {"ok" : False,
					"error_message" : f"Such currency as \'{money_abbr}\' in not founded"}
		else:
			logger.warning(currs_on_date["error_message"])
			return  {"ok" : False,
					"error_message" : f"Such currency as \'{money_abbr}\' in not founded"}


	"""
	get dynamics rate of currency for period(from today) by money abbreviation 
	"""
	def get_dynamic_rate_by_periоd_money_abbr(self, money_abbr="", period=3):
		result=self.get_currencies_on_date_by_abbr(money_abbr=money_abbr)
		if result["ok"]:
			cur_id=result["curr"]["Cur_ID"]
			scale=result["curr"]["Cur_Scale"]
			end_date=datetime.date.today()
			start_date=datetime.datetime.now()-datetime.timedelta(days=period)#.date()
			url=f"{self.rb_bank_root_url}/Dynamics/{cur_id}?startDate={start_date}&endDate={end_date}"

			try:
				res=requests.get(url)
				status=res.status_code

				if status in settings.OK_CODES:
					result={"ok" : True,
							"curr_abbr" : money_abbr,
							"scale" : scale,
							"curr_dynamic" : res.json()}
					logger.info(f"Currency dynamic \'{money_abbr}\' for {period} days got successfull. Status {status}")
				else:
					result={"ok" : False,
							"error_message" : f"Currency dynamic did not get. Status {status}"}
					logger.warning(f"Currency dynamic did not get. Status {status}")
				
			except Exception as ex:
				logger.warning(f"Request of currency dynamic was failed. Error {ex}")
				raise Exception(f"Request of currency dynamic was failed. Error {ex}") 

		else:
			logger.warning(f"Cur_ID \'{money_abbr}\' is not founded")
			result={"ok" : False,
					"error_message" : f"Cur_ID \'{money_abbr}\' is not founded"}
		return result

		

