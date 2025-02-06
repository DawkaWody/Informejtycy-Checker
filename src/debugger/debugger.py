from uuid import uuid4

from .commands import Compiler

class Debugger:
    '''
    Class for managing gdb process.
    Because client stays on connection with debugger for a long time, there is double authentication.
    First auth is static, in debug_processes dictionary, with mapped Debugger class to it.
    Second is inside the class.
    When socketio.emit, the second auth code is given, so that having first auth doesn't let you use Debugger.
    The second auth is dynamic, after some time different is going to be send.
    '''

    def __init__(self, compiler: Compiler) -> None:
        self.compiler = compiler
        self.second_auth = uuid4()

    def run(self, code_file: str) -> None:
        '''
        Runs gdb process.
        :param code_file: Path to the source code file that will be debugged
        '''
        pass
