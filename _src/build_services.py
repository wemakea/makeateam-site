"""메이커팀 분야별 서비스 페이지 생성기.
사용: python3 _src/build_services.py  (저장소 루트에서)
원본 데이터: _src/services.json  (업체명 등 내부 정보는 넣지 않는다. 내부 기록은 구글 시트 '홈페이지 반영' 탭)
'_'로 시작하는 폴더라 GitHub Pages(Jekyll)에 공개되지 않는다.
"""
import json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://makeateam.co.kr'
data = json.load(open(os.path.join(ROOT, '_src', 'services.json'), encoding='utf-8'))
NAV = [('event', '행사 프로그램'), ('staff', '행사 인력')]
e = lambda s: html.escape(s, quote=True)


def page(key, d):
    url = f"{BASE}/{d['path']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": f"{d['title']} | 메이커팀", "url": url, "description": d['desc'], "inLanguage": "ko-KR"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "메이커팀", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": d['title'], "item": url}]},
        {"@type": "ItemList", "name": d['title'], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "Service", "name": it['name'], "description": it.get('one') or it.get('text'),
                "provider": {"@type": "Organization", "name": "메이커팀 MAKE A TEAM", "url": BASE + "/"},
                "areaServed": "KR"}}
            for i, it in enumerate(d['items'] + d['more'])]}]}
    nav = ''.join(f'<a href="../{p}/"' + (' aria-current="page"' if p == key else '') + f'>{e(t)}</a>' for p, t in NAV)
    out = [
        '<!doctype html>', '<html lang="ko">', '<head>', '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title>{e(d["title"])}: {e(d["seo_title"])} | 메이커팀</title>',
        f'<meta name="description" content="{e(d["desc"])}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">', '<meta property="og:site_name" content="메이커팀 MAKE A TEAM">',
        f'<meta property="og:title" content="{e(d["title"])} | 메이커팀">', f'<meta property="og:description" content="{e(d["desc"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}/{d["items"][0]["img"]}">',
        '<link rel="icon" href="../favicon.svg" type="image/svg+xml">', '<link rel="stylesheet" href="../assets/svc.css">',
        '<script type="application/ld+json">', json.dumps(ld, ensure_ascii=False, indent=1), '</script>', '<script src="/assets/analytics.js" defer></script>', '</head>', '<body>',
        '<header><div class="wrap bar"><a href="../"><img src="../assets/logo/h2_white.svg" alt="MAKE A TEAM 메이커팀" style="height:28px;width:auto;display:block"></a>'
        f'<nav aria-label="분야">{nav}<a href="../guide/">가이드</a><a href="../#contact">문의하기</a></nav></div></header>',
        '<section class="hero"><div class="wrap">',
        f'<p class="crumb"><a href="../">메이커팀</a> › {e(d["title"])}</p>',
        f'<div class="en">{e(d["en"])}</div><h1>{e(d["title"])}</h1><p>{e(d["lead"])}</p>',
        '</div></section>', '<main><div class="wrap">']
    for it in d['items']:
        title = (f'<h2><a href="{it["slug"]}.html">{e(it["name"])}</a></h2>' if it.get('slug') else f'<h2>{e(it["name"])}</h2>')
        out.append('<article class="item">'
                   f'<img loading="lazy" src="../{it["img"]}" alt="{e(it["alt"])}">'
                   '<div>' + title + f'<p class="one">{e(it["one"])}</p><dl>'
                   f'<dt>잘 맞는 행사</dt><dd>{e(", ".join(it["fit"]))}</dd>'
                   '<dt>운영 방식</dt><dd><ul>' + ''.join(f'<li>{e(h)}</li>' for h in it['how']) + '</ul></dd></dl>'
                   '<div class="links">' + (f'<a href="{it["slug"]}.html">자세히 보기</a>' if it.get('slug') else '') + f'<a href="../#contact">{e(it["name"])} 문의</a></div></div></article>')
    if d['more']:
        out.append('<section class="more"><h2>이런 것도 맡습니다</h2><p>필요한 것만 골라 맡기셔도 됩니다.</p><div class="grid">'
                   + ''.join(f'<div><b>{e(m["name"])}</b><span>{e(m["text"])}</span></div>' for m in d['more'])
                   + '</div>'
                   + (f'<p style="margin-top:24px">준비 방법은 <a href="{d["guide"]["href"]}" style="font-weight:700">{e(d["guide"]["text"])}</a>에서 볼 수 있습니다.</p>' if d.get('guide') else '')
                   + '</section>')
    out += ['</div></main>',
            '<section class="cta"><div class="wrap"><strong>행사 날짜와 장소만 알려 주세요</strong>'
            '<p>규모와 필요한 구성을 확인한 뒤 견적과 운영 계획을 보내드립니다. 계약과 세금계산서는 주식회사 위메이커 명의로 처리합니다.</p>'
            '<a href="../#contact">문의하기</a><a class="kakao" href="https://pf.kakao.com/_xoTWvX/chat" target="_blank" rel="noopener">카카오톡 문의</a></div></section>',
            '<footer><div class="wrap">메이커팀은 주식회사 위메이커가 운영합니다. 부산 본사, 서울 지사. 이메일 mat@wma.co.kr. '
            '<a href="../">홈</a> <a href="../guide/">행사 준비 가이드</a> <a href="../privacy.html">개인정보 처리방침</a></div></footer>',
            '</body>', '</html>', '']
    os.makedirs(os.path.join(ROOT, d['path']), exist_ok=True)
    open(os.path.join(ROOT, d['path'], 'index.html'), 'w', encoding='utf-8').write('\n'.join(out))
    return url


