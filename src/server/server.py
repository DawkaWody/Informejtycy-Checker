import socket
import threading
from os.path import exists as fExists

class Color:
	error = "\033[38:5:160m"
	normal = "\033[0m"
	info = "\033[38:5:27m"

class Server():
	def __init__(self, host: str, port: int = 5000, directory: str = None) -> None:
		self.host = host
		self.port = port
		self.directory = directory
		self.server_socket = socket.create_server((self.host, self.port))
	
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
			return ""
		
		request_content = request_line.split('\r\n')
		file_content = ""
		
		creating_file = False
		for i in request_content:
			if i == '' and not creating_file:
				creating_file = True
			
			if creating_file:
				file_content += i+'\n'
		
		with open("received/received.cpp", "w") as f:
			f.write(file_content)
		print(f"{Color.info}INFO:{Color.normal} Successfully received user submission")
		
		self.send_response_202(client_socket, "success")
	
	def send_response_202(self, s: socket.socket, response: str) -> None:
		s.send(("HTTP/1.1 202 Accepted\nContent-Type: text/plain\n\n"+response).encode("utf-8"))