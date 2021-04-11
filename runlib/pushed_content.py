import pyperclip
from threading import Thread
from win32api import GetModuleHandle
from win32con import CW_USEDEFAULT, IMAGE_ICON, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_USER, WS_OVERLAPPED, WS_SYSMENU
from win32gui import CreateWindow, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, \
	NIM_MODIFY, RegisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

_is_ignore_last_clipboard: bool = False

_last_push_clipboard_content: str = ''


class EvtNotification(Exception):
	def __init__(self, *, content_to_clipboard: str = '', content_to_notification: str = '',
	             notification_title: str = ''):
		self.content_to_clipboard = content_to_clipboard
		self.content_to_notification = content_to_notification
		super(EvtNotification, self).__init__("this event has not been handled")

		if self.content_to_notification:
			Thread(target=lambda:notification_.show_windows_notification(notification_title if notification_title else 'note: ', content_to_notification)).start( )
		if self.content_to_clipboard:
			global _is_ignore_last_clipboard
			_is_ignore_last_clipboard = True
			pyperclip.copy(self.content_to_clipboard)


#  TODO: add commit about inspiration: https://github.com/jithurjacob/Windows-10-Toast-Notifications
class windows_notification(object):
	def __init__(self):
		# message_map = {WM_DESTROY: self.on_destroy, }

		# Register the window class.
		self.wc = WNDCLASS( )
		self.hinst = self.wc.hInstance = GetModuleHandle(None)
		self.wc.lpszClassName = str("PythonTaskbar")  # must be a string
		# self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
		try:
			self.classAtom = RegisterClass(self.wc)
		except:
			pass  #not sure of this
		style = WS_OVERLAPPED | WS_SYSMENU
		self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
		                         0, 0, CW_USEDEFAULT,
		                         CW_USEDEFAULT,
		                         0, 0, self.hinst, None)
		UpdateWindow(self.hwnd)

		icon_path = r'files/level-128_avatar_128x128.ico'  # TODO: register it into config_library
		icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
		try:
			self.hicon = LoadImage(self.hinst, icon_path,
			                       IMAGE_ICON, 0, 0, icon_flags)
		except Exception as e:
			raise Exception("The icon for windows 10 push notification is invalid")
		flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
		nid = (self.hwnd, 0, flags, WM_USER + 20, self.hicon, "The meowencrypt is running")
		Shell_NotifyIcon(NIM_ADD, nid)

	def show_windows_notification(self, content_to_notification: str, notification_title: str = 'Note:'):
		Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
		                              WM_USER + 20,
		                              self.hicon, "", content_to_notification, 200,
		                              notification_title))


notification_ = windows_notification( )

push_notification = notification_.show_windows_notification


def push_clipboard(content_to_clipboard: str):
	if content_to_clipboard != _last_push_clipboard_content:
		global _is_ignore_last_clipboard
		_is_ignore_last_clipboard = True
		pyperclip.copy(content_to_clipboard)


def get_clipboard() -> str:
	return pyperclip.paste( )


def get_last_pasted_item() -> str:
	return _last_push_clipboard_content


def is_ignore_last_clipboard():
	global _is_ignore_last_clipboard
	if _is_ignore_last_clipboard:
		_is_ignore_last_clipboard = False
		return True
	return False