import requests
import json
import re
import os
import time

disid_param = {'action':'list', '':'', '':'', '':''}
disid_result = requests.get('', params=disid_param, headers={'Connection':'close'})
time.sleep(0.01)

disid_result_json = disid_result.json()
datas = disid_result_json['datas']

for data in datas:
	name = data['name']
	path = os.path.join('',name)
	if(os.path.exists(path)):
		print(path+'存在')
	else:
		os.makedirs(path, 0o777)

	dislst = data['dislst']
	for dis in dislst:
		dis_id = dis['ID']
		dis_name = dis['name']
		dis_path = os.path.join(path, dis_name)
		if(os.path.exists(dis_path)):
			print(dis_path+'存在')
		else:
			os.makedirs(dis_path, 0o777)

		image_param = {'':'', '':'', '':'', '':dis_id}
		try:
			image_result = requests.get('', params=image_param, headers={'Connection':'close'})
			time.sleep(0.01)
			photoPathList = re.findall(r'"PhotoPath":(.*?),', image_result.text)

			for photoPath in photoPathList:
				photoPath = photoPath.replace('\"', '')
				photoPath = os.path.join('', photoPath)

				photoName = photoPath.split("/")[-1]
				photoName = os.path.join(dis_path, photoName)
				try:
					r = requests.get(photoPath, stream=True, headers={'Connection':'close'})
					time.sleep(0.01)
					with open(photoName, 'wb') as fd:
						for chunk in r.iter_content():
							fd.write(chunk)
				except:
					time.sleep(50)
					print('zzzzzzzzzzzzzzzzz~')
					continue
		except:
			time.sleep(50)
			print('Azzzzzzzzzzzzzzzzz~')
			continue



