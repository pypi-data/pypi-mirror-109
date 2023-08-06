import json
import os.path

from py_telegram_bot_api_framework.AStorage import AStorage


class SimpleFileStorage(AStorage):
	def __init__(self, path: str):
		self.__path: str = path
		self.__data: dict = {}
		self.__load()

	def __load(self):
		file_exists = os.path.isfile(self.__path)
		if not file_exists:
			self.__data = {"version": 1}
			self.__save()

		with open(self.__path, mode="r") as json_data_file:
			self.__data = json.load(json_data_file)

	def __save(self):
		with open(self.__path, mode="w") as json_data_file:
			json_data_file.write(json.dumps(self.__data))

	def set(self, uid: [str, int], state: [dict, list, str, int, float, bool]):
		self.__data[uid] = state
		self.__save()

	def get(self, tid, default=None) -> [dict, list, str, int, float, bool]:
		return self.__data.get(tid, default)
