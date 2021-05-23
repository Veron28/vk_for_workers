import urllib3
from vk_api.tools import send_request, transform_date


def get_docs(token):
    http = urllib3.PoolManager()
    response = send_request(http, 'docs.get', token)
    docs_count = response['response']['count']
    docs = response['response']['items']

    data = {
        'count': docs_count,
        'items': []
    }

    for doc in docs:
        title = doc['title']
        url = doc['url']
        date = transform_date(doc['date'])

        data['items'].append({
            'title': title,
            'url': url,
            'date': date
        })

    return data
