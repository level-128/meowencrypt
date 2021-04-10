import pyperclip
from plyer import notification

_is_ignore_last_clipboard: bool = False

_last_push_clipboard_content: str = ''


class EvtNotification(Exception):
	def __init__(self, *, content_to_clipboard: str = '', content_to_notification: str = '', notification_title: str = ''):
		self.content_to_clipboard = content_to_clipboard
		self.content_to_notification = content_to_notification
		super(EvtNotification, self).__init__("this event has not been handled")

		if self.content_to_notification:
			notification.notify(title=notification_title if notification_title else 'note: ',
			                    message=self.content_to_notification
			                    )
		if self.content_to_clipboard:
			global _is_ignore_last_clipboard
			_is_ignore_last_clipboard = True
			pyperclip.copy(self.content_to_clipboard)


def push_notification(content_to_notification: str, notification_title: str = ''):
	notification.notify(title=notification_title if notification_title else 'note: ',
	                    message=content_to_notification
	                    )


def push_clipboard(content_to_clipboard: str):
	if content_to_clipboard != _last_push_clipboard_content:
		global _is_ignore_last_clipboard
		_is_ignore_last_clipboard = True
		pyperclip.copy(content_to_clipboard)


def get_clipboard() -> str:
	return pyperclip.paste()


def get_last_pasted_item() -> str:
	return _last_push_clipboard_content


def is_ignore_last_clipboard():
	global _is_ignore_last_clipboard
	if _is_ignore_last_clipboard:
		_is_ignore_last_clipboard = False
		return True
	return False