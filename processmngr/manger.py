from multiprocessing import Process, Pipe
from typing import Callable


class manager:

    def __init__(self, process: Callable, process_name: bytes):
        self.callables = {}
        self.process_name = process_name
        self.pipe, to_pipe = Pipe(True)
        self.process = Process(target=process, args=(to_pipe, ))

    def register(self, callable_name: bytes, callable_: Callable):
        self.callables[callable_name] = callable_


