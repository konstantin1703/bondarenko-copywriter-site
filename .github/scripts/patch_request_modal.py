from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css_anchor = '<link href="v4.css?v=23" rel="stylesheet"/><link href="v4-locale-v1.css?v=1" rel="stylesheet"/>'
js_anchor = '<script defer src="v4.js?v=16"></script><script defer src="v4-locale-v1.js?v=2"></script>'

if 'v4-request-modal-v1.css' not in s:
    if css_anchor not in s:
        raise SystemExit('CSS anchor not found')
    s = s.replace(css_anchor, css_anchor + '<link href="v4-request-modal-v1.css?v=2" rel="stylesheet"/>', 1)
else:
    s = s.replace('v4-request-modal-v1.css?v=1', 'v4-request-modal-v1.css?v=2')

if 'v4-request-modal-v1.js' not in s:
    if js_anchor not in s:
        raise SystemExit('JS anchor not found')
    s = s.replace(js_anchor, js_anchor + '<script defer src="v4-request-modal-v1.js?v=2"></script>', 1)
else:
    s = s.replace('v4-request-modal-v1.js?v=1', 'v4-request-modal-v1.js?v=2')

p.write_text(s, encoding='utf-8')
print('request modal assets connected at v2')
