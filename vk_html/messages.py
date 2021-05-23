from vk_api.messages import get_messages
from vk_api.info import get_info


def messages_html(name, token):
    s = r'''<!DOCTYPE html>
    <html>
    <head>
      <title>VK</title>
      <link rel="shortcut icon" href="../favicon.ico">
      <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body>
      <div class="wrap">
        <div class="header">
      <div class="page_header">
        <div class="top_home_logo"></div>
      </div>
    </div>
        <div class="page_content clear_fix">
    <div class="page_block">
    <!--content-->
     <h2 class="page_block_h2">
    <div class="page_block_header clear_fix">
      <div class="page_block_header_extra_left _header_extra_left"></div>
      <div class="page_block_header_extra _header_extra"></div>
      <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../messages.html" onclick="return nav.go(this, event, {back: true});">Сообщения</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >%s</div></div>
    </div>
    </h2><div class="wrap_page_content">%s</div>
    <!--/content-->
    </div>
       </div>
       <div class="footer">

       </div>
      </div>
    </body>
    </html>'''

    template = r'''<div class="item">
<div class="item__main"><div class="message" data-id="1241797">
<div class="message__header"><a href="{user_url}">{user_name}</a>, {date}</div>
<div><div class="kludges">{body}<div class="attachment">
<div>{attachment}</div>
<div class="attachment__description">{t}</div>
</div></div></div></div></div></div>'''

    info = get_info(token)
    url = info['url']
    user_id = info['id']

    messages = get_messages(token)

    for friend_ind in range(messages['count']):
        if messages['items'][friend_ind]['count'] == 0:
            continue

        friend_id = messages['items'][friend_ind]['friend']
        friend_name = '%s %s' % (messages['items'][friend_ind]['friend_first_name'], messages['items'][friend_ind]['friend_last_name'])
        f = open(r'users/%s/html/messages/%s.html' % (name, friend_id), 'w', encoding='utf-8')

        content = ''
        for message in messages['items'][friend_ind]['items']:
            if message['from_id'] == friend_id:
                user_name = friend_name
                user_url = 'https://vk.com/id%s' % friend_id
            else:
                user_name = name
                user_url = url

            date = message['date']

            body = attachment = t = date = ''

            if message['t'] == 'text':
                t = ''
                body = message['body']
                attachment = ''
            elif message['t'] == 'photo':
                t = 'Фотография'
                body = ''
                attachment = '<a href="%s"><img src="%s"></a>' % (message['body'], message['body'])
            elif message['t'] == 'video':
                t = 'Видео'
                body = ''
                attachment = '<a href="%s"><img src="%s" style="display: block"><span style="display: block;margin: 10px 0 10px 0">%s</span></a>' % (message['body']['url'], message['body']['photo'], message['body']['title'])
            elif message['t'] == 'audio':
                t = 'Аудиозапись'
                body = ''
                attachment = '<span class="archive__page-icon archive__page-icon--audio-albums" style="padding-left: 10px;padding-right: 10px;padding-bottom: 2px;line-height: 35px"></span><a href="%s">%s</a>' % (message['body'], message['title'])
            elif message['t'] == 'sticker':
                t = 'Стикер'
                body = ''
                attachment = '<img src="%s">' % message['body']['photo']
            elif message['t'] == 'call':
                t = 'Звонок'
                body = ''
                attachment = ''
            elif message['t'] == 'doc':
                t = 'Документ'
                body = ''
                attachment = '<a href=%s>%s</a>' % (message['body'], message['title'])
            elif message['t'] == 'gift':
                t = 'Подарок'
                body = ''
                attachment = '<img src="%s">' % message['body']['photo']
            elif message['t'] == 'wall':
                t = 'Запись на стене'
                body = ''
                attachment = '<a href=%s>%s</a>' % (message['body'], message['body'])
            elif message['t'] == 'fwd':
                t = 'Пересланное сообщение'
                body = ''
                attachment = ''
            elif message['t'] == 'link':
                t = 'Ссылка'
                body = ''
                attachment = '<a href=%s>%s</a>' % (message['body'], message['body'])
            else:
                print(message)

            content += template.format(user_name=user_name, user_url=user_url, date=date, t=t, body=body, attachment=attachment)

        f.write(s % (friend_name, content))
        f.close()