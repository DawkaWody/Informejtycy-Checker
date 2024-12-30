class Logger:
	color_NORMAL = "\033[0m"         # For setting color back to normal
	color_INFO = "\033[38:5:27m"     # For reporting about server activites
	color_ERROR = "\033[38:5:160m"   # For any problems, in which server doesn't continue file submission
	color_WARNING = "\033[38:5:99m"  # For file submission problems, in which server continues file submission
	color_ALERT = "\033[38:5:214m"   # For server problems, in which server continues file submission
	
	def log(self, message: str) -> None:
		print(f"{self.color_INFO}INFO:{self.color_NORMAL} {message}")
	
	def error(self, message: str) -> None:
		print(f"{self.color_ERROR}ERROR:{self.color_NORMAL} {message}")
	
	def warn(self, message: str) -> None:
		print(f"{self.color_WARNING}WARNING:{self.color_NORMAL} {message}")
	
	def alert(self, message: str) -> None:
		print(f"{self.color_ALERT}ALERT:{self.color_NORMAL} {message}")