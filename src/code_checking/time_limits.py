import time

class TimeLimitExceeded(Exception):
	pass


class WallClock:
	def __init__(self, limit: float):
		self.limit = limit
		self._stop = False

	def start(self, limit: float):
		start_time = time.time()
		current_time = start_time
		while current_time - start_time < limit:
			current_time = time.time()
			if self._stop:
				break
		else:
			raise TimeLimitExceeded()

	def stop(self):
		self._stop = True
