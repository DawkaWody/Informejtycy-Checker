import socket
import threading
from typing import Callable, Any
from uuid import uuid4

import server.file_manager as file_manager
from server.logger import Logger
from . import IP, PORT, RECEIVED_DIR

class Server:
	def __init__(self, on_received: Callable[[str], Any], ) -> None:
		self.host = IP
		self.port = PORT
		self.server_socket = socket.create_server((self.host, self.port))
		
		self.logger = Logger()

		self.on_received = on_received
		self.received_directory = RECEIVED_DIR
	
	def run(self) -> None:
		self.logger.log(f"Server is running {self.host}:{self.port}")
		while True:
			client_socket, client_address = self.server_socket.accept()
			thread = threading.Thread(target=self.handle_request, args=(client_socket, client_address))
			thread.start()
	
	def handle_request(self, client_socket: socket.socket, client_address: tuple[str, int]) -> None:
		request_line = client_socket.recv(1024).decode()

		if request_line[0:4] != "POST":
			self.logger.error("Invalid request send")
			self.send_response_405(client_socket, "Only POST method available")
			return

		request_content = request_line.split('\r\n')
		file_content = ""

		problem_id = ""
		problem_name_included = False
		creating_file = False
		for i in request_content:
			if i == '' and not creating_file:
				creating_file = True

			elif creating_file:
				file_content += i+'\n'

			elif i[0:7] == "Problem":
				problem_id = i[9:]
				problem_name_included = True

		if not problem_name_included:
			self.logger.error("Request didn't include problem name. Please add 'Problem: id' header")
			self.send_response_400(client_socket, "\"Problem\" header is missing")
			return
		
		try:
			problem_id = int(problem_id)
		except:
			self.logger.error("'Problem' header didn't contain integer value")
			self.send_response_400(client_socket, "\"id\" in \"Problem: id\" header must be an integer")
			return

		self.logger.log(f"Successfully received user submission for {problem_id}")

		file_name = f"{problem_id}_{uuid4()}.cpp"
		file_manager.write_file(self.received_directory, file_name, file_content)

		self.logger.log(f"Created file: {file_name}")

		self.send_response_202(client_socket, problem_id, f"Successfully received '{problem_id}'")

		self.on_received(file_name)

	@staticmethod
	def send_response_202(s: socket.socket, problem_id: int, response: str) -> None:
		s.send(f"HTTP/1.1 202 Accepted\nContent-Type: text/plain\nContent-Length: {len(response)}\nProblem: {problem_id}\n\n{response}".encode("utf-8"))

	@staticmethod
	def send_response_400(s: socket.socket, response: str) -> None:
		s.send(f"HTTP/1.1 400 Bad Request\nContent-Type: text/plain\nContent-Length: {len(response)}\n\n{response}".encode("utf-8"))

	@staticmethod
	def send_response_405(s: socket.socket, response: str) -> None:
		s.send(f"HTTP/1.1 405 Method Not Allowed\nAllow: POST\nContent-Type: text/plain\nContent-Length: {len(response)}\n\n{response}".encode("utf-8"))
