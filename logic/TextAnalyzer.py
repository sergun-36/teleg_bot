import datetime
import settings

logger=settings.logger

class TextAnalyzer():

	
	"""
	Set data for class where keys - attribut and value - value of attribut
	"""
	def set_data(self, **kwargs):
		for key, value in kwargs.items():
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
			curr = words[index_curr].upper()
			logger.info(f"Currency {curr} is recieved")
			self.set_data(curr=curr)
			return curr

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
	prepare answer message for user. 
	"""
	def prepare_anwer(self, text):
		if self.type == "rate_on_date":
			if self.curr:
				if self.date:
					answer_text = "all ak"
					logger.info("Message on date is oks")

				else:
					logger.info("Message anser - Date in not founded")
					answer_text = "Enter please Date after keyword \"на\" in format YYYY-MM-DD"
			else:
				logger.info("Message anser - Currency in not founded")
				answer_text = "Enter please currency abbreviation after keyword \"курс\""
		if self.type == "rate_dynamic":
			if self.curr:
				if self.period:
					answer_text = "динамика"
				else:
					answer_text= " Enter please period as ceil number"

		if  self.type == "echo":
			answer_text = text

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


text = TextAnalyzer()
words = text.do_analys_text("динамика курса usd за ")
print(words)