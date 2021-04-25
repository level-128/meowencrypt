import wx

from enclib.enc_session import ContentError
from runlib.enc_session_manager import auto_process, encrypt_content, NullSessionError, SessionLimitExceedError, to_session
from runlib.pushed_content import EvtNotification, push_clipboard
from UI.theme_setter import set_color
from UI.message import message_box, message_window, message_dialog


class session_UI(wx.Frame):

	def _conv(self, x, y = 0):
		return (self.FromDIP(x), self.FromDIP(y)) if y else self.FromDIP(x)

	def __init__(self):
		super( ).__init__(None, title='session frame', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		set_color(self, True)

		self.input_tc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=self._conv(400, 200), pos=(0, 0))
		self.input_tc.Bind(wx.EVT_TEXT_ENTER, self.on_input_tc)
		self.input_tc.Bind(wx.EVT_TEXT, self.neg_set_enter_btn)
		set_color(self.input_tc, True)
		set_color(self.input_tc, False, False)

		self.process_btn = wx.Button(self, label='enter', size=self._conv(180, 22), pos=self._conv(5, 205))
		self.process_btn.Bind(wx.EVT_BUTTON, self.on_input_tc)
		set_color(self.process_btn, True, True)
		set_color(self.process_btn, False, False)

		self.text01 = wx.StaticText(self, label='choose mode:', pos=self._conv(200, 210), style=wx.RIGHT)
		set_color(self.text01, False, False)

		self.mode_combobox_choices = ["all", "encrypt", "receive"]
		self.mode_combobox = wx.ComboBox(self, choices=self.mode_combobox_choices, value="all", size=self._conv(100, 30), pos=self._conv(295, 205))
		set_color(self.mode_combobox, True, True)
		set_color(self.mode_combobox, False, False)

		self.output_tc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL, size=self._conv(400, 200), pos=self._conv(0, 234))
		set_color(self.output_tc, True)
		set_color(self.output_tc, False, False)

		self.Fit( )

	def set_enter_btn(self):
		self.process_btn.SetLabelText("copy content to clipboard")
		self.process_btn.Bind(wx.EVT_BUTTON, self.to_clipboard)

	def neg_set_enter_btn(self, event):
		self.process_btn.SetLabelText('enter')
		self.process_btn.Bind(wx.EVT_BUTTON, self.on_input_tc)

	def to_clipboard(self, event):
		push_clipboard(self.output_tc.GetValue( ))

	def on_input_tc(self, event):
		self.process_btn.SetFocus( )

		if self.mode_combobox.GetValue( ) == self.mode_combobox_choices[0]:
			try:
				auto_process(self.input_tc.GetValue( ))
			except EvtNotification as e:
				self.output_tc.Clear( )
				self.output_tc.WriteText(e.content_to_clipboard)
				message_box(e.content_to_notification, e.notification_title).show()
				if e.content_to_clipboard:
					self.set_enter_btn( )
			except (SessionLimitExceedError, NullSessionError) as e:
				message_box(str(e), 'error').show()
				# wx.MessageBox(str(e), "error", wx.OK | wx.ICON_ERROR)

		elif self.mode_combobox.GetValue( ) == self.mode_combobox_choices[1]:
			try:
				encrypt_content(self.input_tc.GetValue( ))
			except EvtNotification as e:
				self.output_tc.Clear( )
				self.output_tc.WriteText(e.content_to_clipboard)
				if e.content_to_clipboard:
					self.set_enter_btn( )
			except NullSessionError as e:
				message_box(str(e), 'error').show()
				# wx.MessageBox(str(e), "error", wx.OK | wx.ICON_ERROR)

		else:
			try:
				to_session(self.input_tc.GetValue( ))
			except EvtNotification as e:
				self.output_tc.Clear( )
				self.output_tc.WriteText(e.content_to_clipboard)
				message_box(e.content_to_notification, e.notification_title).show()
				if e.content_to_clipboard:
					self.set_enter_btn( )
			except (SessionLimitExceedError, NullSessionError, ContentError) as e:
				message_box(str(e), 'error').show()
				# wx.MessageBox(str(e), "error", wx.OK | wx.ICON_ERROR)


def show( ):
	session_UI_frame = session_UI( )
	session_UI_frame.Show( )
