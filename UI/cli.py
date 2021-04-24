from runlib.enc_session_manager import *
from globalization.language_profile import print

import threading
import sys

def _show():
	print("This program should contains GUI, while currently, no GUI components were integrated in this program. ")
	print("Fall back to CLI until GUI components are ready.")
	print("APIs: \n-> get_last_session\n-> encrypt_content\n-> new_session\n-> to_session\n-> to_session_from_clipboard")
	print('use help(api) to show help.')
	print("""current key bindings: 
	    hotkey_select_all_text_to_session: str = 'ctrl + alt + a'
	    hotkey_select_all_text_to_encrypt: str = 'ctrl + alt + s'
	    hotkey_select_all_text_and_auto_process: str = 'ctrl + alt + z'
	    const_hotkey_toggle_listen_clipboard_change: str = 'ctrl + alt + q'""")
	while 1:
		try:
			exec(input('\n>>>'))
		except EvtNotification as push_content:
			print(f"\n-->: {push_content.content_to_notification=}\n{push_content.content_to_clipboard=}\n")
		except NullSessionError:
			print('\n-->: session not recognized\n')
		except Exception as e:
			print('\n-->:', e, '\n')


def show():
	if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():  # detect console / IDE environment
		threading.Thread(target=_show).start()