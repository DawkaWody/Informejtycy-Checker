import time
from uuid import uuid4

from code_checking.commands import Compiler

class Debugger:
    '''
    Class for managing gdb process.
    Firstly, the Debugger class is authenticated by the socket id.
    Secondly, there is check for auth code given in the last emit.
    '''

    def __init__(self, compiler: Compiler, debug_dir: str) -> None:
        self.compiler = compiler
        self.debug_dir = debug_dir

        self.last_ping_time: int = time.perf_counter() # time in seconds from the last time client pinged this class

    def run(self, code_file: str) -> None:
        '''
        Runs gdb process.
        :param code_file: Path to the source code file that will be debugged
        '''
        pass
