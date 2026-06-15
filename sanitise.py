import json, sys, re

raw = open('data_new.json', 'r', encoding='utf-8').read()

# Replace non-breaking spaces with regular spaces
raw = raw.replace('\u00a0', ' ')

# Fix the message field before JSON parsing:
# Find the message value and remove any unescaped double-quotes inside it
# The message field looks like: "message":"some text with "quotes" in it"
# We need to escape or remove those inner quotes
def fix_message_field(text):
    # Match "message":"..." allowing for the value to contain problematic chars
    pattern = r'"message"\s*:\s*"(.*?)"(?=\s*[,}])'
    def replacer(m):
        inner = m.group(1)
        # Remove literal double-quotes from inside the value
        inner = inner.replace('"', '')
        # Clean up other problem chars
        inner = inner.replace('\u00a0', ' ').strip()
        return '"message": "' + inner + '"'
    return re.sub(pattern, replacer, text, flags=re.DOTALL)

raw = fix_message_field(raw)

try:
    data = json.loads(raw)
except Exception as e:
    print('INVALID JSON after fix:', e)
    print('First 400 chars:', raw[:400])
    sys.exit(1)

# Further clean the message field after parsing
if 'message' in data and data['message']:
    msg = data['message']
    msg = msg.replace('\u00a0', ' ')
    msg = msg.replace('\u201c', '"').replace('\u201d', '"')
    msg = msg.replace('\u2018', "'").replace('\u2019', "'")
    msg = msg.strip()
    data['message'] = msg

out = json.dumps(data, ensure_ascii=False)
open('data.json', 'w', encoding='utf-8').write(out)
print('JSON OK')
