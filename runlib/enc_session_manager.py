from time import time
from typing import *

from config.config_library import config
from enclib.enc_session import encryption, ContentError, CONST_NEW_SESSION_NOTATION, CONST_MSG_NOTATION, \
	CONST_KEY_EXCHANGE_NOTATION  # clear import
from enclib.enc_utilities import b94encode, b94decode_to_int
from runlib.pushed_content import EvtNotification, get_clipboard  # clear import

active_session: Dict[str, encryption] = {}
active_session_time: Dict[str, float] = {}
active_session_name: Dict[str, str] = {}
last_session: str = ''

# TODO: feat: complete the function auto_process

class NullSessionError(Exception):
	def __init__(self, session_ID: str):
		super(NullSessionError, self).__init__(
			f"the message does not belongs to any session, requesting ID = {session_ID}.")


class SessionLimitExceedError(Exception):
	def __init__(self):
		super(SessionLimitExceedError, self). \
			__init__(f"the active session number has exceed the limit ({config.max_session})")


def __add_session(session_instance: encryption):
	"""
	add a session to the session manager.
	"""
	global last_session
	if len(active_session) == config.max_session:
		raise SessionLimitExceedError
	# print("add session %s, id = %s" % (session_instance, session_instance.get_session_id()))
	last_session = session_instance.get_session_id()
	active_session[session_instance.get_session_id()] = session_instance
	active_session_time[session_instance.get_session_id()] = time()


def __get_session(session_ID: str) -> encryption:
	"""
	return the session whose ID is session_ID.
	:raise NullSessionError: if the session does not exist.
	"""
	global last_session
	# print("get session id=%s" % session_ID)
	if session_ID in active_session:
		active_session_time[session_ID] = time()
		last_session = session_ID
		return active_session[session_ID]
	raise NullSessionError(session_ID)


def to_session(content: str) -> None:
	"""
	enters a message and determine the right session to process the message
	:param content: the message from either clipboard or input box.
	
	:raise EvtNotification: push the EvtPushToClipboard().content into the clipboard.
	:raise NullSessionError: the message does not belongs to any session.
	:raise ContentError: When the input content could not be parsed.
	:raise SessionLimitExceedError: When the session count exceed the limit. Raised when receive a new session request.
	"""
	if not content.isascii():
		raise ContentError
	content = content.replace('\n', '').replace('\t', '').lstrip().rstrip()
	#  all encoded message should at least contains a identification character, session id and checksum.
	#  if the content is shorter than the sum of these length, means it must not belongs to the session.
	if len(content) <= 1 + config.session_id_len + config.check_sum_len:
		raise ContentError

	notation, text = content[0], content[1:]

	#  not starting a new session
	if notation == CONST_MSG_NOTATION:
		session_ = __get_session(text[:config.check_sum_len])
		raise EvtNotification(content_to_notification = session_.decrypt_content(text))

	#  starting a new session
	elif notation == CONST_NEW_SESSION_NOTATION:
		session_ = encryption()
		session_.receive_session_request(text)
		__add_session(session_)
		raise EvtNotification(content_to_clipboard = session_.create_session_request(),
		                      content_to_notification = 'received a new session request. paste the key exchange message '
		                                                'from clipboard to the sender and then start sending messages.',
							  notification_title = 'New session request',
							  is_force_message_box = True)

	elif notation == CONST_KEY_EXCHANGE_NOTATION:
		session_ = __get_session(text[:config.session_id_len])
		session_.receive_session_request(text)
		raise EvtNotification(content_to_notification = "the session has been established, start sending messages.",
							  notification_title = 'New session request',
							  is_force_message_box = True)

	else:
		raise ContentError


def to_session_from_clipboard():
	"""
	equals to to_session(runlib.pushed_content.get_clipboard( ))
	"""
	return to_session(get_clipboard())


def new_session() -> None:
	"""
	create a new session.
	This function will create a new session triggered by the user.
	:raise EvtNotification: notification only.
	:raise SessionLimitExceedError: When the session count exceed the limit.
	"""
	session_ = encryption()
	session_request = session_.create_session_request()
	__add_session(session_)
	raise EvtNotification(content_to_clipboard = session_request,
	                      content_to_notification = "session request has been created.")


def encrypt_content(content: str, session_id: Union[int, None] = None) -> None:
	"""
	encrypt the message into encoded content
	:param content: message
	:param session_id: the session to where the message belongs. default last session's id.
	:raise NullSessionError: if the session does not exist.
	:raise EvtNotification: returns the encrypted content to the clipboard. No notification.
	"""
	if not session_id:
		session_id = last_session
	else:
		session_id = b94encode(session_id).decode()
	# print(session_id, __get_session(session_id))
	raise EvtNotification(content_to_clipboard = __get_session(session_id).encrypt_content(content))


def auto_process(content: str, session_id: Union[int, None] = None) -> None:
	"""
	auto decide the process method based on the input content.
	:param content: message
	:param session_id: the session to where the message belongs. default last session's id.
	
	:raise NullSessionError: if the session does not exist. This exception will be raised if the message could be parsed
		and checksum is correct. If the condition does not meet, the attempt will be made to encrypt this message.
	
	:raise SessionLimitExceedError: When the session count exceed the limit. Raised when receive a new session request.
	:raise EvtNotification: return the notification for output.
	"""
	if not session_id:
		session_id = last_session
	else:
		session_id = b94encode(session_id).decode()


def get_last_session() -> int:
	"""
	return the last session's identifier. if there is no established session, return ''
	"""
	return b94decode_to_int(last_session)


def get_active_session_count() -> int:
	return len(active_session)


def get_active_sessions(sort_: str = 'none') -> Iterator[tuple[int, bool, float]]:
	"""
	return a iterator of all sessions.
	Usually, this function should not be called, unless generating a summery of all sessions.
	:return: session ID in int, is session established, session establish time
	"""
	active_session_ID = (b94decode_to_int(_) for _ in active_session.keys())
	content = zip(active_session_ID, (_.get_is_session_established() for _ in active_session.values()),
	              active_session_time.values())
	if sort_ == 'none':
		return content
	if sort_ == 'session ID':
		return sorted(content, key=lambda x, _, __: x).__iter__()
	if sort_ == 'session time':
		return sorted(content, key=lambda _, __, x: x).__iter__()
	else:
		raise ValueError("param: sort_ should be one in ('none', 'session ID', 'session time')")
