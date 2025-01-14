import socket
import threading
from typing import Callable
from uuid import uuid4
from os.path import join

from .logger import Logger
from . import IP, PORT, RECEIVED_DIR, REQUEST_LIMIT, REQUEST_TIME_PERIOD_SECONDS
from .client import Client

class Server:
	def __init__(self, on_received: Callable[[str, Client], None], problem_count: int, logger: Logger) -> None:
		self.host = IP
		self.port = PORT
		self.server_socket = socket.create_server((self.host, self.port))
		
		self.logger = logger

		self.on_received = on_received
		self.received_directory = RECEIVED_DIR
		
		self.problem_count = problem_count
	
	def run(self) -> None:
		self.logger.info(f"Server is running {self.host}:{self.port}")
		
		self.logger.start_log_cleaner()
		
		while True:
			client_socket, client_address = self.server_socket.accept()
			server_thread = threading.Thread(target=self.handle_request, args=(client_socket, client_address))
			server_thread.start()
	
	def handle_request(self, client_socket: socket.socket, client_address: tuple[str, int]) -> None:
		request_limit_exceeded = self.logger.log_request(client_address)
		if request_limit_exceeded:
			self.logger.error(f"Too many requests from {client_address[0]}:{client_address[1]}")
			self.send_response_429(client_socket, f"Too many requests. Only {REQUEST_LIMIT} requests per {REQUEST_TIME_PERIOD_SECONDS} seconds from one IP")
			return

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
			self.logger.error("Request didn't include problem id. Please add 'Problem: id' header")
			self.send_response_400(client_socket, "\"Problem\" header is missing")
			return
		
		try:
			problem_id = int(problem_id)
		except ValueError:
			self.logger.error("'Problem' header didn't contain integer value")
			self.send_response_400(client_socket, "\"id\" in \"Problem: id\" header must be an integer")
			return
			
		self.logger.info(f"Successfully received user submission for {problem_id}")

		file_name = f"{problem_id}_{uuid4()}.cpp"
		with open(join(self.received_directory, file_name), 'w') as f:
			f.write(file_content)

		self.logger.info(f"Created file: {file_name}")

		self.on_received(file_name, Client(client_socket, client_address))

	@staticmethod
	def send_response_202(s: socket.socket, problem_id: int, response: str, extra_headers: str = "\n") -> None:
		s.send(f"HTTP/1.1 202 Accepted\nContent-Type: text/plain\nContent-Length: {len(response)}\nProblem: {problem_id}\n{extra_headers}\n{response}".encode("utf-8"))

	@staticmethod
	def send_response_400(s: socket.socket, response: str, extra_headers: str = "\n") -> None:
		s.send(f"HTTP/1.1 400 Bad Request\nContent-Type: text/plain\nContent-Length: {len(response)}\n{extra_headers}\n{response}".encode("utf-8"))

	@staticmethod
	def send_response_405(s: socket.socket, response: str, extra_headers: str = "\n") -> None:
		s.send(f"HTTP/1.1 405 Method Not Allowed\nAllow: POST\nContent-Type: text/plain\nContent-Length: {len(response)}\n{extra_headers}\n{response}".encode("utf-8"))

	@staticmethod
	def send_response_429(s: socket.socket, response: str, extra_headers: str = "\n") -> None:
		s.send(f"HTTP/1.1 429 Too Many Requests\nRetry-After: {REQUEST_TIME_PERIOD_SECONDS}\nContent-Type: text/plain\nContent-Length: {len(response)}\n{extra_headers}\n{response}".encode("utf-8"))