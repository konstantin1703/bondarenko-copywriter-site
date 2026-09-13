from pathlib import Path

index = Path('index.html')
css = Path('v4.css')

html = index.read_text(encoding='utf-8')
style = css.read_text(encoding='utf-8')

old_label = 'КАК ЧИТАТЬ ЭТИ ДАННЫЕ'
new_label = 'ЧТО ОПРЕДЕЛЯЮТ ЭТИ ПАРАМЕТРЫ'
if old_label not in html:
    raise SystemExit('tech meaning label not found')
html = html.replace(old_label, new_label, 1)

if 'v4.css?v=17' not in html:
    raise SystemExit('expected css version v17 not found')
html = html.replace('v4.css?v=17', 'v4.css?v=18', 1)

patch = r'''

/* VANTA R1 — Tech Sheet V2 mobile grid cleanup 2026-09 */
.tech-grid-v2 .tech-group{
  overflow:hidden!important;
  isolation:isolate;
}
.tech-grid-v2 .tech-group-head,
.tech-grid-v2 .tech-metric{
  box-shadow:none!important;
}
.tech-grid-v2 .tech-group-head::before,
.tech-grid-v2 .tech-group-head::after,
.tech-grid-v2 .tech-metric::before,
.tech-grid-v2 .tech-metric::after,
.tech-grid-v2 .tech-value::before,
.tech-grid-v2 .tech-value::after{
  content:none!important;
  display:none!important;
}
.tech-grid-v2 .tech-group-head{
  border:0!important;
  border-bottom:1px solid #292c2a!important;
}
.tech-grid-v2 .tech-metric{
  border:0!important;
  border-bottom:1px solid #292c2a!important;
}
.tech-grid-v2 .tech-metric:last-child{
  border-bottom:0!important;
}
.tech-meaning>div>small{
  letter-spacing:.16em!important;
}

@media(max-width:980px){
  .tech-grid-v2 .tech-group{
    grid-template-columns:116px minmax(0,1fr) minmax(0,1fr)!important;
    grid-template-rows:auto!important;
  }
  .tech-grid-v2 .tech-group-head{
    min-width:0!important;
    min-height:150px!important;
    padding:15px 12px!important;
    border:0!important;
    border-right:1px solid #292c2a!important;
    overflow:hidden!important;
  }
  .tech-group-head h3{
    max-width:100%!important;
    font-size:9px!important;
    line-height:1.13!important;
    letter-spacing:.045em!important;
    overflow-wrap:anywhere!important;
  }
  .tech-group-head small{
    font-size:6.2px!important;
    line-height:1.35!important;
    letter-spacing:.14em!important;
  }
  .tech-grid-v2 .tech-metric{
    min-width:0!important;
    min-height:150px!important;
    padding:15px 12px!important;
    border:0!important;
  }
  .tech-grid-v2 .tech-metric + .tech-metric{
    border-left:1px solid #292c2a!important;
  }
  .tech-label{
    font-size:7.7px!important;
    line-height:1.28!important;
    letter-spacing:.055em!important;
  }
  .tech-grid-v2 .tech-metric p{
    font-size:7.5px!important;
    line-height:1.43!important;
  }
}

@media(max-width:390px){
  .tech-grid-v2 .tech-group{
    grid-template-columns:106px minmax(0,1fr) minmax(0,1fr)!important;
  }
  .tech-grid-v2 .tech-group-head,
  .tech-grid-v2 .tech-metric{
    min-height:146px!important;
    padding:13px 10px!important;
  }
  .tech-group-head h3{font-size:8.4px!important}
  .tech-value strong{font-size:34px!important}
}
'''

marker = '/* VANTA R1 — Tech Sheet V2 mobile grid cleanup 2026-09 */'
if marker in style:
    raise SystemExit('cleanup patch already present')
style += patch

index.write_text(html, encoding='utf-8')
css.write_text(style, encoding='utf-8')

print('Tech Sheet cleanup applied')
