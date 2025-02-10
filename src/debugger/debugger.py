import time
from uuid import uuid4

from code_checking.commands import Compiler

class Debugger:
	'''
	Class for managing debug process.
	Either gdb or lldb should be used.
	'''

	def __init__(self, compiler: Compiler, debug_dir: str) -> None:
		print("Debugger is being initialized")
		self.compiler = compiler
		self.debug_dir = debug_dir

		self.last_ping_time: int = time.time() # time in seconds from the last time client pinged this class

	def ping(self) -> None:
		'''
		Updates last time, the class was pinged.
		'''
		self.last_ping_time = time.time()

	def run(self, code_file: str) -> None:
		'''
		Runs debug (gdb/lldb) process.
		:param code_file: Path to the source code file that will be debugged
		'''
		pass

	def stop(self) -> None:
		'''
		Stops debug (gdb/lldb) process and deinitalizes the class.
		'''
		pass
