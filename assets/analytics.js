/* 메이커팀 방문·문의 측정. 광고 매체 스크립트(네이버·카카오)도 받으면 여기에 추가한다. */
(function () {
  var GA = 'G-YH21S891TE';
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA);
  // 구글 애즈 전환: (주)위메이커 계정 전환 액션 '문의 클릭·접수(카톡·전화·메일·양식)' (2026-11-27)
  var AW = 'AW-16592913405';
  var AW_LEAD = AW + '/T557CJ36rsAdEP2Hj-g9';
  gtag('config', AW);
  function adsLead() { gtag('event', 'conversion', { send_to: AW_LEAD }); }

  // 카카오톡 상담·메일·전화 클릭을 문의 행동으로 기록
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('pf.kakao.com') > -1) { gtag('event', 'kakao_chat_click', { page_path: location.pathname }); adsLead(); }
    else if (h.indexOf('mailto:') === 0) { gtag('event', 'email_click', { page_path: location.pathname }); adsLead(); }
    else if (h.indexOf('tel:') === 0) { gtag('event', 'phone_click', { page_path: location.pathname }); adsLead(); }
  }, true);

  // 홈페이지 문의 양식 접수 완료
  window.matTrackLead = function () { gtag('event', 'generate_lead', { form: 'contact' }); adsLead(); };
})();
