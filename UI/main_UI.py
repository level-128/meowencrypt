import wx
import threading


def start_UI(is_block: bool = False):
	from UI.session_manager_UI import session_manager
	from UI.session_UI import session_UI_frame

	def inner():
		app = wx.App()
		session_manager_frame = session_manager()
		session_manager_frame.Show()
		session_frame = session_UI_frame()
		session_frame.Show()
		app.MainLoop()

	if is_block:
		inner()
	else:
		threading.Thread(target=inner).start()

