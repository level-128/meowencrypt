"""
runlib.key_macro
this module handles keyboard event.
meowencrypt supports shortcut key to perform certain actions. This file
defined keyboard macro which triggered by keyboard shortcut.

When the boot.py executes, method start_keyboard_listen() will be called,
creating a thread and listening shortcuts.


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

import threading
import time

import keyboard
import mouse

from config.config_library import config
from enclib.enc_session import SessionError
from runlib.clipboard_listener import toggle_listen_clipboard as clipboard_listener_toggle_listen_clipboard
from runlib.clipboard_listener import get_is_listen_clipboard, start_clipboard_listen, \
	toggle_listen_clipboard_wrapper, NullSessionError, ContentError, EvtNotification
from runlib.enc_session_manager import to_session, encrypt_content
from runlib.pushed_content import push_clipboard, get_clipboard, push_notification


def _all_keys_released(keys: str):
	for x in keys.split('+'):
		while keyboard.is_pressed(x.strip()):
			time.sleep(0.08)


@toggle_listen_clipboard_wrapper
def _item_to_clipboard():
	push_clipboard(' ')
	mouse.click()
	time.sleep(0.04)
	mouse.click()
	time.sleep(0.1)
	keyboard.press('ctrl + a')
	time.sleep(0.05)
	keyboard.release('a')
	time.sleep(0.1)
	keyboard.press('insert')
	time.sleep(0.05)
	keyboard.release('ctrl + insert')
	time.sleep(0.1)


def _clipboard_to_item():
	mouse.click()
	time.sleep(0.04)
	mouse.click()
	time.sleep(0.1)
	keyboard.press_and_release('ctrl + a')
	keyboard.press_and_release('backspace')
	keyboard.write(get_clipboard())


def _encrypt_content(clipboard_content):
	try:
		encrypt_content(clipboard_content)
	except NullSessionError:
		push_notification("No established encrypt session. Create a session first, then encrypt the message.", "Error",
		                  True)
	except EvtNotification:
		_clipboard_to_item()
	except SessionError:
		push_notification("the last session is not established. establish the session to encrypt messages")


def _select_all_text_to_session():
	_all_keys_released(config.hotkey_select_all_text_to_session)
	_item_to_clipboard()
	# now the text is in clipboard
	clipboard_content = get_clipboard()
	try:
		to_session(clipboard_content)
	except (NullSessionError, ContentError):
		push_notification(
			"The content of the message can't be recognized, or the session is invalid. try again or reestablish the connection.",
			"Error")
	except EvtNotification:
		pass


def _select_all_text_and_encrypt():
	_all_keys_released(config.hotkey_select_all_text_to_encrypt)
	_item_to_clipboard()
	_encrypt_content(get_clipboard())


def _select_all_text_and_auto_process():
	_all_keys_released(config.hotkey_select_all_text_and_auto_process)
	_item_to_clipboard()
	clipboard_content = get_clipboard()
	try:
		to_session(clipboard_content)
	except (ContentError, NullSessionError) as e:
		_encrypt_content(clipboard_content)
	except EvtNotification:
		pass


def toggle_listen_clipboard():
	push_notification("Clipboard listener has turned off" if get_is_listen_clipboard() else "clipboard listener active")
	clipboard_listener_toggle_listen_clipboard()


def change_keyboard_hotkey() -> None:
	keyboard.remove_all_hotkeys()
	keyboard.add_hotkey(config.hotkey_select_all_text_to_session, _select_all_text_to_session)
	keyboard.add_hotkey(config.hotkey_select_all_text_to_encrypt, _select_all_text_and_encrypt)
	keyboard.add_hotkey(config.hotkey_toggle_listen_clipboard_change, toggle_listen_clipboard)
	keyboard.add_hotkey(config.hotkey_select_all_text_and_auto_process, _select_all_text_and_auto_process)


def start_keyboard_listen():
	def _start_keyboard_listen():
		keyboard.add_hotkey(config.hotkey_select_all_text_to_session, _select_all_text_to_session)
		keyboard.add_hotkey(config.hotkey_select_all_text_to_encrypt, _select_all_text_and_encrypt)
		keyboard.add_hotkey(config.hotkey_toggle_listen_clipboard_change, toggle_listen_clipboard)
		keyboard.add_hotkey(config.hotkey_select_all_text_and_auto_process, _select_all_text_and_auto_process)
		keyboard.wait()

	start_clipboard_listen()
	threading.Thread(target = _start_keyboard_listen).start()
