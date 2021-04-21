from typing import List, Union

import wx


class notification(wx.Frame):

	def __init__(self, title: str = "notification"):
		self.app = wx.App()
		super().__init__(None, title=title)
		self.x_axis_accumulator: int = 20
		self.input_boxes: list[Union[wx.ComboBox, wx.TextCtrl, wx.CheckBox]] = []

	def set_input_box(self, label: str = ''):
		if label:
			wx.StaticText(self, label = label, pos = (self.x_axis_accumulator, -1))
			self.x_axis_accumulator += 25
		self.input_boxes.append(wx.TextCtrl(self, size = (200, 22), pos = (self.x_axis_accumulator, 20)))
		self.x_axis_accumulator += 40

	def on_button(self, event):
		self.app.ExitMainLoop()

	def show(self) -> List[Union[bool, str]]:
		btn = wx.Button(self, label='OK', size = (70, 30), pos=(self.x_axis_accumulator, 30))
		btn.Bind(wx.EVT_BUTTON, self.on_button)
		self.Show()
		self.app.MainLoop()
		return [ _.GetValue() for _ in self.input_boxes]


if __name__ == "__main__":
	_ = notification()
	_.set_input_box('hello')
	print(_.show())
