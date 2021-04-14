import json

with open('languages\\' + (lan_pro := input("language profile: ")) + '.lan') as file:
	if len(file_content := file.read()) == 0:
		lan_dict = {}
	else:
		lan_dict = json.loads(file_content)

try:
	while True:
		_ = input("original text: ")
		if _ == '':
			with open('languages\\' + lan_pro + '.lan', 'w') as file:
				_ = json.dumps(lan_dict, indent=0)
				file.write(_)
			exit(0)
		lan_dict[_] = input('--> ')
except Exception as e:
	input(e)

