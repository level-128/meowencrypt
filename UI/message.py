from abc import ABCMeta, abstractmethod
from typing import List, Union

import wx

from UI.theme_setter import detect_darkmode, set_color


class _message_frame(wx.Frame):
	__metaclass__ = ABCMeta
	y_axis_accumulator: int = 5

	def __init__(self, width: int, title: str):
		self.width = width
		self.app = wx.App.GetInstance( )
		super( ).__init__(None, style=0)
		self.Bind(wx.EVT_CLOSE, self.on_cancel)
		set_color(self, True)
		self.panel = wx.ScrolledWindow(self)
		set_color(self.panel, True)

		if title:
			font = self.GetFont( ).Scale(1.4)
			_ = wx.StaticText(self.panel, label=title, pos=self.conv(10, self.y_axis_accumulator), size=(self.width - 15, -1))
			_.Wrap(self.conv(self.width - 25))
			_.SetFont(font)
			set_color(_, False, False)
			self.y_axis_accumulator += 35

		self.return_ = None

	def conv(self, x, y = 0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def on_cancel(self, event):
		self.app.ExitMainLoop( )
		self.Destroy( )

	@abstractmethod
	def on_ok(self, event):
		...

	def set_static_text(self, label: str):
		_ = wx.StaticText(self.panel, label=label, pos=self.conv(10, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self.conv(self.width - 17))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize( )[1])

	def show(self) -> None:
		if self.y_axis_accumulator > 520:
			self.panel.SetScrollbars(-1, self.conv(10), -1, self.conv(self.y_axis_accumulator // 10))
			self.SetSize(wx.Size(self.conv(self.width + 35), self.conv(500)))
		else:
			self.SetSize(wx.Size(self.conv(self.width + 15), self.conv(self.y_axis_accumulator)))
		self.Center( )
		self.Show( )
		print(self.GetSize())
		if not isinstance(self, message_box):
			self.app.MainLoop( )
			return self.return_


class message_box(_message_frame):
	def __init__(self, content, title, *, width = 500):
		super(message_box, self).__init__(width, title)
		self.SetWindowStyle(wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.FRAME_TOOL_WINDOW)

		self.set_static_text(content)

		self.SetSize(self.conv(self.width, self.y_axis_accumulator + 50))

		ok_btn = wx.Button(self.panel, label='OK', size=self.conv(200, 30), pos=self.conv(self.width - 220, self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		set_color(ok_btn, True, True)
		set_color(ok_btn, False, False)

		self.y_axis_accumulator += 45

	def on_ok(self, event):
		self.Destroy()


class message_dialog(_message_frame):

	def __init__(self, content, title, *, width = 500):
		super(message_dialog, self).__init__(width, title)
		self.SetWindowStyle(wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.FRAME_TOOL_WINDOW)

		self.set_static_text(content)

		self.SetSize(self.conv(self.width, self.y_axis_accumulator + 50))
		ok_btn = wx.Button(self.panel, label='OK', size=self.conv(140, 30), pos=self.conv(self.width - 155, self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		set_color(ok_btn, True, True)
		set_color(ok_btn, False, False)

		self.SetSize(self.conv(self.width, self.y_axis_accumulator + 50))
		ok_btn = wx.Button(self.panel, label='cancel', size=self.conv(140, 30), pos=self.conv(self.width - 305, self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
		set_color(ok_btn, True, True)
		set_color(ok_btn, False, False)

		self.y_axis_accumulator += 45

	def on_ok(self, event):
		self.return_ = True
		self.on_cancel(None)


class message_window(_message_frame):

	def __init__(self, title: str = "", *, width: int = 280):
		super( ).__init__(width, '')
		self.SetWindowStyle(wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
		self.SetTitle(title)
		self.input_boxes: list[Union[wx.ComboBox, wx.TextCtrl, wx.CheckBox]] = []

	def set_input_box(self, label: str = '', is_inline: bool = True):
		if label:
			if is_inline:
				_ = wx.StaticText(self.panel, label=label + ':', pos=self.conv(10, self.y_axis_accumulator + 2))
				set_color(_, False, False)
				text_size = self.ToDIP(_.GetSize( )[0])
				self.input_boxes.append(_ := wx.TextCtrl(self.panel, size=self.conv(self.width - 30 - text_size, 22), pos=self.conv(text_size + 15, self.y_axis_accumulator)))
			else:
				_ = wx.StaticText(self.panel, label=label + ':', pos=self.conv(10, self.y_axis_accumulator), size=self.conv(self.width - 10, -1))
				self.y_axis_accumulator += 22
				set_color(_, False, False)
				self.input_boxes.append(_ := wx.TextCtrl(self.panel, size=self.conv(self.width - 30, 22), pos=self.conv(15, self.y_axis_accumulator)))
		else:
			self.input_boxes.append(_ := wx.TextCtrl(self.panel, size=self.conv(self.width - 35, 22), pos=self.conv(15, self.y_axis_accumulator)))
		set_color(_, True)
		set_color(_, False, False)
		self.y_axis_accumulator += 45

	def set_checkbox(self, label: str, /, default: bool = False):
		checkbox = wx.CheckBox(self.panel, pos=self.conv(10, self.y_axis_accumulator))
		checkbox.SetValue(default)
		self.input_boxes.append(checkbox)
		_ = wx.StaticText(self.panel, label=label, pos=self.conv(30, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self.conv(self.width - 40))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize( )[1])

	def on_ok(self, event):
		self.return_ = [_.GetValue( ) for _ in self.input_boxes]
		self.app.ExitMainLoop( )
		self.Destroy( )

	def show(self) -> Union[List[Union[bool, str]], None]:
		self.y_axis_accumulator += 3
		ok_btn = wx.Button(self.panel, label='OK', size=self.conv(int(self.width * 0.35), 30), pos=self.conv(15, self.y_axis_accumulator))
		cancel_btn = wx.Button(self.panel, label='cancel', size=self.conv(round(self.width * 0.35), 30), pos=self.conv(self.width - 15 - round(self.width * 0.35), self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
		set_color(ok_btn, False, False)
		set_color(cancel_btn, False, False)
		set_color(ok_btn, True, True)
		set_color(cancel_btn, True, True)

		self.y_axis_accumulator += 80

		return super( ).show( )


def main():
	if message_dialog('press ok to show a message box, cancel to show a message window', 'test').show( ):
		message_box('test', 'test msgbox ok').show()
		print('not blocking the thread')
	else:
		my_notification = message_window(width=320, title='hello')
		my_notification.set_static_text(
			'this is a example of using message dialog to display static text. This text is too long, so the message dialog will wrap the line and '
			'auto-adjust other contents\' position based on the length of the text. ')
		my_notification.set_checkbox("is dark mode", detect_darkmode())
		my_notification.set_input_box('input box')
		my_notification.set_input_box('input box with a long description')
		my_notification.set_input_box('input box with a very very long description', False)
		# the method will block the thread until the user responds the message dialog. return None of user click cancel or close box. return all the
		# contents with default sequence if the user click OK button.
		print(my_notification.show())


if __name__ == "__main__":
	import platform
	if platform.system() == 'Windows':
		import ctypes

		ctypes.windll.shcore.SetProcessDpiAwareness(0)
	app = wx.App()
	main()
	app.MainLoop()



