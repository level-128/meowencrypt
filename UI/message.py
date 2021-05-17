import ctypes
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, List, Union, Annotated, NewType

import wx
import winsound

import multiprocessing

from UI.theme_setter import detect_darkmode, set_color
from config.config_library import config

DIP = NewType('DIP', int)

SHOW = 0

CREATE_MESSAGE_BOX = 1
CREATE_MESSAGE_DIALOG = 2
CREATE_MESSAGE_WINDOW = 3

SET_STATIC_TEXT = 10
SET_INPUT_BOX = 20
SET_CHECKBOX = 30
SET_COMBOBOX = 40


def _main(pipe: multiprocessing.Pipe):
	ctypes.windll.shcore.SetProcessDpiAwareness(config.GUI_os_process_dpi_awareness)
	instance: Union[_message_window, _message_dialog, _message_box, None] = None
	for content in pipe.recv():
		type_, *content = content
		if type_ == CREATE_MESSAGE_BOX:
			instance = _message_box(*content)
		elif type_ == CREATE_MESSAGE_DIALOG:
			instance = _message_dialog(*content)
		elif type_ == CREATE_MESSAGE_WINDOW:
			instance = _message_window(*content)
		elif type_ == SET_STATIC_TEXT:
			instance.set_static_text(*content)
		elif type_ == SET_INPUT_BOX:
			instance.set_input_box(*content)
		elif type_ == SET_CHECKBOX:
			instance.set_checkbox(*content)
		elif type_ == SET_COMBOBOX:
			instance.set_combobox(*content)
		elif type_ == SHOW:
			try:
				pipe.send(instance.show())
			except BrokenPipeError:
				pass
			finally:
				pipe.close()
				break
		else:
			raise Exception


def create_window(*args):
	raise NotImplementedError("replace this function with message method.")


class __message:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.items: List[List[Union[int, Any]]] = []
		self.message_frame_pipe, self.__receive_pipe = multiprocessing.Pipe()
		self.process = multiprocessing.Process(target=_main, args=(self.__receive_pipe,))

	def show(self, is_block=True):
		self.process.start()
		self.items.append([SHOW])
		self.message_frame_pipe.send(self.items)
		if is_block:
			return_ = self.message_frame_pipe.recv()
			self.message_frame_pipe.close()
			return return_
		else:
			self.message_frame_pipe.close()

	def set_static_text(self, label: str):
		self.items.append([SET_STATIC_TEXT, label])


class message_box(__message):

	def __init__(self, content, title, width=500):
		super(message_box, self).__init__()
		self.items.append([CREATE_MESSAGE_BOX, content, title, width])

	def show(self, is_block=False):
		super().show(is_block)


class message_dialog(__message):

	def __init__(self, content, title, width=500):
		super(message_dialog, self).__init__()
		self.items.append([CREATE_MESSAGE_DIALOG, content, title, width])


class message_window(__message):

	def __init__(self, title: str = "", width: int = 300):
		super(message_window, self).__init__()
		self.items.append([CREATE_MESSAGE_WINDOW, title, width])

	def set_input_box(self, label: str = '', is_inline: bool = True, default: Any = ''):
		self.items.append([SET_INPUT_BOX, label, is_inline, default])

	def set_checkbox(self, label: str, default: bool = False):
		self.items.append([SET_CHECKBOX, label, default])

	def set_combobox(self, label: str, choices: list, default: Union[str, None] = None):
		self.items.append([SET_COMBOBOX, label, choices, default])


