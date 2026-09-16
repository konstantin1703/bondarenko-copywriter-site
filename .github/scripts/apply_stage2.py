from pathlib import Path

index = Path('index.html')
html = index.read_text()
link = '<link href="v4-typography-v1.css?v=1" rel="stylesheet"/>'
anchor = '<link href="v4-request-modal-v1.css?v=6" rel="stylesheet"/>'
if link not in html:
    if anchor not in html:
        raise SystemExit('request modal CSS anchor not found')
    html = html.replace(anchor, anchor + link, 1)
    index.write_text(html)

smoke = Path('.github/scripts/smoke_qa.mjs')
s = smoke.read_text()

if "const typographyCss=fs.readFileSync('v4-typography-v1.css','utf8');" not in s:
    s = s.replace(
        "  const modalCss=fs.readFileSync('v4-request-modal-v1.css','utf8');\n",
        "  const modalCss=fs.readFileSync('v4-request-modal-v1.css','utf8');\n  const typographyCss=fs.readFileSync('v4-typography-v1.css','utf8');\n",
        1,
    )

if 'typography cache-bust must be v1' not in s:
    s = s.replace(
        "  expectStatic(html.includes('v4-request-modal-v1.css?v=6'),'request modal CSS cache-bust must be v6');\n",
        "  expectStatic(html.includes('v4-request-modal-v1.css?v=6'),'request modal CSS cache-bust must be v6');\n"
        "  expectStatic(html.includes('v4-typography-v1.css?v=1'),'typography cache-bust must be v1');\n"
        "  expectStatic(typographyCss.includes('Stage 2 / selective functional typography pass'),'stage 2 typography layer missing');\n",
        1,
    )

marker = "    const phoneSemantics=await page.evaluate(()=>{\n"
if 'functional typography below stage-2 floor' not in s:
    block = """    const functionalType=await page.evaluate(()=>{\n      const selectors=[\n        ['config summary label','.config-stats small',8.5],\n        ['config module description','.config-module-copy small',10],\n        ['config module effect','.config-effect',8.5],\n        ['config action','.config-actions button',9]\n      ];\n      return selectors.map(([name,selector,min])=>{\n        const el=document.querySelector(selector);\n        return {name,selector,min,size:el?parseFloat(getComputedStyle(el).fontSize):null};\n      });\n    });\n    const tooSmallFunctional=functionalType.filter(row=>row.size===null||row.size+0.01<row.min);\n    if(tooSmallFunctional.length)fail(scope,`functional typography below stage-2 floor: ${tooSmallFunctional.map(x=>`${x.name}:${x.size}px<${x.min}px`).join(', ')}`);\n\n"""
    if marker not in s:
        raise SystemExit('smoke runtime insertion marker not found')
    s = s.replace(marker, block + marker, 1)

modal_marker = "    if(!modalState.headerInert||!modalState.heroInert)fail(scope,'background is not inert while request modal is open');\n"
if 'request functional typography below stage-2 floor' not in s:
    block = """    const requestType=await page.evaluate(()=>{\n      const selectors=[\n        ['request progress','.request-progress span',9],\n        ['request field label','.request-field>span',9],\n        ['request hint','.field-hint',innerWidth<=600?10:9.5],\n        ['request action','.request-controls button',innerWidth<=600?9.5:9],\n        ['request summary label','.request-summary-head small',8.5]\n      ];\n      return selectors.map(([name,selector,min])=>{\n        const el=document.querySelector(selector);\n        return {name,selector,min,size:el?parseFloat(getComputedStyle(el).fontSize):null};\n      });\n    });\n    const requestTooSmall=requestType.filter(row=>row.size===null||row.size+0.01<row.min);\n    if(requestTooSmall.length)fail(scope,`request functional typography below stage-2 floor: ${requestTooSmall.map(x=>`${x.name}:${x.size}px<${x.min}px`).join(', ')}`);\n    const modalOverflow=await page.evaluate(()=>({sw:document.getElementById('request')?.scrollWidth||0,cw:document.getElementById('request')?.clientWidth||0}));\n    if(modalOverflow.sw>modalOverflow.cw+3)fail(scope,`request modal horizontal overflow ${modalOverflow.sw}px > ${modalOverflow.cw}px`);\n"""
    if modal_marker not in s:
        raise SystemExit('modal runtime insertion marker not found')
    s = s.replace(modal_marker, modal_marker + block, 1)

smoke.write_text(s)
