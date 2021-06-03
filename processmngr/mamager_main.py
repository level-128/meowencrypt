from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection as typePipe
from multiprocessing.context import Process as typeProcess
from typing import *
from abc import ABCMeta

Something = Optional[Any]


class __inner_func:
    __metaclass__ = ABCMeta

    @staticmethod
    def broadcast_fcall_rqst(pipe_fcall_recv: typePipe):
        for fcall_recv_content in pipe_fcall_recv.recv():
            ...


"""
the pipe needed for message exchange:
1. a none-duplex pipe from process to manager for processes to raise function call. 
    manager will create a thread for listening this pipe and broadcast to 2
    
2. none-duplex pipes from manager to processes for each instance to accept function call 

3. a none-duplex pipe from process to manager for processes to send function call return value
    similar as 1

4. none-duplex pipes from manager to processes for each instance to receive function call return value
"""


class manager:

    def __init__(self, my_process_ID: bytes):
        self.processes: Dict[bytes, Tuple[Optional[typeProcess], Optional[typePipe]]] = {my_process_ID: (None, None)}
        # create function call request pipe:
        self.pipe_fcall_recv, self.pipe_fcall_rqst = Pipe(False)
        # TODO: start listen function call request

    def create_process(self, target_process: Callable, process_ID: bytes):
        assert target_process not in self.processes, "You can't create two processes with same ID"
        pipe_manager, pipe_process = Pipe(True)
        # TODO: create a session manager for target process to bind functions and parse pipe protocol.
        target_process_instance = Process(target=Something, args=(pipe_process, self.pipe_fcall_rqst, target_process))
        self.processes[process_ID] = (target_process_instance, pipe_manager)
