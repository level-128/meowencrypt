from runlib.key_macro import start_keyboard_listen
from runlib.enc_session_manager import *

start_keyboard_listen()


if __name__ == '__main__':
	try:
		new_session()
	except: pass
	while 1:
		try:
			exec(input('>>>'))
		except EvtNotification as push_content:
			print(f"\n-->: {push_content.content_to_notification=}\n{push_content.content_to_clipboard=}\n")
		except NullSessionError:
			print('\n-->: session not recognized\n')
		except Exception as e:
			print('\n-->:', e, '\n')

