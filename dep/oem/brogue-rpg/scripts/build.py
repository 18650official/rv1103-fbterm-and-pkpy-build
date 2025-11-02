from datetime import datetime
import os
import json

targets = ['assets/', 'backend/', 'dungeon/', 'frontend/', 'driver.py', 'main.py']
now = datetime.now().strftime('%Y%m%d%H%M%S')
filename = f'brogue-rpg-{now}.json'

package = {}
def add_file(path: str):
    path = path.replace('\\', '/')
    print(path)
    with open(path, 'r', encoding='utf-8') as f:
        package[path] = f.read()

for t in targets:
    if t.endswith('/'):
        for root, _, files in os.walk(t):
            for f in files:
                add_file(os.path.join(root, f))
    else:
        add_file(t)

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(package, f, ensure_ascii=False)

filesize = os.path.getsize(filename)
print(f'打包完成: {filename} ({filesize / 1024:.2f} KB)')

if input('是否上传到inkpad-backend？(y/n)\n') == 'y':
    import requests
    url = 'https://gyc.hclcat.games/ink/v1/brogue-rpg/update'
    resp = requests.post(url, json={
        'ink_src': package,
    })
    assert (resp.status_code == 200), f'上传失败: {resp.status_code} {resp.text}'
    print('上传成功')
