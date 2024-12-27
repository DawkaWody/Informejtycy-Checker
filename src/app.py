from server import Server

#from pack_loader import PackLoader
#pl = PackLoader('../tests', '.test', 'in', 'out')
#print(pl.load_bytes(0))
#print(pl.load_bytes(1))
#print(pl.load_bytes(2))

def asdfadf(filename: str):
    print(filename)

if __name__ == "__main__":
	server = Server("localhost")
	server.run()