import json, sys

raw = open('data_new.json', 'r', encoding='utf-8').read()
raw = raw.replace('\u00a0', ' ')

try:
    data = json.loads(raw)
except Exception as e:
    print('INVALID JSON:', e)
    sys.exit(1)

if 'message' in data and data['message']:
    msg = data['message']
    msg = msg.replace('\u00a0', ' ')
    msg = msg.replace('\u201c', '"').replace('\u201d', '"')
    msg = msg.replace('\u2018', "'").replace('\u2019', "'")
    msg = msg.strip()
    data['message'] = msg

out = json.dumps(data, ensure_ascii=False)
json.loads(out)
open('data.json', 'w', encoding='utf-8').write(out)
print('JSON OK')
