import datetime
import settings

logger=settings.logger

class TextAnalyzer():

	
	"""
	Set data for class where keys - attribut and value - value of attribut
	"""
	def set_data(self, **kwargs):
		for key, value in kwargs.items():
			print(key, value)
			setattr(self, key,  value)

	"""
	Search key words "сегодня" and "сейчас".Return date today
	Or return date after key word "на"
	"""		

	def get_date_from_text(self, text):
		text=text.lower()
		if text.find("сегодн") > -1 or text.find("сейчас") > -1:
			date = datetime.date.today()
			logger.info(f"Date {date} is recieved")
			return date
			
		if text.find("на") > -1:
			words = text.split(" ")
			index_date = words.index("на")+1
			date = words[index_date]
			logger.info(f"Date {date} is recieved")
			return date

		logger.warning("Date is not recieved")


	"""
	get currency abbreviation after key word "курс"
	"""	
	def get_curr_from_text(self, text):
		text = text.lower()
		if "курс " in text:
			words = text.split(" ")
			index_curr = words.index("курс")+1
			curr = words[index_curr].upper()
			logger.info(f"Currency {curr} is recieved")
			return curr

		logger.warning("Currency is not recieved")


	"""
	get type user message and set type in attribute of class
	"""
	def get_type_user_message(self, text):
		text = text.lower()
		if "курс" in text:
			type = "rate"
		else:
			type = "echo"
		logger.info(f"Type of user message - {type}")
		set_data(type=type)


	"""
	prepare answer message for user. It depends from self.type
	"""
	def prepare_anwer(self, text):
		if self.type == "rate":
			if self.curr:
				if self.date:

				else:
					logger.info("Message anser - Date in not founded")
					return "Enter please Date after keyword \"на\" in format YYYY-MM-DD"
			else:
				logger.info("Message anser - Currency in not founded")
				return "Enter please currency abbreviation after keyword \"курс\""		

text = TextAnalyzer()
words = text.get_curr_from_text("курсы usd на 2020-12-21")
print(words)