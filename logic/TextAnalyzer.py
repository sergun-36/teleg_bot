

import datetime
from . import settings
from .PreparerText import PreparerText
from .Courses import Courses
from .ParserTut import ParserTut
"""
import settings
from PreparerText import PreparerText
from Courses import Courses
from ParserTut import ParserTut
"""


logger=settings.logger

class TextAnalyzer(PreparerText, Courses, ParserTut):

	
	"""
	Set data for class where keys - attribut and value - value of attribut
	"""
	def set_data(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key,  value)
			logger.info(f"{key} = {value}. Attribut added")

	"""
	Search key words "сегодня" and "сейчас".Return date today
	Or return date after key word "на"
	"""		

	def get_date_from_text(self, text):
		text=text.lower()
		if text.find("сегодн") > -1 or text.find("сейчас") > -1:
			date = datetime.date.today()
			logger.info(f"Date {date} is recieved")
			self.set_data(date=date)
			return date
			
		if text.find("на") > -1:
			words = text.split(" ")
			index_date = words.index("на")+1
			date = words[index_date]
			logger.info(f"Date {date} is recieved")
			self.set_data(date=date)
			return date

		self.set_data(date=None)
		logger.warning("Date is not recieved")


	"""
	get currency abbreviation after key word "курс"
	"""	
	def get_curr_from_text(self, text):
		text = text.lower()
		if self.type == "rate_dynamic":
			check_str = "курса"
		if self.type == "rate_on_date":
			check_str = "курс"

		if check_str in text:
			words = text.split(" ")
			index_curr = words.index(check_str)+1
			if index_curr < len(words):
				curr = words[index_curr].upper()
				logger.info(f"Currency {curr} is recieved")
				self.set_data(curr=curr)
				return curr
		self.set_data(curr=None)
		logger.warning("Currency is not recieved")


	"""
	get type user message and set type in attribute of class
	"""
	def get_type_user_message(self, text):
		text = text.lower()
		if "курс" in text:
			if "динамик" in text:
				type = "rate_dynamic"
			else:
				type = "rate_on_date"
		elif "кино" in text:
			type = "movies"
		else:
			type = "echo"
		logger.info(f"Type of user message - {type}")
		self.set_data(type=type)


	"""
	get period from text for type dinamic.Return  period in integer
	"""
	def get_period_from_text(self, text):
		text = text.lower()
		words = text.split(" ")
		for word in words:
			if word.isdigit():
				period = int(word)
				logger.info(f"Period of dynamic is {period}")
				break
		else:
			logger.warning(f"Period of dynamic is not founded")
			period = None

		self.set_data(period=period)

	"""
	prepare answer message for user and cut it, if it is too large
	"""
	def prepare_anwer(self, text):
		if self.type == "rate_on_date":
			if self.curr:
				if self.date:
					currs_on_date_by_abbr = self.get_currencies_on_date_by_abbr(money_abbr=self.curr, date=self.date)
					answer_text = self.do_courses_on_date_text(currs_on_date_by_abbr=currs_on_date_by_abbr)
					logger.info("Message on date is ok")
				else:
					logger.info("Message anser - Date in not founded")
					answer_text = "Enter please Date after keyword \"на\" in format YYYY-MM-DD"
			else:
				logger.info("Message anwser - Currency in not founded")
				answer_text = "Enter please currency abbreviation after keyword \"курс\""

		if self.type == "rate_dynamic":
			if self.curr:
				if self.period:
					curr_dynamic_data = self.get_dynamic_rate_by_periоd_money_abbr(period=self.period, money_abbr=self.curr)
					answer_text = self.do_courses_dynamics_text(curr_dynamic_data=curr_dynamic_data)
				else:
					logger.info("Message answer - period in not founded ")
					answer_text= " Enter please period as ceil number"
			else:
				logger.info("Message anwser - Currency in not founded")
				answer_text = "Enter please currency abbreviation after keyword \"курс\""

		if self.type == "movies":
			movies = self.get_movies_info()
			answer_text = self.do_movies_text(movies)
			print(len(answer_text))
			logger.info("Message answer movies is successfull")

		if  self.type == "echo":
			logger.info("Message answer - echo(repeat)")
			answer_text = text

		if len(answer_text) > settings.MAX_LIMIT_TEXT:
			answer_text = answer_text[0:settings.MAX_LIMIT_TEXT]
			logger.warning("Message is too large and was cut")
		return answer_text


	def do_analys_text(self, text):
		self.get_type_user_message(text)
		if self.type == "rate_on_date":
			self.get_date_from_text(text)
			self.get_curr_from_text(text)
		if self.type == "rate_dynamic":
			self.get_curr_from_text(text)
			self.get_period_from_text(text)
		text = self.prepare_anwer(text)
		return text

"""
text = TextAnalyzer()
words = text.do_analys_text("кино")
print(words)
"""