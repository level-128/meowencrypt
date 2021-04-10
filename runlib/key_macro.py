import keyboard
import mouse
import time
import threading

from runlib.pushed_content import EvtNotification, get_clipboard, push_notification, push_clipboard, get_last_pasted_item
from runlib.enc_session_manager import get_last_session, to_session, NullSessionError, ContentError, encrypt_content
from runlib.clipboard_listener import toggle_listen_clipboard, get_is_listen_clipboard, start_clipboard_listen, toggle_listen_clipboard_wrapper

# TODO: error in using to session to decrypt.

CONST_HOTKEY_SELECT_ALL_TEXT_TO_SESSION: str = 'ctrl + alt + a'

CONST_HOTKEY_SELECT_ALL_TEXT_TO_ENCRYPT: str = 'ctrl + alt + s'

CONST_HOTKEY_SELECT_ALL_TEXT_AND_AUTO_PROCESS: str = 'ctrl + alt + z'

CONST_HOTKEY_TOGGLE_LISTEN_CLIPBOARD_CHANGE: str = 'ctrl + alt + q'


def _all_keys_released(keys: str):
	for x in keys.split('+'):
		while keyboard.is_pressed(x.strip( )):
			time.sleep(0.05)


@toggle_listen_clipboard_wrapper
def _item_to_clipboard():
	push_clipboard(' ')
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


def _clipboard_to_item():
	mouse.click( )
	time.sleep(0.04)
	mouse.click( )
	time.sleep(0.1)
	keyboard.press_and_release('ctrl + a')
	keyboard.press_and_release('backspace')
	keyboard.write(get_clipboard())


def _select_all_text_to_session():
	_all_keys_released(CONST_HOTKEY_SELECT_ALL_TEXT_TO_SESSION)
	_item_to_clipboard( )
	# now the text is in clipboard
	clipboard_content = get_clipboard()
	try:
		to_session(clipboard_content)
	except (NullSessionError, ContentError):
		print('null_session')
	except EvtNotification:
		pass


def _select_all_text_and_encrypt():
	_all_keys_released(CONST_HOTKEY_SELECT_ALL_TEXT_TO_ENCRYPT)
	_item_to_clipboard( )
	clipboard_content = get_clipboard()
	try:
		encrypt_content(clipboard_content)
	except NullSessionError:
		print('nothing')
	except EvtNotification:
		_clipboard_to_item( )


def _select_all_text_and_auto_process():
	_all_keys_released(CONST_HOTKEY_SELECT_ALL_TEXT_AND_AUTO_PROCESS)
	_item_to_clipboard( )
	clipboard_content = get_clipboard( )
	try:
		to_session(clipboard_content)
	except (ContentError, NullSessionError):
		try:
			encrypt_content(clipboard_content)
		except NullSessionError:
			print('nothing')
		except EvtNotification:
			_clipboard_to_item( )

	except EvtNotification:
		pass

def _toggle_listen_clipboard():
	push_notification("turned off clipboard listener" if get_is_listen_clipboard() else "clipboard listener active")
	toggle_listen_clipboard()


def start_keyboard_listen():
	def _start_keyboard_listen():
		keyboard.add_hotkey(CONST_HOTKEY_SELECT_ALL_TEXT_TO_SESSION, _select_all_text_to_session)
		keyboard.add_hotkey(CONST_HOTKEY_SELECT_ALL_TEXT_TO_ENCRYPT, _select_all_text_and_encrypt)
		keyboard.add_hotkey(CONST_HOTKEY_TOGGLE_LISTEN_CLIPBOARD_CHANGE, _toggle_listen_clipboard)
		keyboard.add_hotkey(CONST_HOTKEY_SELECT_ALL_TEXT_AND_AUTO_PROCESS, _select_all_text_and_auto_process)
		keyboard.wait( )

	start_clipboard_listen()
	threading.Thread(target=_start_keyboard_listen).start( )