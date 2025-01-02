import threading
import time
from . import REQUEST_LIMIT, REQUEST_TIME_PERIOD_SECONDS


class Logger:
	color_NORMAL = "\033[0m"         # For setting color back to normal
	color_INFO = "\033[38:5:27m"     # For reporting about server activites
	color_ERROR = "\033[38:5:160m"   # For any problems, in which server doesn't continue file submission
	color_WARNING = "\033[38:5:99m"  # For file submission problems, in which server continues file submission
	color_ALERT = "\033[38:5:214m"   # For server problems, in which server continues file submission
	
	def start_log_cleaner(self) -> None:
		self.request_logs: dict[str: int] = {}   # ip: requests_left
		self.request_log_lock = threading.Lock() # for avoiding conflict usage of request_logs
		
		self.info(f"Request log cleaner is running (MAX {REQUEST_LIMIT} requests/{REQUEST_TIME_PERIOD_SECONDS} seconds)")
		log_cleaning_thread = threading.Thread(target=self.clear_request_logs, daemon=True)
		log_cleaning_thread.start()
	
	def clear_request_logs(self) -> None:
		while True:
			time.sleep(REQUEST_TIME_PERIOD_SECONDS)
			
			with self.request_log_lock:
				self.info("Cleaning request log")
				self.request_logs.clear()
	
	def log_request(self, client_address: tuple[str, int]) -> bool:
		with self.request_log_lock:
			if self.request_logs.get(client_address[0], REQUEST_LIMIT) <= 0:
				return True
			self.request_logs[client_address[0]] = self.request_logs.get(client_address[0], REQUEST_LIMIT)-1
		
		self.info(f"Registered request {client_address[0]}:{client_address[1]}")
		if self.request_logs[client_address[0]] == 0:
			self.warn(f"{client_address[0]}:{client_address[1]} has 0 requests left")
		
		return False
	
	def info(self, message: str) -> None:
		print(f"{self.color_INFO}INFO:{self.color_NORMAL} {message}")
	
	def error(self, message: str) -> None:
		print(f"{self.color_ERROR}ERROR:{self.color_NORMAL} {message}")
	
	def warn(self, message: str) -> None:
		print(f"{self.color_WARNING}WARNING:{self.color_NORMAL} {message}")
	
	def alert(self, message: str) -> None:
		print(f"{self.color_ALERT}ALERT:{self.color_NORMAL} {message}")