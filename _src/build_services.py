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
        '<script type="application/ld+json">', json.dumps(ld, ensure_ascii=False, indent=1), '</script>', '</head>', '<body>',
        '<header><div class="wrap bar"><a href="../"><img src="../assets/logo/h2_white.svg" alt="MAKE A TEAM 메이커팀" style="height:28px;width:auto;display:block"></a>'
        f'<nav aria-label="분야">{nav}<a href="../guide/">가이드</a><a href="../#contact">문의하기</a></nav></div></header>',
        '<section class="hero"><div class="wrap">',
        f'<p class="crumb"><a href="../">메이커팀</a> › {e(d["title"])}</p>',
        f'<div class="en">{e(d["en"])}</div><h1>{e(d["title"])}</h1><p>{e(d["lead"])}</p>',
        '</div></section>', '<main><div class="wrap">']
    for it in d['items']:
        out.append('<article class="item">'
                   f'<img loading="lazy" src="../{it["img"]}" alt="{e(it["alt"])}">'
                   f'<div><h2>{e(it["name"])}</h2><p class="one">{e(it["one"])}</p><dl>'
                   f'<dt>잘 맞는 행사</dt><dd>{e(", ".join(it["fit"]))}</dd>'
                   '<dt>운영 방식</dt><dd><ul>' + ''.join(f'<li>{e(h)}</li>' for h in it['how']) + '</ul></dd></dl>'
                   f'<a class="ask" href="../#contact">{e(it["name"])} 문의</a></div></article>')
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


for k, d in data.items():
    print(page(k, d))
