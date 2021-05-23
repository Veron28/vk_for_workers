import urllib3
from vk_api.tools import send_request, transform_date


def get_photos(token):
    http = urllib3.PoolManager()

    data = {
        'wall': {
            'count': 0,
            'items': []
        },
        'saved': {
            'count': 0,
            'items': []
        },
        'profile': {
            'count': 0,
            'items': []
        }
    }

    for t in ['wall', 'saved', 'profile']:
        extra_data = '&album_id=' + t + '&rev=0&count=1000'
        response = send_request(http, 'photos.get', token, extra_data)
        photos_count = response['response']['count']
        photos = response['response']['items']

        data[t]['count'] = photos_count

        for photo in photos:
            url = (
                    photo.get('photo_1280', '') or
                    photo.get('photo_807', '') or
                    photo.get('photo_604', '') or
                    photo.get('photo_130', '') or
                    photo.get('photo_75', '')
            )
            date = transform_date(photo['date'])

            data[t]['items'].append({
                'url': url,
                'date': date
            })

    return data

