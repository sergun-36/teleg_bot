
user = {"email": "email_user",
		"password": 12345,
		"post": 4646,
		"users0": "they"}


class DbCRUD:

	def __init__(self, table_name):
		self.table_name = table_name


	def create(self, income_dict):
		if isinstance(income_dict, dict) and income_dict:
			columns = tuple(income_dict.keys())
			values = tuple(income_dict.values())
			f"INSERT INTO {self.table_name} {columns} VALUES {values}"
		else:
			print("You pass wrong data")



	def read(self):
		pass



	def delete(self):
		pass



	def update(self):
		pass

