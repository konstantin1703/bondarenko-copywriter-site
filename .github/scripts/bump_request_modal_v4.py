from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = 'v4-request-modal-v1.js?v=3'
new = 'v4-request-modal-v1.js?v=4'
if old not in s:
    if new in s:
        print('request modal JS already at v4')
    else:
        raise SystemExit('request modal JS anchor not found')
else:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')
    print('request modal JS cache-bust bumped to v4')
