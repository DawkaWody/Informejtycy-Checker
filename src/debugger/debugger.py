import time
from uuid import uuid4

from code_checking.commands import Compiler

class Debugger:
	'''
	Class for managing debug process.
	Either gdb or lldb should be used.
	'''

	def __init__(self, compiler: Compiler, debug_dir: str) -> None:
		self.compiler = compiler
		self.debug_dir = debug_dir

		self.last_ping_time: int = time.time() # time in seconds from the last time client pinged this class

		self.gdb_init_input = [
			"python",
			"import sys",
			"sys.path.insert(0, '/usr/share/gcc/python/')",
			"from libstcxx.v6.printers import register_libstdcxx_printers",
			"register_libstdcxx_printers(None)",
			"end",
			"set debuginfod enabled off",
			"break main",
			"run"
		]

		self.docker_manager = DockerManager(self.compiler.output_dir, debug_dir)
		self.memory_limit_MB = 60

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
