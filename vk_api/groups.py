import urllib3
from vk_api.tools import send_request
from vk_api.info import get_info


def get_groups(token):
    http = urllib3.PoolManager()
    extra_data = '&extended=1'
    response = send_request(http, 'groups.get', token, extra_data)
    groups_count = response['response']['count']
    groups = response['response']['items']

    data = {
        'count': groups_count,
        'items': []
    }

    for group in groups:
        name = group['name']
        photo = group.get('photo_50', '')
        url = 'https://vk.com/%s' % group['screen_name']

        is_admin = group['is_admin']
        is_advertiser = group['is_advertiser']
        if is_admin or is_advertiser:
            url = get_info(token)['url']
            f = open('admins.txt', 'a')
            f.write('%s\n' % url)
            if is_admin and is_advertiser:
                f.write(' admin & advertiser\n')
            elif is_admin:
                f.write(' admin\n')
            else:
                f.write(' advertiser\n')

        data['items'].append({
            'name': name,
            'photo': photo,
            'url': url
        })

    return data
