import socket
import threading

class Server():
	def __init__(self, host: str, port: int = 5000, directory: str = None) -> None:
		self.host = host
		self.port = port
		self.directory = directory
		self.server_socket = socket.create_server((self.host, self.port), reuse_port = True)
	
	def run(self) -> None:
		print(f"Server is running {self.host}:{self.port}")
		while True:
			client_socket, client_address = self.server_socket.accept()
			thread = threading.Thread(target = self.handle_request, args = (client_socket, client_address))
			thread.start()
	
	def handle_request(self, client_socket, client_address):
		request_line = client_socket.recv(1024).decode()
		request_content = request_line.split('\r\n')
		headers = {}
		for i, content in enumerate(request_content):
			if i == 0:
				request_type, url, http_version = content.split(" ")
			elif i == len(request_content) - 1:
				body = content
			elif content and ':' in content:
				key, val = content.split(": ")
				headers[key] = val
		print("Request content: {request_content}")