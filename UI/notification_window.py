from typing import List, Union
from UI.theme_setter import detect_darkmode, set_color

import wx


class notification(wx.Frame):

	def __init__(self, title: str = "notification", width: int = 280):
		self.app = wx.App( )
		super( ).__init__(None, style=wx.MINIMIZE_BOX | wx.CLOSE_BOX)
		self.Bind(wx.EVT_CLOSE, self.on_cancel)
		self.y_axis_accumulator: int = 40
		self.input_boxes: list[Union[wx.ComboBox, wx.TextCtrl, wx.CheckBox]] = []
		self.width = width
		self.return_ = None
		self.is_dark_mode = detect_darkmode( )
		set_color(self, True)

		font = self.GetFont( ).Scale(1.3)
		_ = wx.StaticText(self, label=title + ':', pos=self._conv(5, 5))
		_.Wrap(self._conv(self.width - 10))
		_.SetFont(font)
		set_color(_, False, False)

	def _conv(self, x, y = 0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def set_input_box(self, label: str = '', is_inline: bool = True):
		if label:
			if is_inline:
				_ = wx.StaticText(self, label=label + ':', pos=self._conv(10, self.y_axis_accumulator + 2))
				set_color(_, False, False)
				text_size = self.ToDIP(_.GetSize( )[0])
				self.input_boxes.append(_ := wx.TextCtrl(self, size=self._conv(self.width - 25 - text_size, 22), pos=self._conv(text_size + 15, self.y_axis_accumulator)))
			else:
				_ = wx.StaticText(self, label=label + ':', pos=self._conv(10, self.y_axis_accumulator), size=self._conv(self.width - 10, -1))
				self.y_axis_accumulator += 22
				set_color(_, False, False)
				self.input_boxes.append(_ := wx.TextCtrl(self, size=self._conv(self.width - 35, 22), pos=self._conv(30, self.y_axis_accumulator)))
		else:
			self.input_boxes.append(_ := wx.TextCtrl(self, size=self._conv(self.width - 20, 22), pos=self._conv(15, self.y_axis_accumulator)))
		set_color(_, True)
		set_color(_, False, False)
		self.y_axis_accumulator += 45

	def set_static_text(self, label: str):
		_ = wx.StaticText(self, label=label, pos=self._conv(10, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self._conv(self.width - 15))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize( )[1])

	def set_checkbox(self, label: str):
		self.input_boxes.append(wx.CheckBox(self, pos=self._conv(10, self.y_axis_accumulator)))
		_ = wx.StaticText(self, label=label, pos=self._conv(30, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self._conv(self.width - 35))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize( )[1])

	def on_ok(self, event):
		self.return_ = [_.GetValue( ) for _ in self.input_boxes]
		self.app.ExitMainLoop( )
		self.Destroy( )

	def on_cancel(self, event):
		self.app.ExitMainLoop( )
		self.Destroy( )

	def show(self) -> Union[List[Union[bool, str]], None]:
		self.y_axis_accumulator += 3
		ok_btn = wx.Button(self, label='OK', size=self._conv(int(self.width * 0.35), 30), pos=self._conv(15, self.y_axis_accumulator))
		cancel_btn = wx.Button(self, label='cancel', size=self._conv(int(self.width * 0.35), 30), pos=self._conv(self.width - 15 - int(self.width * 0.35), self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
		set_color(ok_btn, False, False)
		set_color(cancel_btn, False, False)
		set_color(ok_btn, True, True)
		set_color(cancel_btn, True, True)
		self.Fit( )
		x, y = self.GetSize( )
		_ = self._conv(10)
		self.SetSize(x + _, y + _)
		self.Center( )
		self.Show( )
		self.app.MainLoop( )
		return self.return_


if __name__ == "__main__":
	_ = notification( )
	_.set_static_text('this is a example this is a example this is a example this is a example this is a example this is a example this is a example this is a example this is a '
	                  'example this is a example this is a example this is a example this is a example this is a example ')

	_.set_checkbox("roe3hfuirehof regfhreghouireghoui rehgouirehgui")
	_.set_input_box('f')
	print(_.show( ))
