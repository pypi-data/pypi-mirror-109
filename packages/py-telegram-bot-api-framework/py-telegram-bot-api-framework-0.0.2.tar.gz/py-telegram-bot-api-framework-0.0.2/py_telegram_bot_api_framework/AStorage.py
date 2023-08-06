class AStorage:

	def set(self, uid: [str, int], state: [dict, list, str, int, float, bool]):
		raise NotImplementedError("method set must be implemented")

	def get(self, tid, default=None) -> [dict, list, str, int, float, bool]:
		raise NotImplementedError("")
