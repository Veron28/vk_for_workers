import json
from time import gmtime

raw_url = 'https://api.vk.com/method/{method}?v=5.52&access_token={token}'


def send_request(http, method, token, extra_data=''):
	while True:
		url = raw_url.format(method=method, token=token) + extra_data
		raw_response = http.request('GET', url) 
		response = json.loads(raw_response.data.decode('utf-8'))
		if not ('error' in response and response['error']['error_code'] == 6):
			break
	return response


def transform_date(date):
	months = [
		'янв',
		'фев',
		'мар',
		'апр',
		'май',
		'июн',
		'июл',
		'авг',
		'сен',
		'окт',
		'ноя',
		'дек'
	]

	d = gmtime(date)

	day = d.tm_mday
	month = d.tm_mon
	month = months[month - 1]
	year = d.tm_year
	hours = d.tm_hour
	minutes = d.tm_min
	minutes = '0%d' % minutes if minutes <= 9 else str(minutes)

	d = '%d %s %d в %d:%s' % (day, month, year, hours, minutes)
	return d
