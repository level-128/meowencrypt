"""
meowencrypt boot:

The program should start executing from this file.

This file should include proper procedure to start all events and threads.


COPYRIGHT NOTICE:
Copyright (C) 2021  level-128

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# TODO: if a session created but not established, encrypt a message will cause error


import platform

from runlib.key_macro import start_keyboard_listen
from UI.cli import show as cli_show
from UI.main_UI import show as main_show

import wx

if platform.system() == 'Windows':
	import ctypes
	ctypes.windll.shcore.SetProcessDpiAwareness(1)

app = wx.App()

if __name__ == '__main__':
	start_keyboard_listen( )
	cli_show()
	main_show()

	app.MainLoop()
