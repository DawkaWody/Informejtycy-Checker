from server.server import Server
from server.logger import Logger
from code_checking.pack_loader import PackLoader
from code_checking.checker import Checker
from code_checking.commands import Compiler
from threading import Thread

def received_file(filename: str) -> None:
	global checker
	checker.push_check(filename, int(filename.split('_')[0]), print_stats)

def print_stats(result):
	global logger
	logger.info(f"Accuracy: {result["%"]}%")

if __name__ == "__main__":
	logger = Logger()
	
	pl = PackLoader('../tests', '.test', 'in', 'out')
	compiler = Compiler('g++', '../received', '../received/compiled', logger)
	checker = Checker(compiler, pl)

	lt = Thread(target=checker.listen)
	lt.start()

	server = Server(received_file, pl.get_problem_count(), logger)
	server.run()
	
