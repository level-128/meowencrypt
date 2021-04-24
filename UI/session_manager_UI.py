import threading

import wx

from runlib.enc_session_manager import get_active_sessions

from time import localtime, strftime

from UI.theme_setter import detect_darkmode, set_color


class session_manager(wx.Frame):
	def __init__(self):
		super().__init__(None, title="session manager")
		self.SetSize(self.FromDIP(wx.Size(400, 400)))
		self.Bind(wx.EVT_SET_FOCUS, self.refresh)

		def set_menu_bar( ):
			self.menu_bar = wx.MenuBar( )
			self.SetMenuBar(self.menu_bar)

			self.refresh_menu = wx.Menu( )
			# self.refresh_menu.Bind()
			self.menu_bar.Append(self.refresh_menu, "&refresh")
			self.menu_bar.Bind(wx.EVT_MENU_OPEN, self.refresh)

		self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
		set_color(self.list, True)

		self.list.InsertColumn(0, "")
		self.list.InsertColumn(1, "ID")
		self.list.InsertColumn(2, "established")
		self.list.InsertColumn(3, "time")

		self.list.SetColumnWidth(0, self.FromDIP(40))
		self.list.SetColumnWidth(1, self.FromDIP(80))
		self.list.SetColumnWidth(2, self.FromDIP(100))
		self.list.SetColumnWidth(3, self.FromDIP(150))

		if detect_darkmode():
			self.list.SetTextColour(wx.Colour(240, 240, 240))

		set_menu_bar( )

	def refresh(self, event: None):
		print("refresh")
		self.list.DeleteAllItems( )
		for index, _ in enumerate(get_active_sessions( )):
			session_ID, is_established, time = _
			self.list.InsertItem(index, str(index))
			self.list.SetItem(index, 1, str(session_ID))
			self.list.SetItem(index, 2, str(is_established))
			self.list.SetItem(index, 3, strftime("%m/%d %H:%M:%S", localtime(time)))


def show():
	session_manager_frame = session_manager( )
	session_manager_frame.Show( )
