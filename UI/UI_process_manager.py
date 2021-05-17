import multiprocessing
import threading
import platform
from multiprocessing.dummy import Lock
from multiprocessing.dummy.connection import Connection
from typing import Optional

import wx

message_frame_pipe: Optional[Connection] = None
function_call_receive_pipe: Optional[Connection] = None
function_call_pipe: Optional[Connection] = None
function_call_lock: Optional[Lock] = None


def outer(func):
	def _(*args, **kwargs):
		assert multiprocessing.current_process().name == "MainProcess", "this function must execute within main process"
		return func(*args, **kwargs)

	return _


@outer
def main():
	global message_frame_pipe, function_call_pipe
	__message_frame_receive_pipe, message_frame_pipe = multiprocessing.Pipe(False)
	__function_call_receive_pipe, function_call_pipe = multiprocessing.Pipe(True)

	thread = threading.Thread(target=_main_function_call_process, args=(function_call_pipe,), name='UI_function_call_process')
	thread.start()

	process = multiprocessing.Process(target=_main_UI_thread, args=(__message_frame_receive_pipe, __function_call_receive_pipe), name='UI_process')
	process.start()


@outer
def get_frame_pipe():
	return message_frame_pipe


def _main_function_call_process(pipe):
	while True:
		func, args, kwargs = pipe.recv()
		pipe.send(eval(func)(*args, **kwargs))


def _main_UI_thread(__message_frame_receive_pipe, __function_call_receive_pipe):
	global function_call_receive_pipe, function_call_lock
	function_call_receive_pipe = __function_call_receive_pipe
	function_call_lock = multiprocessing.Lock()

	from UI.main_UI import main_UI
	from UI.session_manager_UI import session_manager as session_manager_UI
	from UI.session_UI import session_UI

	def show_UIs(_pipe):
		while True:
			content = _pipe.recv()
			if content == 'show_main':
				wx.CallAfter(lambda: main_UI_frame.Show())
			elif content == 'show_session_manager':
				wx.CallAfter(lambda: session_manager_UI_frame.Show())
			elif content == 'show_session_UI':
				wx.CallAfter(lambda: session_UI_frame.Show())
			else:
				raise ValueError(f"{content} in pipe is not valid")

	if platform.system() == 'Windows':
		import ctypes
		ctypes.windll.shcore.SetProcessDpiAwareness(1)

	app = wx.App()
	main_UI_frame = main_UI()
	session_manager_UI_frame = session_manager_UI()
	session_UI_frame = session_UI()

	threading.Thread(target=show_UIs, args=(__message_frame_receive_pipe,)).start()
	app.MainLoop()


def show_UI(frame):
	assert multiprocessing.current_process().name == 'UI_process', "show_UI method must run inside the UI_process"
	assert threading.current_thread() is threading.main_thread(), "show_UI method must run as main thread"
	frame_instance = frame()
	frame_instance.Show()


def function_call(function: str, *args, **kwargs):
	global function_call_receive_pipe, function_call_lock

	function_call_lock.acquire(True)
	function_call_receive_pipe.send([function, args, kwargs])
	return_ = function_call_receive_pipe.recv()
	function_call_lock.release()
	return return_
