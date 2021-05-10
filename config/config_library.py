import json
import os.path
from dataclasses import dataclass
from typing import *

FILE_DIR: str = fr"config\bootconfig.cfg"

VERSION = '0.1.210430-alpha'

@dataclass
class _default_config:
	GUI_os_process_dpi_awareness: int = 1

	check_sum_len: int = 3
	session_id_len: int = 3

	max_session: int = 5

	public_diffile_hellman_key: int = 15

	hotkey_select_all_text_to_session: str = 'ctrl + alt + a'
	hotkey_select_all_text_to_encrypt: str = 'ctrl + alt + s'
	hotkey_select_all_text_and_auto_process: str = 'ctrl + alt + z'
	hotkey_toggle_listen_clipboard_change: str = 'ctrl + alt + q'
	hotkey_new_session: str = 'ctrl + alt + n'
	hotkey_show_main_UI: str = 'ctrl + alt + u'

	is_default_listen_clipboard: bool = False
	language: str = 'default'  # default or local code
	is_dark_mode: Union[bool, None] = None
	icon_path: str = r'files/level-128_avatar_128x128.ico'
	is_show_cli: bool = True


class modify_config:

	def __init__(self):
		self.__modifiable_config: dict = {}
		self.__default_config = _default_config( )
		try:
			self.load_config( )
		except FileNotFoundError:
			self.reset_config( )
		except PermissionError:
			raise IOError(f"Permission denied while loading config at {FILE_DIR} ")

	def __getattr__(self, item: str) -> Any:
		if item in self.__modifiable_config:
			return self.__modifiable_config[item]
		if item in self.__default_config.__dict__:
			return self.__default_config.__getattribute__(item)
		else:
			raise AttributeError(f"the '{item}' is not in config library.")

	def __setitem__(self, key: str, value: Any):
		if not isinstance(key, str):
			raise ValueError("the key must be string.")
		self.__modifiable_config[key] = value

	def reset_config(self):
		if not os.path.isdir('config'):
			os.mkdir('config')
		_ = open(FILE_DIR, 'w')
		_.write('{}')
		_.close( )
		self.__modifiable_config = {}

	def save_config(self):
		_ = open(FILE_DIR, 'w')
		_.write(json.dumps(self.__modifiable_config, indent = 0))
		_.close( )

	def load_config(self):
		_ = open(FILE_DIR, 'r')
		self.__modifiable_config = json.loads(_.read())
		_.close( )


config = modify_config( )

if __name__ == '__main__':
	raise Exception("this file is not used for execution.")
