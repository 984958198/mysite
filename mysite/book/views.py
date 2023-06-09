
from django.db import connection, connections, transaction
from django.contrib.auth import authenticate, login, logout
from mysite.basics import ME
from mysite.book.models import Douban
from mysite.basics import login_exempt
import pyquery, requests
import logging, re, time
log = logging.getLogger('log')

@login_exempt
def get_book(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    obj = Douban.objects.filter()
    total = obj.count()
    data = obj[(page - 1) * page_size: page * page_size]
    return {'data': list(data.values()), 'total': total, 'page': page, 'page_size': page_size}


@login_exempt
def sync_book(request):
    num = write_db()
    return num


def crawl_book(start=0):
    # 爬取数据
    data = []
    try:
        content = requests.get('https://book.douban.com/top250?start=%s' % start, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}).content
    except Exception as e:
        logging.exception(e)
    else:
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pq = pyquery.PyQuery(content)
        for it in pq.items('table[width="100%"]'):
            data.append({
                'img': it.find('img').attr('src'),
                'href': it.find('div[class="pl2"] a').attr('href'),
                'title': it.find('div[class="pl2"] a').attr('title'),
                'read': it.find('div[class="pl2"] img').attr('alt') == u'可试读',
                'make': it.find('p[class="pl"]').text(),
                'score': it.find('div[class="star clearfix"] span[class="rating_nums"]').text(),
                'appraise': re.sub('.+?(\d+).+', r'\1', it.find('div[class="star clearfix"] span[class="pl"]').text()),
                'intro': it.find('p[class="quote"] span[class="inq"]').text(),
                'update_time': update_time,
            })
            data[-1]['id'] = int(re.sub('.+?/(\d+)/$', r'\1', data[-1]['href']))  # 唯一标识, 作为修改依据
    return data


def write_db():
    # 写入数据库
    datas = []
    for i in range(1, 4):  # 获取3页数据，页数不多就不写并发了
        datas += crawl_book((i - 1) * 25)
    if datas:
        keys = datas[0].keys()
        sql = 'INSERT INTO book_douban (%s) VALUES %s ON CONFLICT (id) DO UPDATE SET %s;' % (
            ','.join(keys),
            ','.join(["('%s')" % "','".join(['%s' % d[k] for k in keys]) for d in datas]),
            ','.join(['%s = excluded.%s' % (k, k) for k in keys if k != 'id'])
        )
        with connections['default'].cursor() as cursor:
            cursor.execute(sql)
    return len(datas)
