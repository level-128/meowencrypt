import platform
from abc import ABCMeta, abstractmethod
from typing import List, Union
from UI.theme_setter import detect_darkmode, set_color

import wx


class NotificationError(Exception):
	def __init__(self):
		super(NotificationError, self).__init__("you can't create input content if you choose not to block the thread.")


class __message_frame(wx.Frame):
	__metaclass__ = ABCMeta

	def __init__(self, width: int):
		if not wx.App.GetInstance( ):
			self.app = wx.App( )
		else:
			self.app = wx.App.GetInstance()
		super( ).__init__(None, style=0)
		self.Bind(wx.EVT_CLOSE, self.on_cancel)
		self.y_axis_accumulator: int = 40
		self.width = width
		self.is_dark_mode = detect_darkmode( )
		set_color(self, True)

	def conv(self, x, y = 0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def on_cancel(self, event):
		self.app.ExitMainLoop( )
		self.Destroy( )

	@abstractmethod
	def on_ok(self, *args) -> None:
		...

	@abstractmethod
	def set_static_text(self, *args) -> None:
		...

	def show(self) -> None:
		self.Center( )
		self.Show( )
		self.app.MainLoop( )


class message_box(__message_frame):

	def __init__(self, title: str = "notification", *, width: int = 400):
		super( ).__init__(width)
		self.SetWindowStyle(wx.CLOSE_BOX | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.CAPTION)
		self.SetTitle(title)

	def show(self):
		self.SetSize(self.conv(500, 200))
		super().show()



class message_dialog(__message_frame):
	...


class message_window(__message_frame):

	def __init__(self, title: str = "notification", *, width: int = 280):
		super( ).__init__(width)
		self.input_boxes: list[Union[wx.ComboBox, wx.TextCtrl, wx.CheckBox]] = []
		self.return_ = None

		font = self.GetFont( ).Scale(1.3)
		_ = wx.StaticText(self, label=title + ':', pos=self.conv(5, 5))
		_.Wrap(self.conv(self.width - 10))
		_.SetFont(font)
		set_color(_, False, False)

	def set_input_box(self, label: str = '', is_inline: bool = True):
		if label:
			if is_inline:
				_ = wx.StaticText(self, label=label + ':', pos=self.conv(10, self.y_axis_accumulator + 2))
				set_color(_, False, False)
				text_size = self.ToDIP(_.GetSize( )[0])
				self.input_boxes.append(_ := wx.TextCtrl(self, size=self.conv(self.width - 25 - text_size, 22), pos=self.conv(text_size + 15, self.y_axis_accumulator)))
			else:
				_ = wx.StaticText(self, label=label + ':', pos=self.conv(10, self.y_axis_accumulator), size=self.conv(self.width - 10, -1))
				self.y_axis_accumulator += 22
				set_color(_, False, False)
				self.input_boxes.append(_ := wx.TextCtrl(self, size=self.conv(self.width - 30, 22), pos=self.conv(20, self.y_axis_accumulator)))
		else:
			self.input_boxes.append(_ := wx.TextCtrl(self, size=self.conv(self.width - 20, 22), pos=self.conv(15, self.y_axis_accumulator)))
		set_color(_, True)
		set_color(_, False, False)
		self.y_axis_accumulator += 45

	def set_static_text(self, label: str):
		_ = wx.StaticText(self, label=label, pos=self.conv(10, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self.conv(self.width - 5))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize( )[1])

	def set_checkbox(self, label: str, /, default: bool = False):
		checkbox = wx.CheckBox(self, pos=self.conv(10, self.y_axis_accumulator))
		checkbox.SetValue(default)
		self.input_boxes.append(checkbox)
		_ = wx.StaticText(self, label=label, pos=self.conv(30, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self.conv(self.width - 35))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize( )[1])

	def on_ok(self, event):
		self.return_ = [_.GetValue( ) for _ in self.input_boxes]
		self.app.ExitMainLoop( )
		self.Destroy( )

	def show(self) -> Union[List[Union[bool, str]], None]:
		self.y_axis_accumulator += 3
		ok_btn = wx.Button(self, label='OK', size=self.conv(int(self.width * 0.35), 30), pos=self.conv(15, self.y_axis_accumulator))
		cancel_btn = wx.Button(self, label='cancel', size=self.conv(round(self.width * 0.35), 30), pos=self.conv(self.width - 5 - round(self.width * 0.35),
		                                                                                                         self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
		set_color(ok_btn, False, False)
		set_color(cancel_btn, False, False)
		set_color(ok_btn, True, True)
		set_color(cancel_btn, True, True)
		self.Fit( )
		x, y = self.GetSize( )
		_ = self.conv(10)
		self.SetSize(x + _, y + _)
		super().show()
		return self.return_


if __name__ == "__main__":
	if platform.system( ) == 'Windows':
		import ctypes


		ctypes.windll.shcore.SetProcessDpiAwareness(1)

	message_box().show()

	my_notification = message_window(width=320)
	my_notification.set_static_text('this is a example of using message dialog to display static text. This text is too long, so the message dialog will wrap the line and '
	                                'auto-adjust other contents\' position based on the length of the text. ')
	my_notification.set_checkbox("is dark mode", detect_darkmode( ))
	my_notification.set_input_box('input box')
	my_notification.set_input_box('input box with a long description')
	my_notification.set_input_box('input box with a very very long description', False)
	# the method will block the thread until the user responds the message dialog. return None of user click cancel or close box. return all the
	# contents with default sequence if the user click OK button.
	print(my_notification.show( ))
