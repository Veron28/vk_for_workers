import urllib3
from vk_api.tools import send_request


def get_black_list(token):
	http = urllib3.PoolManager()
	response = send_request(http, 'account.getBanned', token)
	black_list_count = response['response']['count']
	black_list = response['response']['items']
	data = {
		'count': black_list_count,
		'items': []
	}

	for person in black_list:
		first_name = person['first_name']
		last_name = person['last_name']
		url = 'vk.com/id%s' % person['id']

		data['items'].append({
			'first_name': first_name,
			'last_name': last_name,
			'url': url
		})

	return data
