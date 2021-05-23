import urllib3

from vk_api.friends import get_friends
from vk_html.messages import messages_html

from vk_api.tools import send_request


def message_list_html(name, token):
    template = r'''<div class="item" style="border-bottom: 1px solid #e7e8ec;">
<div class='item__main'><img style="margin-bottom: -15px;width: 50px;height: 50px;margin-right: 10px;border-radius: 5px" src="{photo}"><a href="messages/{id}.html">{friend_name}</a></div></div>'''

    friends = get_friends(token)
    content = ''
    for friend in friends['items']:
        http = urllib3.PoolManager()
        extra_data = '&user_id=%d' % friend['id']
        response = send_request(http, 'messages.getHistory', token, extra_data)
        message_count = response['response']['count']
        if message_count == 0:
            continue

        friend_name = '%s %s' % (friend['first_name'], friend['last_name'])
        url = friend['url']
        photo = friend['photo']
        friend_id = friend['id']
        content += template.format(friend_name=friend_name, url=url, photo=photo, id=friend_id)

    s = r'''<!DOCTYPE html>
<html>
<head>
  <title>VK</title>
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="stylesheet" type="text/css" href="style.css">
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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Сообщения</div></div>
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

    s %= content

    f = open(r'users/%s/html/messages.html' % name, 'w', encoding='utf-8')
    f.write(s)
    f.close()

    messages_html(name, token)