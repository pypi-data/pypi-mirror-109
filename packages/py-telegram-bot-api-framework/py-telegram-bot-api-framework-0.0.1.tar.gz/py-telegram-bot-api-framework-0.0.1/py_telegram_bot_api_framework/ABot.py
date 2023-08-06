import logging
from typing import List

from py_telegram_bot_api_framework.AHandler import AHandler
from telegram_bot_api import API, Pooling, Update


class ABot:
	def __init__(self, token: str, name: str = "DefaultBotName", **kwargs):
		self.name = name
		self.token = token
		self.config: dict = kwargs
		self.api: API = API(token)
		self.handlers: List[AHandler] = []
		self.pooling = None

		self._on_initialise()

	# for overrides
	def _on_initialise(self):
		pass

	def add_handlers(self, *handler_classes: type):
		for h in handler_classes:
			self.add_handler(h)

	def add_handler(self, handler_class: type):
		assert issubclass(handler_class, AHandler), f"Type {handler_class} is not a subclass of AHandler"
		self.handlers.append(handler_class(self.api, self.config))

	def on_update(self, update: Update):
		handled_by = None
		for h in self.handlers:
			if h.handle(update):
				handled_by = h
				break

		if not handled_by:
			logging.debug(f"[ABot][Unhandled update] {update}")

	def start_pooling(self, update_time: int = 5, dev_mode: bool = False):
		self.pooling = Pooling(self.api, self.on_update, update_time, dev_mode=dev_mode)
		self.pooling.start()
