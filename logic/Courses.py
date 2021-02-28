import requests
import settings
import datetime

class Courses():
	rb_bank_root_url=settings.rb_bank_root_url


	"""
	get rates on date(default today)  for all currenсies
	return list with data dictionaries. Date format - "yyyy-mm-dd"
	"""
	def get_currenсies_on_date(self, date=datetime.date.today()):
		url=f"{self.rb_bank_root_url}?ondate={date}&periodicity=0"
		try:
			response=requests.get(url)
			currencies_on_date=response.json()
			return currencies_on_date
		except Exception as ex:
			raise Exception(f"Error. {response}. Exception - {ex}")


	"""
	get rates all currencies on date(date format - "yyyy-mm-dd") and select needed by money abbreviation
	return dict with single currenсy data.
	"""
	def currencies_on_date_by_abbr(self, money_abbr="", date=datetime.date.today()):
		money_abbr=money_abbr.upper()
		currencies_on_date=self.get_currenсies_on_date(date=date)

		for curr in currencies_on_date:
			if curr["Cur_Abbreviation"]==money_abbr:
				return curr


	"""
	get cur ID of currency by money abbreviation.
	"""
	def get_cur_id_by_abbr(self, money_abbr=""):
		curr=self.currencies_on_date_by_abbr(money_abbr=money_abbr)
		return curr["Cur_ID"]


	"""
	get dynamics rate of currency for period(from today) by money abbreviation 
	"""
	def get_dynamic_rate_by_perid_money_abbr(self, money_abbr="", period=3):
		cur_id=get_cur_id_by_abbr(money_abbr=money_abbr)

		


		


courses=Courses()
print(courses.get_cur_id_by_abbr("USD"))


