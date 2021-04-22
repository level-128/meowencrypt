from typing import List, Union
from UI.theme_setter import detect_darkmode, set_color

import wx


class message_dialog(wx.Frame):

	def __init__(self, title: str = "notification"):
		if not wx.App.GetInstance( ):
			self.app = wx.App( )
		super( ).__init__(None, style=wx.FRAME_FLOAT_ON_PARENT)
