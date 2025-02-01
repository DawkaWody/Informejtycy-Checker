import json

class CheckResult:	
	
	def __init__(self) -> None:
		self.percentage = 0
		self.first_failed = ""
		self.time_limit_exceeded = False
		self.memory_limit_exceeded = False
		self.compilation_error = False
		self.invalid_problem_id = False
		self.unauthorized = False
	
	def __repr__(self) -> str:
		return json.dumps(self.as_dict(), indent=4)
	
	def as_dict(self) -> dict:
		return {
			"percentage": self.percentage,
			"first_failed": self.first_failed,
			"time_limit_exceeded": self.time_limit_exceeded,
			"memory_limit_exceeded": self.memory_limit_exceeded,
			"compilation_error": self.compilation_error,
			"invalid_problem_id": self.invalid_problem_id,
			"unauthorized": self.unauthorized
		}

class UnauthorizedCheckResult(CheckResult):
	
	def __init__(self) -> None:
		super().__init__()
		self.unauthorized = True