import urllib3
from vk_api.tools import send_request


def get_friends(token):
    http = urllib3.PoolManager()
    extra_data = '&fields=photo_50'
    response = send_request(http, 'friends.get', token, extra_data)
    friends_count = response['response']['count']
    friends = response['response']['items']

    data = {
        'count': friends_count,
        'items': []
    }

    for friend in friends:
        friend_id = friend['id']
        url = 'https://vk.com/id%d' % friend['id']
        first_name = friend['first_name']
        last_name = friend['last_name']
        photo = friend.get('photo_50', '')

        data['items'].append({
            'id': friend_id,
            'first_name': first_name,
            'last_name': last_name,
            'photo': photo,
            'url': url
        })

    return data
