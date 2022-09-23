from . import settings
import os


logger = settings.logger

class Vershi():
	vershi = settings.vershi

	def create_message_with_vershi(self):
		scroll_name_versh = ""
		for versh in self.vershi:
			if versh[-5:] == "_love":
				pass
			else:
				scroll_name_versh+=f"\n{versh.capitalize()}"
		return scroll_name_versh

	def get_versh_text(self, name, user_first_name = None):
		if user_first_name == "Valeri Ignis":
			new_name =f"{name}_love"
			if self.vershi.get(new_name):
				name = new_name

		if self.vershi.get(name):
			try:
				with open(os.path.join("logic","vershi", self.vershi[name]), "r") as f:
					answer_text = f.read()
					logger.info(f"Text of \'{name}\' is ready")
			except:
				answer_text = "there is a problem with search file with this poem"
				logger.error(f"problem with openning or serching file {self.vershi[name]}")
		else:
			vershies = self.create_message_with_vershi()
			answer_text = f"\'{name}\' is absent in list of poems. \nEnter please name from list:{vershies}"
			logger.warning(f"\'{name}\' in not found in exists poems")
		return answer_text



