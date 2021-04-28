from hashlib import sha256
from math import log, ceil
from secrets import randbelow

from gmpy2 import mpz

from enclib.DHElib.HDE_const import MODB_GROUPS


def pow_mod(g, k, p):
	g, k, p = mpz(g), mpz(k), mpz(p)

	n = 1
	while k:
		if k & 1:
			n = n * g % p
		k >>= 1
		g = g * g % p
	return int(n)


class DHE_target:

	def __init__(self, public_key: int):
		self._generator = MODB_GROUPS[public_key][0]
		self._public_key = MODB_GROUPS[public_key][1]
		self._a = randbelow(self._public_key - 1) + 1  # [1, self.p)

		self.shared_key = pow_mod(self._generator, self._a, self._public_key)  # pass this value to the target

	def get_shared_key(self) -> bytes:
		byte_length = ceil(log(self.shared_key, 256))
		return int.to_bytes(self.shared_key, length=byte_length, byteorder='big')

	def generate_shared_key(self, shared_key_from_bob: bytes) -> bytes:
		"""
		:param shared_key_from_bob: str, the shared key from the other sender,
		hexadecimal value converted to string.
		:return: the final key for encoding
		"""
		shared_key_from_bob: int = int.from_bytes(shared_key_from_bob, byteorder='big')
		key = pow_mod(shared_key_from_bob, self._a, self._public_key)
		byte_length = ceil(log(key, 256))
		return sha256(int.to_bytes(key, length=byte_length, byteorder='big')).digest( )

