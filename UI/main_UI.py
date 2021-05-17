import os
import sys
import threading
import webbrowser

import wx

from UI.message import message_box, message_dialog
from UI.settings_UI import show as settings_UI_show
from UI.theme_setter import set_color
from UI.UI_process_manager import get_frame_pipe, show_UI
from UI.session_manager_UI import session_manager as session_manager_UI
from UI.session_UI import session_UI
from config.config_library import config, VERSION
from runlib.clipboard_listener import toggle_listen_clipboard
from runlib.enc_session_manager import auto_new_session

class main_UI(wx.Frame):

	def _conv(self, x, y=0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def __init__(self):
		super().__init__(None, title='session frame',
		                 style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		set_color(self, True)
		self.Bind(wx.EVT_CLOSE, self.on_exit)

		def set_menu_bar():
			self.menu_bar = wx.MenuBar()
			self.SetMenuBar(self.menu_bar)

			self.new_menu = wx.Menu()
			self.new_session = self.new_menu.Append(wx.ID_ANY, f"new session\t{config.hotkey_new_session}")
			self.Bind(wx.EVT_MENU, self.on_new_session, self.new_session)
			new_advanced_session = self.new_menu.Append(wx.ID_ANY, 'new advanced session')
			self.Bind(wx.EVT_MENU, self.on_new_advanced_session, new_advanced_session)
			self.menu_bar.Append(self.new_menu, "new")

			self.open_menu = wx.Menu()
			dialog_window = self.open_menu.Append(wx.ID_ANY, f"dialog window")
			self.Bind(wx.EVT_MENU, self.on_dialog_window, dialog_window)
			session_manager = self.open_menu.Append(wx.ID_ANY, 'session manager')
			self.Bind(wx.EVT_MENU, self.on_session_manager, session_manager)
			self.menu_bar.Append(self.open_menu, "open")

			self.settings_menu = wx.Menu()
			enable_clipboard_listener = self.settings_menu.Append(wx.ID_ANY,
			                                                      f'toggle clipboard listener\t{config.hotkey_toggle_listen_clipboard_change}')
			self.Bind(wx.EVT_MENU, self.on_toggle_clipboard_listener, enable_clipboard_listener)
			self.settings_menu.AppendSeparator()
			preferences = self.settings_menu.Append(wx.ID_ANY, "preferences")
			self.Bind(wx.EVT_MENU, self.on_preferences, preferences)
			shortcut_settings = self.settings_menu.Append(wx.ID_ANY, "shortcut settings")
			self.Bind(wx.EVT_MENU, self.on_preferences, shortcut_settings)
			self.menu_bar.Append(self.settings_menu, "settings")

			self.about_menu = wx.Menu()
			about = self.about_menu.Append(wx.ID_ANY, "about")
			self.Bind(wx.EVT_MENU, self.on_about, about)
			github = self.about_menu.Append(wx.ID_ANY, "GitHub project page")
			self.Bind(wx.EVT_MENU, self.on_github, github)
			self.menu_bar.Append(self.about_menu, "help")

		set_menu_bar()
		"""
		        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('R'), refreshMenuItem.GetId()),
                                              (wx.ACCEL_ALT, ord('X'), xit_id),
                                              (wx.ACCEL_SHIFT|wx.ACCEL_ALT, ord('Y'), yit_id)
                                             ])
        self.SetAcceleratorTable(self.accel_tbl)
		"""

	#
	# main_text = wx.StaticText(self, '')

	def on_exit(self, event=None):
		x = message_dialog("Exiting meowencrypt will lost all established sessions, and the content will be impossible to decrypt. Do you want to do so?", "warning").show()
		if x:
			self.Destroy()
			os.abort()

	@staticmethod
	def on_new_session(event=None):
		auto_new_session()

	@staticmethod
	def on_new_advanced_session(event=None):
		message_box(
			'this feature is messing. You should wait for the official release of the beta version to use this feature.',
			'error').show()

	@staticmethod
	def on_toggle_clipboard_listener(event=None):
		toggle_listen_clipboard()

	@staticmethod
	def on_preferences(event=None):
		settings_UI_show()

	@staticmethod
	def on_shortcut_settings(event=None):
		message_box(
			'this feature is messing. You should wait for the official release of the beta version to use this feature.',
			'error').show()

	def on_dialog_window(self, event=None):
		show_UI(session_UI)
		# session_UI_show()

	def on_session_manager(self, event=None):
		show_UI(session_manager_UI)
		# session_manager_UI_show()

	def on_github(self, event=None):
		webbrowser.open("https://github.com/level-128/meowencrypt")

	def on_about(self, event=None):
		about = message_box('Created by level-128 and other contributors\n'
		                    'Meowencrypt is a real-time end-to-end encryption software which encodes encrypted data into printable characters\n\n'
		                    "COPYRIGHT NOTICE:\nmeowencrypt  Copyright (C) 2021  level-128\n\n"
		                    "This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under "
		                    "certain conditions:\n\n"

		                    "The software Meowencrypt is licensed under GPL-3.0 (GNU General Public License 3.0) and LGPL-3.0 (GNU Lesser General "
		                    "Public License 3.0) depends on different parts of the program. Both licences are provided in /document folder.\n\n"

		                    "All the codes under meowencrypt/enclib are licensed under LGPL-3.0, while the rest of the program is licensed under "
		                    "GPL-3.0.\n\n"

		                    "The purpose for using different licenses for different parts of this software is because codes in folder "
		                    "meowencrypt/enclib may be used in other independent projects. These codes implement Diffie-Hellman key exchange "
		                    "algorithm and multi-session key support that might be useful in other scenarios. GNU GPL is a strong copyleft license "
		                    "that may, in my opinion, hinders the free-software development when other programmers founded that their work must be "
		                    "open-sourced under GPL, which they may not intended to do so.\n\n"

		                    "As a programming hobbyist, I hope I could respect users' and developers' freedom. While GNU GPL ensures freedom for "
		                    "all entities, it does not ensure the software is fully utilized and disseminated.\n\n"

		                    "You should have received copies of the GNU General Public License and GNU Lesser General Public License along with this"
		                    " program.  If not, see <https://www.gnu.org/licenses/>.",
		                    f'About: Meowencrypt        --version {VERSION}', width=700)
		about.show()
