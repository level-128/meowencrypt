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
CONST_MSG_NOTATION: str = '/'


class ContentError(Exception):
	def __init__(self):
		super(ContentError, self).__init__("this message is not in meowencrypt format")


class encryption:
	"""
	creates a encryption session object.
	a session indicates a single end-to-end encryption instance. it includes essential components to
	establish a connection.
	"""

	def __init__(self, enc_strength: int = 15):
		"""
		you shouldn't modify the param enc_strength.
		"""
		self.__key: Union[bytes, None] = None
		self.DHE_target_instance = DHE_target(enc_strength)
		self.__check_sum_len = config.check_sum_len
		self.session_id_len = config.session_id_len
		self.__key: Union[bytes, None] = None
		self.__session_id: Union[str, None] = None
		self.__aes: Union[Any, None] = None

	def create_session_request(self) -> str:
		"""
		create a session request by generating a session ID and a public key, then return the encoded key.
		:return: key in str with checksum
		"""
		if self.__session_id is None:
			#  generate a random printable session ID.
			self.__session_id = ''.join([chr(randint(33, 126)) for _ in range(self.session_id_len)])
			_ = CONST_NEW_SESSION_NOTATION + self.__session_id
		else:
			_ = CONST_KEY_EXCHANGE_NOTATION + self.__session_id
		_ = _ + b94encode(self.DHE_target_instance.get_shared_key( )).decode('ASCII')
		return _ + get_md5_checksum_str(_, self.__check_sum_len)

	def receive_session_request(self, bob_share_key: str) -> None:
		"""
		received a key exchange message. In diffie-hellman algorithm, if public key has been received, the key could be
		generated.
		First, acquire the session ID. if the session ID does not exist, it means this instance has received a new session
		request from others.
		If the session ID exist, this instance has created a new session before receiving this session request.
		"""
		if self.__session_id is None:
			self.__session_id = bob_share_key[1:self.session_id_len + 1]
		bob_share_key: str = bob_share_key[1 + self.session_id_len:-self.__check_sum_len]
		bob_share_key: bytes = b94decode(bob_share_key)
		self.__key = self.DHE_target_instance.generate_shared_key(bob_share_key)

	def get_session_id(self) -> str:
		"""
		return the session's ID
		"""
		return self.__session_id

	def get_checksum_len(self) -> int:
		"""
		return the length of the checksum.
		"""
		return self.__check_sum_len

	def encrypt_content(self, original_content: str) -> str:
		"""
		encrypt the message by creating a AES algorithm object.
		"""
		original_content: bytes = original_content.encode('utf-8')
		#  since the AES counter mode requires padding to fill the content,
		#  making length of the content becomes the multiplier of 16.
		original_content: bytes = original_content + (16 - len(original_content) % 16) * b' '
		
		#  in AES counter mode, it generates the next key stream block by encrypting successive values of a counter,
		#  which is guaranteed not to repeat for a long time. The counter itself could be public.
		self.__aes = AES.new(self.__key, AES.MODE_CTR, counter=Counter.new(128))
		original_content: bytes = self.__aes.encrypt(original_content)
		original_content: str = b85encode(original_content).decode('ASCII')
		_ = CONST_MSG_NOTATION + self.__session_id + original_content
		return _ + get_md5_checksum_str(_, self.__check_sum_len)

	def decrypt_content(self, content: str):
		"""
		decrypt the content.
		"""
		content = content[1+self.session_id_len:-self.__check_sum_len]
		content = b85decode(content.encode('ASCII'))
		self.__aes = AES.new(self.__key, AES.MODE_CTR, counter=Counter.new(128))
		try:
			return self.__aes.decrypt(content).decode('utf-8').rstrip()  # remove the padding space.
		except UnicodeDecodeError:
			raise ContentError


if __name__ == '__main__':
	"""
	a small demo about how it works.
	"""
	x = encryption( )
	y = encryption( )

	y_skey = y.create_session_request( )
	x.receive_session_request(y_skey)

	x_skey = x.create_session_request( )
	y.receive_session_request(x_skey)

	print(x_msg := x.encrypt_content('hello'))
	print(y_msg := y.encrypt_content('hello'))
	print(x.decrypt_content(x_msg))
