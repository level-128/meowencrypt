import json
from dataclasses import dataclass
from typing import *

from util.locked_class import lock

FILE_DIR: str = fr"config\bootconfig.cfg"


@dataclass
class _default_config:
    GUI_force_set_zoom_ratio: float = 0.0  # manually set self.gui value, none or float
    GUI_os_process_dpi_awareness: int = 1

    check_sum_len: int = 3
    session_id_len: int = 3
    is_dynamic_checksum_len: bool = True

    max_session: int = 5

    public_diffile_hellman_key: int = 15
    is_b94_encode_key: bool = True


class modify_config:

    def __init__(self):
        self.__modifiable_config: dict = {}
        self.__default_config = _default_config()
        try:
            self.load_config()
        except FileNotFoundError:
            self.reset_config()
        except PermissionError:
            raise IOError(f"Permission denied while loading config at {FILE_DIR} ")
        lock(self.__class__)

    def __getattr__(self, item):
        if item in self.__modifiable_config:
            return self.__modifiable_config[item]
        else:
            return self.__default_config.__getattribute__(item)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError("the key must be string.")
        self.__modifiable_config[key] = value

    def reset_config(self):
        _ = open(FILE_DIR, 'w')
        _.write('{}')
        _.close()
        self.__modifiable_config = {}

    def save_config(self):
        _ = open(FILE_DIR, 'w')
        _.write(json.dumps(self.__modifiable_config, indent=0))
        _.close()

    def load_config(self):
        _ = open(FILE_DIR, 'r')
        self.__modifiable_config = json.loads(_.read())
        _.close()


config = modify_config()

if __name__ == '__main__':
    raise Exception("this file is not used for execution.")