def head(title, desc, url, img, ld, depth='../'):
    return ['<!doctype html>', '<html lang="ko">', '<head>', '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<title>{e(title)}</title>', f'<meta name="description" content="{e(desc)}">', f'<link rel="canonical" href="{url}">',
            '<meta property="og:type" content="website">', '<meta property="og:site_name" content="메이커팀 MAKE A TEAM">',
            f'<meta property="og:title" content="{e(title)}">', f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{BASE}/{img}">',
            f'<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">', f'<link rel="stylesheet" href="{depth}assets/svc.css">',
            '<script type="application/ld+json">', json.dumps(ld, ensure_ascii=False, indent=1), '</script>', '<script src="/assets/analytics.js" defer></script>', '</head>', '<body>']


def header(key):
    nav = ''.join(f'<a href="../{p}/"' + (' aria-current="page"' if p == key else '') + f'>{e(t)}</a>' for p, t in NAV)
    return ('<header><div class="wrap bar"><a href="../"><img src="../assets/logo/h2_white.svg" alt="MAKE A TEAM 메이커팀" style="height:28px;width:auto;display:block"></a>'
            f'<nav aria-label="분야">{nav}<a href="../guide/">가이드</a><a href="../#contact">문의하기</a></nav></div></header>')


TAIL = ['<section class="cta"><div class="wrap"><strong>행사 날짜와 장소만 알려 주세요</strong>'
        '<p>규모와 필요한 구성을 확인한 뒤 견적과 운영 계획을 보내드립니다. 계약과 세금계산서는 주식회사 위메이커 명의로 처리합니다.</p>'
        '<a href="../#contact">문의하기</a><a class="kakao" href="https://pf.kakao.com/_xoTWvX/chat" target="_blank" rel="noopener">카카오톡 문의</a></div></section>',
        '<footer><div class="wrap">메이커팀은 주식회사 위메이커가 운영합니다. 부산 본사, 서울 지사. 이메일 mat@wma.co.kr. '
        '<a href="../">홈</a> <a href="../guide/">행사 준비 가이드</a> <a href="../privacy.html">개인정보 처리방침</a></div></footer>',
        '</body>', '</html>', '']


def detail(key, d, it, by_name):
    dt = it['detail']
    url = f"{BASE}/{d['path']}/{it['slug']}.html"
    cat_url = f"{BASE}/{d['path']}/"
    desc = dt['intro'][:150]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": it['name'], "description": dt['intro'], "serviceType": d['title'], "url": url,
         "image": f"{BASE}/{it['img']}", "areaServed": "KR",
         "provider": {"@type": "Organization", "name": "메이커팀 MAKE A TEAM", "url": BASE + "/",
                      "parentOrganization": {"@type": "Organization", "name": "주식회사 위메이커", "url": "https://wma.co.kr/"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "메이커팀", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": d['title'], "item": cat_url},
            {"@type": "ListItem", "position": 3, "name": it['name'], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in dt['faq']]}]}
    out = head(f"{it['name']} | {d['title']} | 메이커팀", desc, url, it['img'], ld)
    out += [header(key),
            '<section class="hero"><div class="wrap">',
            f'<p class="crumb"><a href="../">메이커팀</a> › <a href="./">{e(d["title"])}</a> › {e(it["name"])}</p>',
            f'<div class="en">{e(d["en"])}</div><h1>{e(it["name"])}</h1><p>{e(it["one"])}</p>',
            '</div></section>',
            '<main><div class="wrap dt">', f'<img class="dt-hero" src="../{it["img"]}" alt="{e(it["alt"])}">', f'<p class="intro">{e(dt["intro"])}</p>']
    for sec in dt['sections']:
        out.append(f'<h2>{e(sec["h"])}</h2>')
        if 'table' in sec:
            h, *rows = sec['table']
            out.append('<div class="tw"><table><thead><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' for c in h) + '</tr></thead><tbody>'
                       + ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
        for tag in ('ul', 'ol'):
            if tag in sec:
                out.append(f'<{tag}>' + ''.join(f'<li>{e(x)}</li>' for x in sec[tag]) + f'</{tag}>')
        if 'p' in sec:
            out.append(f'<p>{e(sec["p"])}</p>')
    out.append('<h2>자주 묻는 질문</h2>')
    out += [f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in dt['faq']]
    rel = [by_name[n] for n in dt.get('related', []) if n in by_name and by_name[n].get('slug')]
    links = ''.join(f'<a href="../{r["_path"]}/{r["slug"]}.html">{e(r["name"])}</a>' for r in rel)
    links += f'<a href="./">{e(d["title"])} 전체 보기</a>'
    if dt.get('guide'):
        links += f'<a href="{dt["guide"][0]}">{e(dt["guide"][1])}</a>'
    out += ['<h2>함께 보면 좋은 서비스</h2>', f'<div class="rel">{links}</div>', '</div></main>'] + TAIL
    open(os.path.join(ROOT, d['path'], it['slug'] + '.html'), 'w', encoding='utf-8').write('\n'.join(out))
    return url


by_name = {}
for k, d in data.items():
    for it in d['items']:
        it['_path'] = d['path']; by_name[it['name']] = it
urls = []
for k, d in data.items():
    urls.append(page(k, d))
    for it in d['items']:
        if it.get('detail'):
            urls.append(detail(k, d, it, by_name))
print('\n'.join(urls))
open(os.path.join(ROOT, '_src', 'urls.txt'), 'w').write('\n'.join(urls) + '\n')
