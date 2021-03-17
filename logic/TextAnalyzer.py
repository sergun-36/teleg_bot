import datetime

class TextAnalyzer():

	def set_data(self, **kwargs):
		for key, value in kwargs.items():
			print(key, value)
			setattr(self, key,  value)

	def get_date_from_text(self, text):
		text=text.lower()
		if text.find("сегодн") > -1 or text.find("сейчас") > -1:
			date = datetime.date.today()
			return date
			
		if text.find("на") > -1:
			words = text.split(" ")
			index_date = words.index("на")+1
			date = words[index_date]
			return date



text = TextAnalyzer()
words = text.get_date_from_text("курс usd на 2020-02-21")
print(words)