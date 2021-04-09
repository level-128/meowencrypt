from hashlib import md5
from typing import Union
from math import log, ceil

B85_EXCLUDE_CHAR = ('"', "'", ',', '.', '/', ':', ']')
ALL_PRINTABLE_CHR = tuple(int.to_bytes(_, 1, byteorder='big') for _ in range(33, 127))


def get_md5_checksum_str(content: str, check_str_len: int) -> str:
	"""
	return the checksum str of the given content.
	:param content: compute the content of the check sum
	:param check_str_len: the length of the checksum
	:return: the check sum represented by using characters in B85_EXCLUDE_STR
	"""

	#  get the md5 checksum of the content
	check_sum = int.from_bytes(md5(content.encode( )).digest( ), byteorder='big')
	# the checksum value which should converted to base94 and map to B85_EXCLUDE_CHAR
	modulo_check_sum = check_sum % 94**check_str_len
	# next, the problem is how to convert modulo_check_sum (base 10) into a base 94 int

	checksum_str = []  # contains each number of the converted base 94 int
	for x in range(check_str_len):
		x = check_str_len - 1 - x
		_ = modulo_check_sum // 94 ** x
		checksum_str.append(_)
		modulo_check_sum -= _ * 94 ** x
	return ''.join([ALL_PRINTABLE_CHR[_ - 1].decode() for _ in checksum_str])


def b94encode(message: Union[bytes, int]) -> bytes:
	if isinstance(message, bytes):
		message = int.from_bytes(message, 'big')
	message: int
	result = bytearray()
	while True:
		truediv = message // 94
		result.append(message % 94 + 33)  # base94 starts with ascii 33
		if not truediv:
			break
		message = truediv
	result.reverse()
	return bytes(result)


def b94decode(message: Union[bytes, str]) -> bytes:
	if isinstance(message, str):
		message: bytes = message.encode('ASCII')
	message: bytearray = bytearray(x - 33 for x in message)  # base94 starts with ascii 33
	message.reverse()
	sum_ = 0
	for index, x in enumerate(message):
		sum_ += x * 94**index
	return int.to_bytes(sum_, ceil(log(sum_, 0xFF)), byteorder='big')

