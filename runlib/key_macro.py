import keyboard
import mouse
import time
import threading

from runlib.pushed_content import EvtNotification, get_clipboard, push_notification, push_clipboard
from runlib.enc_session_manager import to_session, NullSessionError, ContentError, encrypt_content
from runlib.clipboard_listener import toggle_listen_clipboard, get_is_listen_clipboard, start_clipboard_listen,\
	toggle_listen_clipboard_wrapper
from config.config_library import config


def _all_keys_released(keys: str):
	for x in keys.split('+'):
		while keyboard.is_pressed(x.strip( )):
			time.sleep(0.08)


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
	_all_keys_released(config.hotkey_select_all_text_to_session)
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
	_all_keys_released(config.hotkey_select_all_text_to_encrypt)
	_item_to_clipboard( )
	clipboard_content = get_clipboard()
	try:
		encrypt_content(clipboard_content)
	except NullSessionError:
		print('nothing')
	except EvtNotification:
		_clipboard_to_item( )


def _select_all_text_and_auto_process():
	_all_keys_released(config.hotkey_select_all_text_and_auto_process)
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
	push_notification("Clipboard listener has turned off" if get_is_listen_clipboard() else "clipboard listener active")
	toggle_listen_clipboard()


def change_keyboard_hotkey() -> None:
	keyboard.remove_all_hotkeys()
	keyboard.add_hotkey(config.hotkey_select_all_text_to_session, _select_all_text_to_session)
	keyboard.add_hotkey(config.hotkey_select_all_text_to_encrypt, _select_all_text_and_encrypt)
	keyboard.add_hotkey(config.const_hotkey_toggle_listen_clipboard_change, _toggle_listen_clipboard)
	keyboard.add_hotkey(config.hotkey_select_all_text_and_auto_process, _select_all_text_and_auto_process)


def start_keyboard_listen():
	def _start_keyboard_listen():
		keyboard.add_hotkey(config.hotkey_select_all_text_to_session, _select_all_text_to_session)
		keyboard.add_hotkey(config.hotkey_select_all_text_to_encrypt, _select_all_text_and_encrypt)
		keyboard.add_hotkey(config.const_hotkey_toggle_listen_clipboard_change, _toggle_listen_clipboard)
		keyboard.add_hotkey(config.hotkey_select_all_text_and_auto_process, _select_all_text_and_auto_process)
		keyboard.wait( )

	start_clipboard_listen()
	threading.Thread(target=_start_keyboard_listen).start( )
