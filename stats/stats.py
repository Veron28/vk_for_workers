from datetime import datetime


def logs(token, url, delta, success):
    f = open('logs.txt', 'a')
    f.write('%s %s %s %.2f %d\n' % (
        url,
        token,
        str(datetime.now().strftime('%Y:%m:%d:%H:%M')),
        delta,
        success
    ))
    f.close()


def urls(url):
    f = open('urls.txt', 'a')
    f.write('%s -\n' % url)
    f.close()


def errors(url, err):
    f = open('errors.txt', 'a')
    f.write('%s %s\n' % (url, str(err)))
    f.close()
