from vk_api.info import get_info


def page_info_html(name, token):
    info = get_info(token)
    url = info['url']
    name = '%s %s' % (info['first_name'], info['last_name'])
    photo = info['photo']
    city = info['city']
    home_town = info['home_town']
    bdate = info['bdate']
    country = info['country']
    status = info['status']
    phone = info['phone']


    s = r'''
<!DOCTYPE html>
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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Информация о странице</div></div>
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

    photo_html = r'''<div class="item">
  <div class="item__tertiary">Фотография</div>
  <img class="fans_fan_img" src="{photo}">
</div>'''

    name_html = r'''<div class="item">
  <div class="item__tertiary">Полное имя</div>
  <div>{name}</div>
</div>'''

    bdate_html = r'''<div class="item">
  <div class="item__tertiary">Дата рождения</div>
  <div>{bdate}</div>
</div>'''

    phone_html = r'''<div class="item">
  <div class="item__tertiary">Номер телефона</div>
  <div>{phone}</div>
</div>'''

    city_html = r'''<div class="item">
  <div class="item__tertiary">Город</div>
  <div>{city}</div>
</div>'''

    country_html = r'''<div class="item">
  <div class="item__tertiary">Страна</div>
  <div>{country}</div>
</div>'''

    home_town_html = r'''<div class="item">
  <div class="item__tertiary">Родной город</div>
  <div>{home_town}</div>
</div>'''

    status_html = r'''<div class="item">
  <div class="item__tertiary">Статус</div>
  <div>{status}</div>
</div>'''

    content = ''

    if photo: content += photo_html.format(photo=photo)
    if name: content +=  name_html.format(name=name)
    if bdate: content += bdate_html.format(bdate=bdate)
    if phone: content += phone_html.format(phone=phone)
    if city: content += city_html.format(city=city)
    if country: content += country_html.format(country=country)
    if home_town: content += home_town_html.format(home_town=home_town)
    if status: content += status_html.format(status=status)

    s %= content

    f = open(r'users/%s/html/page-info.html' % name, 'w', encoding='utf-8')
    f.write(s)
    f.close()




