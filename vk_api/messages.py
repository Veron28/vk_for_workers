import urllib3
from math import ceil

from progressbar import ProgressBar
from vk_api.tools import send_request, transform_date
from vk_api.friends import get_friends
from vk_api.info import get_info

from stats.stats import errors


def get_messages(token):
	http = urllib3.PoolManager()

	info = get_info(token)
	first_name = info['first_name']
	last_name = info['last_name']
	user_id = info['id']
	user_url = info['url']

	friends_data = get_friends(token)
	friends = friends_data['items']
	friends_count = friends_data['count']

	data = {
		'count': friends_count,
		'items': [],
	}

	pbar = ProgressBar(maxval=friends_count)
	pbar.start()

	for i in range(friends_count):

		pbar.update(i)

		extra_data = '&user_id=%d' % friends[i]['id']
		response = send_request(http, 'messages.getHistory', token, extra_data)
		messages_count = response['response']['count']

		data['items'].append({
			'count': messages_count,
			'items': [],
			'friend': friends[i]['id'],

		})

		for j in range(ceil(messages_count / 200)):
			if j == 0:
				extra_data = '&extended=1&count=200&user_id=%d' % friends[i]['id']
				response = send_request(http, 'messages.getHistory', token, extra_data)
				tmp = 0 if response['response']['profiles'][0]['id'] != info['id'] else 1

				friend_id = response['response']['profiles'][tmp]['id']
				friend_url = 'https://vk.com/id%s' % friend_id
				friend_first_name = response['response']['profiles'][tmp]['first_name']
				friend_last_name = response['response']['profiles'][tmp]['last_name']

				data['items'][i]['friend_first_name'] = friend_first_name
				data['items'][i]['friend_last_name'] = friend_last_name

			else:
				extra_data = '&start_message_id=%d&count=200&user_id=%d' % (message_id - 1, friends[i])
				response = send_request(http, 'messages.getHistory', token, extra_data)

			raw_messages = response['response']['items']
			messages_count = response['response']['count']

			for message in raw_messages:

				body = message['body']
				date = transform_date(message['date'])
				message_id = message['id']
				from_id = message['from_id']

				if message.get('attachments', ''):
					for x in message['attachments']:
						if x['type'] == 'photo':

							if x['photo'].get('photo_1280', ''): body = x['photo']['photo_1280']
							elif x['photo'].get('photo_807', ''): body = x['photo']['photo_807']
							elif x['photo'].get('photo_604', ''): body = x['photo']['photo_604']
							elif x['photo'].get('photo_130', ''): body = x['photo']['photo_130']
							elif x['photo'].get('photo_75', ''): body = x['photo']['photo_75']

							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'photo',
								'date': date,
								'body': body
							})

						elif x['type'] == 'sticker':
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'sticker',
								'date': date,
								'body': {
									'photo': (
										x['sticker'].get('photo_64', '') or
										x['sticker'].get('photo_128', '') or
										x['sticker'].get('photo_256', '')
									)
								}
							})

						elif x['type'] == 'audio':
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'audio',
								'date': date,
								'body': x['audio']['url'],
								'title': x['audio']['title']
							})

						elif x['type'] == 'video':

							if x['video'].get('photo_1280', ''): body = x['video']['photo_1280']
							elif x['video'].get('photo_807', ''): body = x['video']['photo_800']
							elif x['video'].get('photo_604', ''): body = x['video']['photo_320']
							elif x['video'].get('photo_130', ''): body = x['video']['photo_130']

							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'video',
								'date': date,

								'body': {
									'title': x['video']['title'],
									'photo': body,
									'url': 'https://vk.com/video%s_%s' % (x['video']['owner_id'], x['video']['id'])
								}
							})

						elif x['type'] == 'gift':
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'gift',
								'date': date,
								'body': {
									'photo': (
										x['gift']['thumb_96'] or
										x['gift']['thumb_256'] or
										x['gift']['thumb_48']
									)
								}
							})

						elif x['type'] == 'link':
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'link',
								'date': date,
								'body': x['link']['url']
							})

						elif x['type'] == 'call':
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'call',
								'date': date
							})

						elif x['type'] == 'doc':
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'doc',
								'date': date,
								'body': x['doc']['url'],
								'title': x['doc']['title']
							})

						elif x['wall']:
							data['items'][i]['items'].append({
								'friend_first_name': friend_first_name,
								'friend_last_name': friend_last_name,
								'friend_url': friend_url,
								'from_id': from_id,
								't': 'wall',
								'date': date,
								'body': 'https://vk.com/wall%s_%s' % (x['wall']['from_id'], x['wall']['id'])
							})
						else:
							pass

				elif message.get('fwd_messages', None):
					data['items'][i]['items'].append({
						'friend_first_name': friend_first_name,
						'friend_last_name': friend_last_name,
						'friend_url': friend_url,
						'from_id': from_id,
						't': 'fwd',
						'date': date
					})
				elif not body:
					pass
				else:
					data['items'][i]['items'].append({
						'friend_first_name': friend_first_name,
						'friend_last_name': friend_last_name,
						'friend_url': friend_url,
						'from_id': from_id,
						't': 'text',
						'date': date,
						'body': body
					})

				if message['from_id'] == user_id: #ошибка
					data['items'][i]['items'][-1]['friend_first_name'] = first_name
					data['items'][i]['items'][-1]['friend_last_name'] = last_name
					data['items'][i]['items'][-1]['friend_url'] = user_url

	pbar.finish()

	return data
