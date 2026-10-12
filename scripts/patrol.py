"""巡逻：查重 + 检查链接是否还活着。用法：python scripts/patrol.py [--add URL]"""
import json, sys, datetime, urllib.request
from urllib.parse import urlparse
P = 'index.json'
def norm(u):
    p = urlparse(u.lower().rstrip('/')); return p.netloc.removeprefix('www.') + p.path
idx = json.load(open(P, encoding='utf-8'))
keys = {}
for it in idx['items']:
    k = norm(it['url'])
    if k in keys: print(f"重复: {it['name']} 与 {keys[k]}")
    keys[k] = it['name']
if '--add' in sys.argv:
    u = sys.argv[sys.argv.index('--add') + 1]
    print(f"已收录: {keys[norm(u)]}" if norm(u) in keys else "没收录过，可以加")
    sys.exit()
today = str(datetime.date.today())
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8'}
def check(url):
    # GET + 浏览器 UA，失败重试一次；401/403/429/503 多是机器人防护（Cloudflare 等），算“活着但无法验证”
    last = None
    for _ in range(2):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25)
            return 'ok' if r.status < 400 else f'http {r.status}'
        except Exception as e:
            code = getattr(e, 'code', None)
            if code in (401, 403, 405, 429, 503): return 'ok'
            last = f'down: {code or type(e).__name__}'
    return last
for it in idx['items']:
    it['status'] = check(it['url'])
    it['last_checked'] = today
    if it['status'] != 'ok': print(f"{it['name']}: {it['status']}")
idx['updated'] = today
json.dump(idx, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
