from server.server import Server
from code_checking.pack_loader import PackLoader
from code_checking.checker import Checker
from code_checking.commands import Compiler
from threading import Thread

def received_file(filename: str) -> None:
    print(f"Received {filename}, should be in ../received/{filename[0:7]}...")

def print_stats(result):
    print("Accuracy: " + str(result["%"]) + "%")

if __name__ == "__main__":
    pl = PackLoader('../tests', '.test', 'in', 'out')
    print(pl.load_bytes(0))
    print()
    compiler = Compiler('g++', '../received/', '../received/compiled')
    checker = Checker(compiler, pl)
    lt = Thread(target=checker.listen)
    lt.start()
    checker.push_check('0_a1ce0081-caff-426c-80ff-cd390683e5d1.cpp', 0, print_stats)

    server = Server(received_file)
    server.run()
