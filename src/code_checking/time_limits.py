import time

class TimeLimitExceeded(Exception):
	pass


class WallClock:
	def __init__(self, limit: float):
		self.limit = limit
		self.is_stopped = False

	def start(self, limit: float):
		start_time = time.time()
		current_time = start_time
		while current_time - start_time < limit:
			current_time = time.time()
			if self.is_stopped:
				break
		else:
			raise TimeLimitExceeded()

	def stop(self):
		self.is_stopped = True
