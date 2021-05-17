import multiprocessing
import threading
import platform

import wx

message_frame_pipe = None


def main():
	global message_frame_pipe
	message_frame_pipe, __receive_pipe = multiprocessing.Pipe()
	process = multiprocessing.Process(target=_main_UI_process, args=(__receive_pipe,), name='UI_process')
	process.start()


def get_pipe():
	return message_frame_pipe


def _main_UI_process(pipe):
	from UI.main_UI import main_UI
	from UI.session_manager_UI import session_manager as session_manager_UI
	from UI.session_UI import session_UI

	def show_UIs(_pipe):
		while True:
			for content in _pipe.recv():
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

	threading.Thread(target=show_UIs, args=(pipe,)).start()
	app.MainLoop()


def show_UI(frame):
	assert multiprocessing.current_process().name == 'UI_process', "show_UI method must run inside the UI_process"
	assert threading.current_thread() == threading.main_thread(), "show_UI method must run as main thread"
	frame_instance = frame()
	frame_instance.Show()
