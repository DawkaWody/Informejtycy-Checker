import os
import time
from pygdbmi.gdbcontroller import GdbController
from uuid import uuid4
from pprint import pprint

from code_checking.commands import Compiler

# type: result -> can be skipped
# type: log -> command, which was given
# type: console -> gdb output for command
# type: notify -> extra gdb output for command

class GDBDebugger:
	'''
	Class for managing debug process (gdb).
	'''

	def __init__(self, compiler: Compiler, debug_dir: str, file_name: str) -> None:
		self.compiler = compiler
		self.received_dir = self.compiler.input_dir
		self.debug_dir = debug_dir
		self.file_name = file_name

		self.last_ping_time: int = time.time() # time in seconds from the last time client pinged this class

		self.gdb_init_input = [
			"set debuginfod enabled off",
			"python",
			"import sys",
			"sys.path.insert(0, '/usr/share/gcc/python/')",
			"from libstcxx.v6.printers import register_libstdcxx_printers",
			"register_libstdcxx_printers(None)",
			"end",
			"break main",
			"run"
		]

		self.compiled_file_name = ""
		self.process: GdbController | None = None

		#
		# Currently, for purpose of testing, debugger is being runned without docker container.
		# In the future, it should be changed, so that program can be debugged safely.
		#
		# self.docker_manager = DockerManager(self.compiler.output_dir, debug_dir)
		# self.memory_limit_MB = 60
		#

	def ping(self) -> None:
		'''
		Updates last time, the class was pinged.
		'''
		self.last_ping_time = time.time()

	def pprint_response(self, response: dict) -> None:
		pprint(response)

	def run(self) -> int:
		'''
		Runs debug process (gdb).
		:param file_name: Path to the source code file that will be debugged
		'''
		output_file_name = self.compiler.compile(self.file_name, debug=True)

		if not os.path.exists(os.path.join(self.debug_dir, output_file_name)):
			return -1

		self.compiled_file_name = output_file_name
		self.process = GdbController()

		response = self.process.write(f"file {os.path.join(self.debug_dir, output_file_name)}")
		response = self.process.write(f"set debuginfod enabled off")
		self.pprint_response(response)
		response = self.process.write(f"break main")
		self.pprint_response(response)

		self.process.exit()
		self.process = None

		return 0

	def stop(self) -> None:
		'''
		Stops debug process (gdb) and deinitalizes the class.
		'''
		if self.compiled_file_name:
			os.remove(os.path.join(self.debug_dir, self.compiled_file_name))
		os.remove(os.path.join(self.received_dir, self.file_name))
