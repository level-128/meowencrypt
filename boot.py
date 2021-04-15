"""
meowencrypt boot:

The program should start executing from this file.

This file should include proper procedure to start all events and threads.


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

from runlib.key_macro import start_keyboard_listen
from runlib.enc_session_manager import *
from globalization.language_profile import print
from UI.session_UI import start_session_UI

start_session_UI( )

start_keyboard_listen( )

print("This program should contains GUI, while currently, no GUI components were integrated in this program. ")
print("Fall back to CLI until GUI components are ready.")
print("APIs: \n-> get_last_session\n-> encrypt_content\n-> new_session\n-> to_session\n-> to_session_from_clipboard")
print('use help(api) to show help.')
print("""current key bindings: 
    hotkey_select_all_text_to_session: str = 'ctrl + alt + a'
    hotkey_select_all_text_to_encrypt: str = 'ctrl + alt + s'
    hotkey_select_all_text_and_auto_process: str = 'ctrl + alt + z'
    const_hotkey_toggle_listen_clipboard_change: str = 'ctrl + alt + q'""")

if __name__ == '__main__':
	try:
		new_session( )
	except:
		pass
	while 1:
		try:
			exec(input('\n>>>'))
		except EvtNotification as push_content:
			print(f"\n-->: {push_content.content_to_notification=}\n{push_content.content_to_clipboard=}\n")
		except NullSessionError:
			print('\n-->: session not recognized\n')
		except Exception as e:
			print('\n-->:', e, '\n')