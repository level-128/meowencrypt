import os

from runlib.enc_session_manager import *
from config.config_library import config

import threading
import sys


def _show():
	print("CLI utility for meowencrypt.")
	print("APIs: \n-> get_last_session\n-> encrypt_content\n-> new_session\n-> to_session\n-> to_session_from_clipboard")
	print('use help(api) to show help.')
	while 1:
		try:
			exec(input())
		except EvtNotification as push_content:
			print(f"\n-->: {push_content.content_to_notification=}\n{push_content.content_to_clipboard=}\n")
		except NullSessionError:
			print('\n-->: session not recognized\n')
		except Exception as e:
			print('\n-->:', e, '\n')
		except KeyboardInterrupt:
			print('exiting the program....')
			sys.exit(0)


def show():
	if config.is_show_cli:
		if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():  # detect console / IDE environment
			print('detected that meowencrypt is running in console')
			threading.Thread(target=_show).start()

		elif 'PYCHARM_HOSTED' in os.environ:  # program runs in Pycharm
			print('detected that meowencrypt is running in Pycharm')
			threading.Thread(target=_show).start()
