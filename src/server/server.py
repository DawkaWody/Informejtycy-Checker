import socket
import threading

class Color:
	error = "\033[38:5:160m"
	normal = "\033[38:5:7m"
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
	
	def handle_request(self, client_socket, client_address) -> str:
		request_line = client_socket.recv(1024).decode()
		if request_line[0:4] != "POST":
			print(f"{Color.error}ERROR:{Color.normal} invalid request send")
			return ""
		
		request_content = request_line.split('\r\n')
		file_content = ""
		
		creating_file = False
		for i in request_content:
			if i == '' and not creating_file:
				creating_file = True
			
			if creating_file:
				file_content += i
		print(file_content)