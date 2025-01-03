import socket


class Client():
	
	def __init__(self, client_socket: socket.socket, client_address: tuple[str, int]) -> None:
		self.SOCKET = client_socket
		self.IP = client_address[0]
		self.PORT = client_address[1]