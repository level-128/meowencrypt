import threading

import wx

from runlib.enc_session_manager import get_active_sessions

from time import localtime, strftime


class session_manager(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title = "session manager", size = (400, 400))
		self.Bind(wx.EVT_SET_FOCUS, self.refresh)

		def set_menu_bar():
			self.menu_bar = wx.MenuBar()
			self.SetMenuBar(self.menu_bar)

			self.refresh_menu = wx.Menu()
			# self.refresh_menu.Bind()
			self.menu_bar.Append(self.refresh_menu, "&refresh")
			self.menu_bar.Bind(wx.EVT_MENU_OPEN, self.refresh)

		self.list = wx.ListCtrl(self, -1, style = wx.LC_REPORT)

		self.list.InsertColumn(0, "")
		self.list.InsertColumn(1, "ID")
		self.list.InsertColumn(2, "established")
		self.list.InsertColumn(3, "time")

		self.list.SetColumnWidth(0, 40)
		self.list.SetColumnWidth(1, 80)
		self.list.SetColumnWidth(2, 100)
		self.list.SetColumnWidth(3, 150)

		set_menu_bar()

	def refresh(self, event: None):
		print("refresh")
		self.list.DeleteAllItems()
		for index, _ in enumerate(get_active_sessions()):
			session_ID, is_established, time = _
			self.list.InsertItem(index, str(index))
			self.list.SetItem(index, 1, str(session_ID))
			self.list.SetItem(index, 2, str(is_established))
			self.list.SetItem(index, 3, strftime("%m/%d %H:%M:%S", localtime(time)))


def session_manager_show():
	session_manager_frame = session_manager()
	session_manager_frame.Show()
