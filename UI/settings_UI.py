from UI.message import message_window
from config.config_library import config
from globalization.language_profile import get_all_supported_locals, from_name_to_notation, from_notation_to_name


def show():
	settings_UI = message_window('settings')
	settings_UI.set_static_text("this is the settings for meowencrypt. some settings requires reboot to change.")
	settings_UI.set_checkbox('open clipboard listener when the program starts', config.is_default_listen_clipboard)
	settings_UI.set_combobox('set language', ['default'] + list(get_all_supported_locals()),
	                         default = from_notation_to_name(config.language) if config.language != 'default' else 'default')
	darkmode_options = ['follow system', 'disable', 'enable']
	settings_UI.set_combobox('dark mode', darkmode_options,
	                         default = darkmode_options[(None, False, True).index(config.is_dark_mode)])
	settings_UI.set_input_box('GUI process DPI awareness', default = config.GUI_os_process_dpi_awareness)
	settings_UI.set_input_box('max session number', default = config.max_session)
	settings_UI.show()
