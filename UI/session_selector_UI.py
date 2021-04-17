import wx

from time import localtime

class LibrarySys(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400, 400))

		def set_menu_bar():
			self.menu_bar = wx.MenuBar()
			self.SetMenuBar(self.menu_bar)

			self.refresh_menu = wx.Menu()
			# self.refresh_menu.Bind()
			self.menu_bar.Append(self.refresh_menu, "&refresh")




		self.list = wx.ListCtrl(self, -1, style = wx.LC_REPORT)
		self.list.InsertColumn(0, "ID")
		self.list.InsertColumn(1, "书名")
		self.list.InsertColumn(2, "添加日期")

		for index in range(3):
			self.list.InsertItem(index, hash(index))
			self.list.SetItem(index, 1, hash(index + 1))
			self.list.SetItem(index, 2, hash(index + 2))

		self.list.SetColumnWidth(0, 60)
		self.list.SetColumnWidth(1,230)
		self.list.SetColumnWidth(2, 90)

		set_menu_bar()

		self.Show()


	def refresh(self, event: None):
		self.list.SetItem(index, 1, data[0])
		self.list.SetItem(index, 2, data[1])



if __name__ == "__main__":
	app = wx.App()
	frame = LibrarySys(None, "library-system")
	app.MainLoop()