class _message_frame(wx.Frame):
	__metaclass__ = ABCMeta
	y_axis_accumulator: int = 5  # indicates the next element's y axis position.
	return_ = None  # the return value after the window is shown.

	def __init__(self, width: int, title: str):
		self.width = width

		self.app = wx.App()
		super().__init__(None, style=0)
		self.Bind(wx.EVT_CLOSE, self.on_cancel)
		self.panel = wx.ScrolledWindow(self)

		set_color(self, True)
		set_color(self.panel, True)

		if title:  # if the title exist, add title and move other contents down.
			font = self.GetFont().Scale(1.4)
			title_text = wx.StaticText(self.panel, label=title, pos=self.conv(10, self.y_axis_accumulator), size=(self.width - 15, -1))
			title_text.Wrap(self.conv(self.width - 25))
			title_text.SetFont(font)
			set_color(title_text, False, False)
			self.y_axis_accumulator += 35

	def conv(self, x, y=0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def on_cancel(self, event):
		self.app.ExitMainLoop()
		self.Destroy()

	@abstractmethod
	def on_ok(self, event):
		...

	def set_static_text(self, label: str):
		static_text = wx.StaticText(self.panel, label=label, pos=self.conv(10, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		static_text.Wrap(self.conv(self.width - 17))
		set_color(static_text, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(static_text.GetSize()[1])

	def show(self) -> None:
		if self.y_axis_accumulator > 520:  # add scroll bar when the y axis count is larger than 520
			self.panel.SetScrollbars(-1, self.conv(10), -1, self.conv(self.y_axis_accumulator // 10))
			self.SetSize(wx.Size(self.conv(self.width + 35), self.conv(500)))
		else:
			self.SetSize(wx.Size(self.conv(self.width + 15), self.conv(self.y_axis_accumulator)))
		self.Center()
		self.Show()
		#  play a sound when the window has shown up
		winsound.PlaySound(r'files\notification_CClicense.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
		self.app.MainLoop()
		return self.return_


class _message_box(_message_frame):
	def __init__(self, content, title, width=500):
		super(_message_box, self).__init__(width, title)
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


class _message_dialog(_message_frame):

	def __init__(self, content, title, width=500):
		super(_message_dialog, self).__init__(width, title)
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


class _message_window(_message_frame):
	input_boxes: list[Union[wx.ComboBox, wx.TextCtrl, wx.CheckBox]] = []

	def __init__(self, title: str, width: int):
		super(_message_window, self).__init__(width, '')
		self.SetWindowStyle(wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
		self.SetTitle(title)

	def set_input_box(self, label: str = '', is_inline: bool = True, default: Any = ''):
		if label:
			if is_inline:
				label_text = wx.StaticText(self.panel, label=label + ':', pos=self.conv(10, self.y_axis_accumulator + 2))
				set_color(label_text, False, False)
				text_size = self.ToDIP(label_text.GetSize()[0])  # the length of the text, in DIP
				self.input_boxes.append(label_box := wx.TextCtrl(self.panel, size=self.conv(self.width - 30 - text_size, 22), pos=self.conv(text_size + 15, self.y_axis_accumulator)))
			else:
				label_text = wx.StaticText(self.panel, label=label + ':', pos=self.conv(10, self.y_axis_accumulator), size=self.conv(self.width - 10, -1))
				self.y_axis_accumulator += 22
				set_color(label_text, False, False)
				self.input_boxes.append(label_box := wx.TextCtrl(self.panel, size=self.conv(self.width - 30, 22), pos=self.conv(15, self.y_axis_accumulator)))
		else:
			self.input_boxes.append(label_box := wx.TextCtrl(self.panel, size=self.conv(self.width - 35, 22), pos=self.conv(15, self.y_axis_accumulator)))
		set_color(label_box, True)
		set_color(label_box, False, False)
		label_box.SetValue(str(default))
		self.y_axis_accumulator += 45

	def set_checkbox(self, label: str, default: bool = False):
		checkbox = wx.CheckBox(self.panel, pos=self.conv(10, self.y_axis_accumulator))
		checkbox.SetValue(default)
		self.input_boxes.append(checkbox)
		_ = wx.StaticText(self.panel, label=label, pos=self.conv(30, self.y_axis_accumulator), style=wx.TE_MULTILINE)
		_.Wrap(self.conv(self.width - 40))
		set_color(_, False, False)
		self.y_axis_accumulator += 18 + self.ToDIP(_.GetSize()[1])

	def set_combobox(self, label: str, choices: list, default: Union[str, None] = None):
		_ = wx.StaticText(self.panel, label=label + ':', pos=self.conv(10, self.y_axis_accumulator + 2))
		set_color(_, False, False)
		text_size = self.ToDIP(_.GetSize()[0])
		combobox = wx.ComboBox(self.panel, choices=choices, value=default if default else choices[0],
		                       size=self.conv(self.width - 30 - text_size, 22), pos=self.conv(text_size + 15, self.y_axis_accumulator))
		self.input_boxes.append(combobox)
		set_color(combobox, True, True)
		set_color(combobox, False, False)
		self.y_axis_accumulator += 45

	def on_ok(self, event):
		self.return_ = [_.GetValue() for _ in self.input_boxes]
		self.app.ExitMainLoop()
		self.Destroy()

	def show(self) -> Union[List[Union[bool, str]], None]:
		self.y_axis_accumulator += 3
		ok_btn = wx.Button(self.panel, label='OK', size=self.conv(int(self.width * 0.35), 30), pos=self.conv(15, self.y_axis_accumulator))
		cancel_btn = wx.Button(self.panel, label='cancel', size=self.conv(round(self.width * 0.35), 30),
		                       pos=self.conv(self.width - 15 - round(self.width * 0.35), self.y_axis_accumulator))
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
		set_color(ok_btn, False, False)
		set_color(cancel_btn, False, False)
		set_color(ok_btn, True, True)
		set_color(cancel_btn, True, True)

		self.y_axis_accumulator += 80

		return super().show()


def test():
	if message_dialog('press ok to show a message box, cancel to show a message window', 'test').show():
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
		my_notification.set_combobox('test combobox', ['one', 'two', 'three'])
		print(my_notification.show())

