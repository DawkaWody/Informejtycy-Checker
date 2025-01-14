from server.server import Server
from server.logger import Logger
from server.client import Client
from code_checking.pack_loader import PackLoader
from code_checking.checker import Checker
from code_checking.commands import Compiler
from threading import Thread

def received_file(filename: str, client: Client) -> None:
	global checker
	checker.push_check(filename, client, int(filename.split('_')[0]), print_stats)

def print_stats(result, client: Client, problem_id: int):
	global logger, server
	
	if result["invalid_problem_id"]:
		logger.error(f"Invalid problem id {problem_id}")
		server.send_response_400(client.SOCKET, f"Problem {problem_id} doesn't exist.", "Compilation error: false\nResult percent: 0\n")
		return
	
	if result["compilation_error"]:
		logger.error("Compilation error")
		server.send_response_400(client.SOCKET, f"Compilation error occurred.", "Compilation error: true\nResult percent: 0\n")
		return

	if result["time_limit_exceeded"]:
		logger.info("Time limit exceeded")
		server.send_response_400(client.SOCKET, "Time limit exceeded.", "Compilation error: false\nResult percent: 0\n")
	
	logger.info(f"Accuracy: {result["%"]}%")
	server.send_response_202(client.SOCKET, problem_id, f"Successfully received '{problem_id}'.", f"Compilation error: false\nResult percent: {result["%"]}\n")

if __name__ == "__main__":
	logger = Logger()
	
	pl = PackLoader('../tests', '.test', 'in', 'out', 'CONFIG')
	compiler = Compiler('g++', '../received', '../received/compiled', logger)
	checker = Checker(compiler, pl)

	lt = Thread(target=checker.listen)
	lt.start()

	server = Server(received_file, pl.get_pack_count(), logger)
	server.run()
