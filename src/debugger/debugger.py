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

        self.auth: str = ""

    def run(self, code_file: str) -> None:
        '''
        Runs gdb process.
        :param code_file: Path to the source code file that will be debugged
        '''
        pass

    def get_next_auth(self, last_auth: str = "") -> str:
        '''
        Returns next uuid4 authentication code. If last authentication doesn't match current debugger one, then stop debugging.
        :param last_auth: The last authentication code given by debugger
        :return: uuid4 authentication code
        '''
        if last_auth != self.auth:
            # Stop Debugging
            return ""

        self.auth = str(uuid4())
        return self.auth
