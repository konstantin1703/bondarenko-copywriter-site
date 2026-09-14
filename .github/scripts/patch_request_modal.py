from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css_old = '<link href="v4.css?v=23" rel="stylesheet"/><link href="v4-locale-v1.css?v=1" rel="stylesheet"/>'
css_new = css_old + '<link href="v4-request-modal-v1.css?v=1" rel="stylesheet"/>'
js_old = '<script defer src="v4.js?v=16"></script><script defer src="v4-locale-v1.js?v=2"></script>'
js_new = js_old + '<script defer src="v4-request-modal-v1.js?v=1"></script>'

if 'v4-request-modal-v1.css' not in s:
    if css_old not in s:
        raise SystemExit('CSS anchor not found')
    s = s.replace(css_old, css_new, 1)

if 'v4-request-modal-v1.js' not in s:
    if js_old not in s:
        raise SystemExit('JS anchor not found')
    s = s.replace(js_old, js_new, 1)

p.write_text(s, encoding='utf-8')
print('request modal assets connected')
