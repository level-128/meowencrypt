import threading

import wx

from enclib.enc_session import ContentError
from runlib.enc_session_manager import SessionLimitExceedError, NullSessionError, auto_process, encrypt_content, \
    to_session
from runlib.pushed_content import push_clipboard, EvtNotification


class session_UI_frame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='session frame')
        self.SetSize((416, 473))
        self.SetMaxSize((416, 473))
        self.SetMinSize((416, 473))

        self.input_tc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, size=(400, 200), pos=(0, 0))
        self.input_tc.Bind(wx.EVT_TEXT_ENTER, self.on_input_tc)
        self.input_tc.Bind(wx.EVT_SET_FOCUS, self.neg_set_enter_btn)

        self.process_btn = wx.Button(self, label='enter', size=(180, 22), pos=(5, 205))
        self.process_btn.Bind(wx.EVT_BUTTON, self.on_input_tc)

        self.text01 = wx.StaticText(self, label='choose mode:', pos=(200, 210), style=wx.RIGHT)

        self.mode_combobox_choices = ["all", "encrypt", "receive"]
        self.mode_combobox = wx.ComboBox(self, choices=self.mode_combobox_choices, value="all", size=(100, 30),
                                         pos=(295, 205))

        self.output_tc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(400, 200), pos=(0, 234))

    def set_enter_btn(self):
        self.process_btn.SetLabelText("copy content to clipboard")
        self.process_btn.Bind(wx.EVT_BUTTON, self.to_clipboard)

    def neg_set_enter_btn(self, event):
        self.process_btn.SetLabelText('enter')
        self.process_btn.Bind(wx.EVT_BUTTON, self.on_input_tc)

    def to_clipboard(self, event):
        push_clipboard(self.output_tc.GetValue())

    def on_input_tc(self, event):
        self.process_btn.SetFocus()

        if self.mode_combobox.GetValue() == self.mode_combobox_choices[0]:
            try:
                auto_process(self.input_tc.GetValue())
            except EvtNotification as e:
                self.output_tc.Clear()
                self.output_tc.WriteText(e.content_to_clipboard)
                wx.MessageBox(e.content_to_notification, e.notification_title)
                if e.content_to_clipboard:
                    self.set_enter_btn()
            except (SessionLimitExceedError, NullSessionError) as e:
                wx.MessageBox(str(e), "error", wx.OK | wx.ICON_ERROR)

        elif self.mode_combobox.GetValue() == self.mode_combobox_choices[1]:
            try:
                encrypt_content(self.input_tc.GetValue())
            except EvtNotification as e:
                self.output_tc.Clear()
                self.output_tc.WriteText(e.content_to_clipboard)
                if e.content_to_clipboard:
                    self.set_enter_btn()
            except NullSessionError as e:
                wx.MessageBox(str(e), "error", wx.OK | wx.ICON_ERROR)

        else:
            try:
                to_session(self.input_tc.GetValue())
            except EvtNotification as e:
                self.output_tc.Clear()
                self.output_tc.WriteText(e.content_to_clipboard)
                wx.MessageBox(e.content_to_notification, e.notification_title)
                if e.content_to_clipboard:
                    self.set_enter_btn()
            except (SessionLimitExceedError, NullSessionError, ContentError) as e:
                wx.MessageBox(str(e), "error", wx.OK | wx.ICON_ERROR)



def _start_session_UI():
    app = wx.App()
    my_frame = session_UI_frame()
    my_frame.Show()
    app.MainLoop()

def start_session_UI():
    thread = threading.Thread(target=_start_session_UI)
    thread.start()
