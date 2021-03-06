"""


COPYRIGHT NOTICE:
Copyright (C) 2021  level-128

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from hashlib import md5
from math import log, ceil, floor
from typing import *

B85_EXCLUDE_CHAR = ('"', "'", ',', '.', '/', ':', ']')
ALL_PRINTABLE_CHR: Tuple[bytes] = tuple(int.to_bytes(_, 1, byteorder='big') for _ in range(33, 127))


def get_md5_checksum_str(content: str, check_str_len: int) -> str:
	"""
	return the checksum str of the given content.
	:param content: compute the content of the check sum
	:param check_str_len: the length of the checksum
	:return: the check sum represented by all printable characters (base 94)
	"""

	#  get the md5 checksum of the content
	check_sum = int.from_bytes(md5(content.encode()).digest(), byteorder='big')
	modulo_check_sum = check_sum % 94 ** check_str_len
	# next, the problem is how to convert modulo_check_sum (base 10) into a base 94 int

	checksum_str = []  # contains each number of the converted base 94 int
	for x in range(check_str_len):
		x = check_str_len - 1 - x
		_ = modulo_check_sum // 94 ** x
		checksum_str.append(_)
		modulo_check_sum -= _ * 94 ** x
	return ''.join([ALL_PRINTABLE_CHR[_ - 1].decode() for _ in checksum_str])


def is_md5_checksum_for_message_correct(content_with_checksum: str, check_str_len: int) -> bool:
	"""
	check the checksum is correct or not
	"""
	content, checksum = content_with_checksum[:-check_str_len], content_with_checksum[-check_str_len:]
	return checksum == get_md5_checksum_str(content, check_str_len)


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


def b94decode_to_int(message: Union[bytes, str]) -> int:
	message: bytes = message.encode('ASCII') if isinstance(message, str) else message
	message: bytearray = bytearray(x - 33 for x in message)  # base94 starts with ascii 33
	message.reverse()

	# noinspection PyRedundantParentheses
	# bug of PyCharm's parser
	def power():
		yield (_ := 1)
		while True: yield (_ := _ * 94)

	return sum(x * power for power, x in zip(power(), message))


def b94decode(message: Union[bytes, str]) -> bytes:
	return int.to_bytes(_ := b94decode_to_int(message), ceil(log(_, 0xFF)), byteorder='big').lstrip(b'\x00')
