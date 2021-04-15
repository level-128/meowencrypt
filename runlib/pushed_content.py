"""
meowencrypt runlib.pushed_content:

this module handles clipboard modification and windows 10 notification
banner.

In meowencrypt, it is recommended to use notification banner instead
of popping up a message window, the latter will interrupt users' work
flow. The circumstances which we (developers) should consider to use
pop up message window to notify users are:

1. the length of the message has exceeds the limit (around 170 Latin
or Cyrillic characters or 90 Asian characters, while I have no idea
about other writing systems). When the character count exceeds the
limit, windows notification banner will likely to cutoff some of
the characters.
2. the message is VERY important (Eg: the session ID mismatch while
the check sum is correct, indicating fail session establishment).

There are two ways to handle windows notification and clipboard
event: by raising exception EvtNotification then catch this event
at the outer scope, or calling none thread-blocking APIs.


COPYRIGHT NOTICE:
Copyright (C) 2021  level-128

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pyperclip
from threading import Thread
from win32api import GetModuleHandle, MessageBox
from win32con import IMAGE_ICON, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_USER, WS_OVERLAPPED, WS_SYSMENU, MB_OK, MB_SETFOREGROUND
from win32gui import CreateWindow, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD,\
	NIM_MODIFY, RegisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

from globalization.language_profile import _

_is_ignore_last_clipboard: bool = False

_last_push_clipboard_content: str = ''


class EvtNotification(Exception):
	def __init__(self, *, content_to_clipboard: str = '', content_to_notification: str = '',
	             notification_title: str = ''):
		self.content_to_clipboard = content_to_clipboard
		self.content_to_notification = content_to_notification
		super(EvtNotification, self).__init__("this event has not been handled")

		if self.content_to_notification:
			notification_.show_windows_notification(content_to_notification, notification_title if notification_title else 'note:')
		if self.content_to_clipboard:
			global _is_ignore_last_clipboard
			_is_ignore_last_clipboard = True
			pyperclip.copy(self.content_to_clipboard)


#  TODO: add commit about content inspiration source: https://github.com/jithurjacob/Windows-10-Toast-Notifications
class windows_notification(object):
	def __init__(self):

		# Register the window class.
		self.wc = WNDCLASS( )
		self.hinst = self.wc.hInstance = GetModuleHandle(None)
		self.wc.lpszClassName = 'pushed_content'
		RegisterClass(self.wc)

		style = WS_OVERLAPPED | WS_SYSMENU
		self.hwnd = CreateWindow(self.wc.lpszClassName, '', style,
		                         0, 0, 0, 0, 0, 0, self.hinst, None)
		UpdateWindow(self.hwnd)

		icon_path = r'files/level-128_avatar_128x128.ico'  # TODO: register it into config_library
		icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
		try:
			self.hicon = LoadImage(self.hinst, icon_path, IMAGE_ICON, 0, 0, icon_flags)
		except Exception as e:
			raise Exception(f"The icon for windows 10 push notification is invalid {e=}")
		flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
		nid = (self.hwnd, 0, flags, WM_USER + 20, self.hicon, _("The meowencrypt is running"))
		Shell_NotifyIcon(NIM_ADD, nid)

	def show_windows_notification(self, content_to_notification: str, notification_title: str = 'note:',
								  is_force_message_box: bool = False):
		content_to_notification, notification_title = _(content_to_notification), _(notification_title)
		if not is_force_message_box and self.__is_length_count_in_limit(content_to_notification):
			Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
			                              WM_USER + 20,
			                              self.hicon, "", content_to_notification, 200,
			                              notification_title))
		else:
			MessageBox(0, content_to_notification, notification_title, MB_OK | MB_SETFOREGROUND)

	@staticmethod
	def __is_length_count_in_limit(content: str) -> bool:
		"""
		determine whether the content could be displayed through windows notification banner.
		"""
		length: float = 0.0
		for char in content:
			if ord(char) < 0x0530:  # before unicode Armenian, the end of Cyrillic Supplement
				length += 1
			else:
				length += 2.118  #
			if length > 170:
				return False
		return True
#  TODO: when AES method decrypt the message, space padding will remain

notification_ = windows_notification( )

push_notification = notification_.show_windows_notification


def push_clipboard(content_to_clipboard: str):
	"""
	copy the content into clipboard
	"""
	if content_to_clipboard != _last_push_clipboard_content:
		global _is_ignore_last_clipboard
		_is_ignore_last_clipboard = True
		pyperclip.copy(content_to_clipboard)


def get_clipboard() -> str:
	return pyperclip.paste( )


def get_last_pasted_item() -> str:
	return _last_push_clipboard_content


def is_ignore_last_clipboard():
	"""
	should call by runlib.clipboard_listener
	when the clipboard is modified by means, the clipboard listener shouldn't be triggered.
	"""
	global _is_ignore_last_clipboard
	if _is_ignore_last_clipboard:
		_is_ignore_last_clipboard = False
		return True
	return False
