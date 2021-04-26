import wx

from UI.message import message_box
from UI.session_UI import show as session_UI_show
from UI.session_manager_UI import show as session_manager_UI_show
from UI.settings_UI import show as settings_UI_show
from UI.theme_setter import set_color
from config.config_library import config
from runlib.enc_session_manager import new_session
from runlib.pushed_content import EvtNotification
import webbrowser

class main_UI(wx.Frame):

	def _conv(self, x, y = 0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def __init__(self):
		super().__init__(None, title='session frame', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		set_color(self, True)

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
			enable_clipboard_listener = self.settings_menu.AppendCheckItem(wx.ID_ANY, f'enable clipboard listener\t{config.hotkey_toggle_listen_clipboard_change}')
			self.Bind(wx.EVT_MENU, self.on_enable_clipboard_listener, enable_clipboard_listener)
			self.settings_menu.AppendSeparator()
			preferences = self.settings_menu.Append(wx.ID_ANY, "preferences")
			self.Bind(wx.EVT_MENU, self.on_preferences, preferences)
			shortcut_settings = self.settings_menu.Append(wx.ID_ANY, "shortcut settings")
			self.Bind(wx.EVT_MENU, self.on_preferences, shortcut_settings)
			self.menu_bar.Append(self.settings_menu, "settings")

			self.about_menu = wx.Menu()
			self.menu_bar.Append(self.about_menu, "about")
			self.about_menu.Bind(wx.EVT_MENU, self.on_about)

		set_menu_bar()

	# self.Fit( )

	def on_new_session(self, event = None):
		try:
			new_session()
		except EvtNotification as e:
			pass



	def on_new_advanced_session(self, event = None):
		message_box('this feature is messing. You should wait for the official release of the beta version to use this feature.', 'error').show()

	def on_enable_clipboard_listener(self, event = None):
		message_box('this feature is messing. You should wait for the official release of the beta version to use this feature.', 'error').show()

	def on_preferences(self, event=None):
		settings_UI_show()

	def on_shortcut_settings(self, event=None):
		message_box('this feature is messing. You should wait for the official release of the beta version to use this feature.', 'error').show()

	def on_dialog_window(self, event=None):
		session_UI_show()

	def on_session_manager(self, event=None):
		session_manager_UI_show()

	def on_about(self, event=None):
		webbrowser.open("https://github.com/level-128/meowencrypt")



def show():
	main_UI_frame = main_UI()
	main_UI_frame.Show()


if __name__ == '__main__':
	app = wx.App()
	show()
	app.MainLoop()
