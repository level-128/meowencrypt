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

	content = settings_UI.show()
	if content is not None:
		config.is_default_listen_clipboard = content.pop(0)
		config.language = 'default' if (_ := content.pop(0)) == 'default' else from_name_to_notation(_)
		config.is_dark_mode = (None, False, True)[darkmode_options.index(content.pop(0))]
		config.GUI_os_process_dpi_awareness = int(content.pop(0))
		config.max_session = int(content.pop(0))
