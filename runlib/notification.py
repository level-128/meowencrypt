import pyperclip
from plyer import notification

_is_ignore_last_clipboard: bool = False


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


def is_ignore_last_clipboard():
	global _is_ignore_last_clipboard
	if _is_ignore_last_clipboard:
		_is_ignore_last_clipboard = False
		return True
	return False