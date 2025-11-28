import sys
import base64
import os
import requests
import msgpack

url = sys.argv[1]
root_dir = 'dep/oem/brogue-rpg'

if not os.path.exists(root_dir):
    os.mkdir(root_dir)

resp = requests.get(url)
resp.raise_for_status()

mpk_b64 = resp.text
mpk_data = base64.b64decode(mpk_b64)
data = msgpack.loads(mpk_data)

assert isinstance(data, dict)

for flat_path, b in data.items():
    path = os.path.join(root_dir, flat_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f'Writing {path}...')
    with open(path, 'wb') as f:
        f.write(b)
