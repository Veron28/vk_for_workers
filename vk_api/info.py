import urllib3
from vk_api.tools import *


def get_info(token):
	http = urllib3.PoolManager()
	response = send_request(http, 'account.getProfileInfo', token)

	url = 'https://vk.com/id%d' % response['response']['id']
	first_name = response['response']['first_name']
	last_name = response['response']['last_name']
	home_town = response['response']['home_town']
	city = response['response']['city']['title']
	status = response['response']['status']

	day, month, year = response['response']['bdate'].split('.')
	if len(day) == 1: day = '0%s' % day
	if len(month) == 1: month = '0%s' % month
	bdate = '.'.join([day, month, year])

	country = response['response']['country']['title']
	phone = response['response']['phone']
	photo = response['response']['photo_200']
	user_id = response['response']['id']

	data = {
		'first_name': first_name,
		'last_name': last_name,
		'url': url,
		'home_town': home_town,
		'city': city,
		'status': status,
		'bdate': bdate,
		'country': country,
		'phone': phone,
		'photo': photo,
		'id': user_id
	}

	return data