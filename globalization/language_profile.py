import json
import locale
import sys

from config.config_library import config  # clear import


# print function used for print translated items
# noinspection PyShadowingBuiltins
def print(*args, sep=' ', end='\n'):
	sys.stdout.write(_(sep.join(args)) + end)


def get_all_supported_locals() -> tuple:
	return tuple(_all_locals.keys())


def to_local_notation(language_name: str) -> str:
	return _all_locals[language_name]


def _(english_original_text: str) -> str:
	return language_file.get(english_original_text, english_original_text)


current_locale: str = config.language
if current_locale == 'default':
	current_locale = locale.getdefaultlocale()[0]

with open(f'globalization\\languages\\all_locals', 'r') as file:
	_all_locals = json.loads(file.read())

if current_locale not in _all_locals.values():
	raise Exception(f"the selected language {current_locale} does not exist")

if current_locale == 'en_US':  # there is no need to translate when the selected language is en-US.
	def _(x):
		return x
else:
	with open(f'globalization\\languages\\{current_locale}.lan', 'r') as file:
		language_file = json.loads(file.read())
