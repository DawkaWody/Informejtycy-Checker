import socket
import threading
from uuid import uuid4
from os.path import exists as fExists

class Color:
	error = "\033[38:5:160m"
	normal = "\033[0m"
	info = "\033[38:5:27m"

class Server():
	def __init__(self, host: str, port: int = 5000) -> None:
		self.host = host
		self.port = port
		self.server_socket = socket.create_server((self.host, self.port))
		
		self.received_directory = "received"
	
	def run(self) -> None:
		print(f"{Color.info}INFO:{Color.normal} Server is running {self.host}:{self.port}")
		while True:
			client_socket, client_address = self.server_socket.accept()
			thread = threading.Thread(target = self.handle_request, args = (client_socket, client_address))
			thread.start()
	
	def handle_request(self, client_socket: socket.socket, client_address: tuple[str, int]) -> str:
		request_line = client_socket.recv(1024).decode()
		
		if request_line[0:4] != "POST":
			print(f"{Color.error}ERROR:{Color.normal} Invalid request send")
			self.send_response_405(client_socket, "Only POST method available")
			return ""
		
		request_content = request_line.split('\r\n')
		file_content = ""
		
		problem_name = ""
		problem_name_included = False
		creating_file = False
		for i in request_content:
			if i == '' and not creating_file:
				creating_file = True
				
			elif creating_file:
				file_content += i+'\n'
			
			elif i[0:7] == "Problem":
				problem_name = i[9:]
				problem_name_included = True
		
		if not problem_name_included:
			print(f"{Color.error}ERROR:{Color.normal} Request didn't include problem name. Please add 'Problem: name' header")
			self.send_response_400(client_socket, "\"Problem\" header is missing")
			return ""
			
		print(f"{Color.info}INFO:{Color.normal} Successfully received user submission for {problem_name}")
		
		file_name = f"{problem_name}_{uuid4()}.cpp"
		with open(f"{self.received_directory}/{file_name}", "w") as f:
			f.write(file_content)
		
		print(f"{Color.info}INFO:{Color.normal} Created file: {file_name}")
		
		self.send_response_202(client_socket, problem_name, f"Successfully received '{problem_name}'")
	
	def send_response_202(self, s: socket.socket, problem_name: str, response: str) -> None:
		s.send(f"HTTP/1.1 202 Accepted\nContent-Type: text/plain\nContent-Length: {len(response)}\nProblem: {problem_name}\n\n{response}".encode("utf-8"))
	
	def send_response_400(self, s: socket.socket, response: str) -> None:
		s.send(f"HTTP/1.1 400 Bad Request\nContent-Type: text/plain\nContent-Length: {len(response)}\n\n{response}".encode("utf-8"))
	
	def send_response_405(self, s: socket.socket, response: str) -> None:
		s.send(f"HTTP/1.1 405 Method Not Allowed\nAllow: POST\nContent-Type: text/plain\nContent-Length: {len(response)}\n\n{response}".encode("utf-8"))
		