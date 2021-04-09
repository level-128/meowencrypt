from enclib.enc_session import encryption, ContentError, CONST_NEW_SESSION_NOTATION, CONST_MSG_NOTATION, CONST_KEY_EXCHANGE_NOTATION
from runlib.notification import EvtNotification
import pyperclip

from time import time
from typing import *


active_session: Dict[str, encryption] = {}
active_session_time: Dict[str, float] = {}
last_session: str = ''


class NullSessionError(Exception):
	def __init__(self):
		super(NullSessionError, self).__init__("the message does not belong to any session.")


def __add_session(session_instance: encryption):
	active_session[session_instance.get_session_id( )] = session_instance
	active_session_time[session_instance.get_session_id( )] = time( )


def __get_session(session_ID: str) -> encryption:
	global last_session
	if session_ID in active_session:
		active_session_time[session_ID] = time( )
		last_session = session_ID
		return active_session[session_ID]
	raise NullSessionError


def to_session(content: str) -> None:
	"""
	enters a message and determine the right session to process the message
	:param content: the message from either clipboard or input box.
	:raise enclib.enc_session.ContentError: the content of the message is incorrect.
	:raise NullSessionError: the message does not belong to any session.
	:raise EvtPushToClipboard: push the EvtPushToClipboard().content into the clipboard.
	:raise ContentError: When the input content could not be parsed.
	"""
	if not content.isascii( ):
		raise ContentError
	content = content.replace('\n', '').replace('\t', '').lstrip( ).rstrip( )
	if len(content) < 3:
		raise ContentError

	#  not starting a new session
	if content[0] == CONST_MSG_NOTATION:
		session_ = __get_session(content[1:4])
		raise EvtNotification(content_to_notification=session_.decrypt_content(content))

	#  starting a new session
	elif content[0] == CONST_NEW_SESSION_NOTATION:
		session_ = encryption( )
		session_.receive_session_request(content)
		__add_session(session_)
		raise EvtNotification(content_to_clipboard=session_.create_session_request( ),
		                      content_to_notification='received a new session request. paste the session key change request to the sender.')

	elif content[0] == CONST_KEY_EXCHANGE_NOTATION:
		session_ = __get_session(content[1:4])
		session_.receive_session_request(content)
		raise EvtNotification(content_to_notification="the session has been established, start sending messages. ")

	else:
		raise ContentError


def to_session_from_clipboard():
	return to_session(pyperclip.paste( ))


def new_session() -> None:
	session_ = encryption( )
	session_request = session_.create_session_request( )
	__add_session(session_)
	raise EvtNotification(content_to_clipboard=session_request,
	                      content_to_notification="session request has been created.")


def encrypt_content(content: str, session_id: Union[str, None] = None) -> None:
	"""

	:param content:
	:param session_id:
	:return:
	:raise NullSessionError: if the session does not exist.
	"""
	if not session_id:
		session_id = last_session
	print(session_id, __get_session(session_id))
	raise EvtNotification(content_to_clipboard=__get_session(session_id).encrypt_content(content))


def get_last_session() -> str:
	return last_session