import keyboard
import mouse
import pyperclip
import time
import threading
from runlib.clipboard_listener import toggle_listen_clipboard
from runlib.notification import EvtNotification
from runlib.enc_session_manager import get_last_session, to_session, NullSessionError, ContentError, encrypt_content


CONST_HOTKEY_SELECT_ALL_TEXT_TO_SESSION: str = 'ctrl + alt + a'

CONST_HOTKEY_SELECT_ALL_TEXT_TO_ENCRYPT: str = 'ctrl + alt + s'


def _all_keys_released(keys: str):
	for x in keys.split('+'):
		while keyboard.is_pressed(x.strip( )):
			time.sleep(0.05)


def _item_to_clipboard():
	toggle_listen_clipboard( )  # stop listening the keyboard.
	pyperclip.copy('  ')
	mouse.click( )
	time.sleep(0.04)
	mouse.click( )
	time.sleep(0.1)
	keyboard.press('ctrl + a')
	time.sleep(0.05)
	keyboard.release('a')
	time.sleep(0.1)
	keyboard.press('insert')
	time.sleep(0.05)
	keyboard.release('ctrl + insert')
	time.sleep(0.1)
	toggle_listen_clipboard( )


def _clipboard_to_item():
	mouse.click( )
	time.sleep(0.04)
	mouse.click( )
	time.sleep(0.1)
	keyboard.press_and_release('ctrl + a')
	keyboard.press_and_release('backspace')
	keyboard.write(pyperclip.paste( ))


def _select_all_text_to_session():
	_all_keys_released(CONST_HOTKEY_SELECT_ALL_TEXT_TO_SESSION)
	_item_to_clipboard( )
	# now the text is in clipboard
	clipboard_content = pyperclip.paste( )
	try:
		to_session(clipboard_content)
	except (NullSessionError, ContentError):
		print('null_session')
	except EvtNotification:
		pass


def _select_all_text_and_encrypt():
	_all_keys_released(CONST_HOTKEY_SELECT_ALL_TEXT_TO_ENCRYPT)
	_item_to_clipboard( )
	clipboard_content = pyperclip.paste( )
	try:
		encrypt_content(clipboard_content)
	except NullSessionError:
		print('nothing')
	except EvtNotification:
		_clipboard_to_item( )


def start_keyboard_listen():
	def _start_keyboard_listen():
		keyboard.add_hotkey(CONST_HOTKEY_SELECT_ALL_TEXT_TO_SESSION, _select_all_text_to_session)
		keyboard.add_hotkey(CONST_HOTKEY_SELECT_ALL_TEXT_TO_ENCRYPT, _select_all_text_and_encrypt)
		keyboard.wait( )

	threading.Thread(target=_start_keyboard_listen).start( )