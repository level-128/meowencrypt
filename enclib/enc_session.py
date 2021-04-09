from typing import *
from base64 import b85encode, b85decode
from random import randint

from Crypto.Cipher import AES
from Crypto.Util import Counter

from enclib.enc_utilities import b94encode, b94decode, get_md5_checksum_str
from enclib.DHElib.DHE import DHE_target
from config.config_library import config


#  the printable characters which b85 does not include are:
B85_EXCLUDE_CHAR = ('"', "'", ',', '.', '/', ':', ']')
ALL_PRINTABLE_CHR = tuple(chr(_) for _ in range(33, 127))
CONST_NEW_SESSION_NOTATION: str = ':'
CONST_KEY_EXCHANGE_NOTATION: str = '.'
CONST_MSG_NOTATION: str = '"'


class ContentError(Exception):
	def __init__(self):
		super(ContentError, self).__init__("this message is not in meowencrypt format")


class encryption:

	def __init__(self, enc_strength: int = 15):
		self.__key: Union[bytes, None] = None
		self.DHE_target_instance = DHE_target(enc_strength)
		self.__check_sum_len = 3
		self.session_id_len = 3
		self.__key: Union[bytes, None] = None
		self.__session_id: Union[str, None] = None
		self.__aes: Union[Any, None] = None

	def create_session_request(self) -> str:
		"""
		return the shared key to the other user
		:return: key in str with checksum
		"""
		if self.__session_id is None:
			self.__session_id = ''.join([chr(randint(33, 126)) for _ in range(self.session_id_len)])
			_ = CONST_NEW_SESSION_NOTATION + self.__session_id
		else:
			_ = CONST_KEY_EXCHANGE_NOTATION + self.__session_id
		_ = _ + b94encode(self.DHE_target_instance.get_shared_key( )).decode('ASCII')
		return _ + get_md5_checksum_str(_, self.__check_sum_len)

	def receive_session_request(self, bob_share_key: str) -> None:
		if self.__session_id is None:
			self.__session_id = bob_share_key[1:self.session_id_len + 1]
		bob_share_key: str = bob_share_key[1 + self.session_id_len:-self.__check_sum_len]
		bob_share_key: bytes = b94decode(bob_share_key)
		self.__key = self.DHE_target_instance.generate_shared_key(bob_share_key)

	def get_session_id(self) -> str:
		return self.__session_id

	def get_checksum_len(self) -> int:
		return self.__check_sum_len

	def encrypt_content(self, original_content: str) -> str:
		original_content: bytes = original_content.encode('utf-8')
		original_content: bytes = original_content + (16 - len(original_content) % 16) * b' '

		self.__aes = AES.new(self.__key, AES.MODE_CTR, counter=Counter.new(128))
		original_content: bytes = self.__aes.encrypt(original_content)
		original_content: str = b85encode(original_content).decode('ASCII')
		_ = CONST_MSG_NOTATION + self.__session_id + original_content
		return _ + get_md5_checksum_str(_, self.__check_sum_len)

	def decrypt_content(self, content: str):
		content = content[1+self.session_id_len:-self.__check_sum_len]
		content = b85decode(content.encode('ASCII'))
		self.__aes = AES.new(self.__key, AES.MODE_CTR, counter=Counter.new(128))
		try:
			return self.__aes.decrypt(content).decode('utf-8')
		except UnicodeDecodeError:
			raise ContentError


# x = session( )
# y = session( )
#
# y_skey = y.create_session_request( )
# x.receive_session_request(y_skey)
#
# x_skey = x.create_session_request( )
# y.receive_session_request(x_skey)
#
# print(x_msg := x.encrypt_content('你好'))
# print(y_msg := y.encrypt_content('你好'))
# print(x.decrypt_content(x_msg))
