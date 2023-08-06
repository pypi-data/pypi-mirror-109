from typing import Optional

from telegram_bot_api import API, Update


class AHandler:
	def __init__(self, api: API, config: dict):
		self.telegram_api: API = api
		self.config = config

		self._on_initialise()

	def _on_initialise(self):
		pass

	def handle(self, update: Update) -> bool:
		raise NotImplementedError("handle method have to be implemented")
