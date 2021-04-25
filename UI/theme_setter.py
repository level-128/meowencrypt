import platform
import wx

from config.config_library import config


def _detect_darkmode( ):
	if config.is_dark_mode is not None:
		return config.is_dark_mode

	if platform.system() != 'Windows':  # does not support operating system other than windows
		return False
	reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
	try:
		import winreg
		registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
		reg_key = winreg.OpenKey(registry, reg_keypath)
		value, _ = winreg.QueryValueEx(reg_key, 'AppsUseLightTheme')
		return value == 0
	except (FileNotFoundError, ImportError):
		return False


# noinspection PyUnresolvedReferences
def detect_darkmode():
	try:
		return is_darkmode
	except NameError:
		globals()['is_darkmode'] = _detect_darkmode()
		return is_darkmode


def set_color(item, is_white, is_background = True):
	if detect_darkmode():
		if is_background:
			if is_white:
				item.SetOwnBackgroundColour(wx.Colour(17, 17, 17))
			else:
				item.SetOwnBackgroundColour(wx.Colour(240, 240, 240))
		else:
			if is_white:
				item.SetOwnForegroundColour(wx.Colour(17, 17, 17))
			else:
				item.SetOwnForegroundColour(wx.Colour(240, 240, 240))


if __name__ == '__main__':
	print(detect_darkmode( ))
	print(detect_darkmode( ))
