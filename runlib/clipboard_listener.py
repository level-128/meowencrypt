import win32gui
import win32con
import win32clipboard
import threading

import pyperclip
from runlib.enc_session_manager import to_session_from_clipboard, NullSessionError, ContentError
from runlib.pushed_content import EvtNotification, is_ignore_last_clipboard, push_notification
from config.config_library import config
from typing import *


is_listen_clipboard: bool = config.is_default_listen_clipboard


def _clipboard_session():
	try:
		to_session_from_clipboard( )
	except EvtNotification:
		pass
	except NullSessionError:
		# print('nullsec')
		...
	except ContentError:
		# print('conterr')
		...


class clipboard_listener:
	"""
	using win32gui to create a window object. In Microsoft Windows, event will be broadcast to each window object.
	When clipboard changes, the window object will receive clipboard event, thus call method clipboard_listener.handle.
	This window is not used for GUI or display. it is used for capturing event only.
	"""
	def __init__(self):
		wc = win32gui.WNDCLASS( )  # create a window class
		wc.lpszClassName = ' '  # the window class name
		wc.style = 0
		wc.hbrBackground = 0
		win32gui.RegisterClass(wc)
		self.frame_handle = win32gui.CreateWindow(wc.lpszClassName,  # create a window with 0 size and poz.
		                                          '', 0, 0, 0, 0, 0, 0, 0, 0, None)

		self.last_msg_hash: int = 0  # record the hash value of the last copied item. if it is the same, _clipboard_session will not be called.

		# bind the window to listen clipboard event.
		win32gui.SetWindowLong(self.frame_handle, win32con.GWL_WNDPROC, self.handle)
		win32clipboard.SetClipboardViewer(self.frame_handle)

	def handle(self, _, msg, __, ___):
		if msg == win32con.WM_DRAWCLIPBOARD:
			if is_ignore_last_clipboard( ) or not is_listen_clipboard:
				return
			clipboard_data = pyperclip.paste( )
			if self.last_msg_hash != hash(clipboard_data):
				_clipboard_session( )
				self.last_msg_hash = hash(clipboard_data)


def start_clipboard_listen():
	def _start():
		clipboard_listener( )
		win32gui.PumpMessages( )

	_keyboard_listen_thread = threading.Thread(target=_start)
	_keyboard_listen_thread.start( )


def toggle_listen_clipboard() -> bool:
	global is_listen_clipboard
	is_listen_clipboard = not is_listen_clipboard
	return is_listen_clipboard


def get_is_listen_clipboard() -> bool:
	return is_listen_clipboard


def toggle_listen_clipboard_wrapper(func: callable) -> callable:

	def inner(*args, **kwargs):
		if get_is_listen_clipboard():
			toggle_listen_clipboard()
			func(*args, **kwargs)
			toggle_listen_clipboard()
		else:
			func(*args, **kwargs)

	return inner