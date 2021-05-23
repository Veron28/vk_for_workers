import os
import urllib3
from vk_api.tools import *


def get_videos(token):
    http = urllib3.PoolManager()
    extra_data = '&extended=1&count=200'
    response = send_request(http, 'video.get', token, extra_data)
    videos_count = response['response']['count']
    videos = response['response']['items']

    data = {
        'count': videos_count,
        'items': []
    }

    for video in videos:
        title = video['title']
        url = video['player']
        photo = video.get('photo_320', '') or video.get('photo_130', '')

        data['items'].append({
            'title': title,
            'url': url,
            'photo': photo
        })

    return data
