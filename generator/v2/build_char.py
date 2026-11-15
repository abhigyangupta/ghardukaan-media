"""Derive the character version (commission_char.html) from commission.html."""
s=open('commission.html').read()
def rep(a,b):
    global s
    assert a in s, a[:60]; s=s.replace(a,b,1)
rep('.head{left:0;width:1080px;top:270px','.head{left:0;width:1080px;top:245px')
rep('#pill1{left:50%;top:300px','#pill1{left:50%;top:285px')
rep('#tiles{left:68px;top:560px','#tiles{left:68px;top:500px')
rep('#cut{left:440px;top:545px','#cut{left:440px;top:485px')
rep('#flow{left:68px;top:540px','#flow{left:68px;top:480px')
rep('.stat{left:0;width:1080px;top:850px;text-align:center}','.stat{left:0;width:600px;top:0;height:340px;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center}')
rep(".stat .n{font-weight:800;font-size:230px;line-height:1;letter-spacing:-8px;display:inline-block}",".stat .n{font-weight:800;font-size:138px;line-height:1;letter-spacing:-5px;display:inline-block}")
rep(".stat .s{font-weight:700;font-size:56px;margin-top:10px;opacity:.95}",".stat .s{font-weight:700;font-size:46px;margin-top:8px;color:#422B22}")
rep("#st1 .n{color:var(--gold)} #st2 .n{color:var(--red);font-size:200px} #st3 .n{color:var(--mint);font-size:300px}","#st1 .n{color:#9E3D00} #st2 .n{color:#D4301F;font-size:124px} #st3 .n{color:#15803D;font-size:210px;letter-spacing:-8px}")
rep("#st1{top:850px}\n","#st1{padding-bottom:96px}\n")
rep("#q{left:0;width:1080px;top:1130px;text-align:center;font-weight:800;font-size:92px;letter-spacing:-2px}\n#q em{font-style:normal;color:var(--gold);display:inline-block}",
    "#q{left:0;width:600px;top:212px;text-align:center;font-weight:800;font-size:68px;letter-spacing:-1.5px;color:#422B22}\n#q em{font-style:normal;color:#CC5705;display:inline-block}\n"
    "#bubble{left:452px;top:835px;width:600px;height:340px;border-radius:48px;background:#FFF7EA;box-shadow:0 14px 0 rgba(0,0,0,.28)}\n"
    "#bubble:before{content:'';position:absolute;left:-46px;top:150px;border:30px solid transparent;border-right:52px solid #FFF7EA;border-left:0}\n"
    "#char{left:-90px;top:740px;width:720px;height:660px;-webkit-mask-image:linear-gradient(to bottom,#000 86%,transparent 100%)}")
rep(".note{left:50%;top:1240px;",".note{left:752px;top:1208px;")
rep("font-weight:600;font-size:36px;padding:14px 30px;","font-weight:600;font-size:29px;padding:12px 24px;")
rep('style="top:1282px;background:var(--gold);color:var(--jag);border:0;font-weight:800;font-size:42px;padding:18px 38px"','style="top:1205px;background:var(--gold);color:var(--jag);border:0;font-weight:800;font-size:40px;padding:16px 34px"')
a=s.index('  <div id="st1"'); b=s.index('  <div id="n2"')
stats=s[a:b]
char='''  <svg id="char" class="abs" viewBox="-120 -60 720 660">
    <g id="cbody">
      <path d="M30 600C30 480 100 432 185 418L295 418C380 432 450 480 450 600Z" fill="#B8480E"/>
      <path d="M196 416L240 486L284 416Z" fill="#D9996A"/>
      <path d="M196 416L240 486L284 416" fill="none" stroke="#FFC454" stroke-width="9" stroke-linejoin="round"/>
      <path d="M300 420C352 432 404 458 430 510L452 600L372 600C356 520 330 462 300 420Z" fill="#FFC454"/>
      <g id="armL" transform="translate(78 492)"><g class="up"><path d="M0 0L0 140" stroke="#A53F0B" stroke-width="66" stroke-linecap="round"/>
        <g class="fore" transform="translate(0 140)"><path d="M0 0L0 118" stroke="#E0A476" stroke-width="42" stroke-linecap="round"/><circle cx="0" cy="130" r="31" fill="#E0A476"/><path d="M-14 100L14 100" stroke="#FFC454" stroke-width="10" stroke-linecap="round"/></g></g></g>
      <g id="armR" transform="translate(402 492)"><g class="up"><path d="M0 0L0 140" stroke="#A53F0B" stroke-width="66" stroke-linecap="round"/>
        <g class="fore" transform="translate(0 140)"><path d="M0 0L0 118" stroke="#E0A476" stroke-width="42" stroke-linecap="round"/><circle cx="0" cy="130" r="31" fill="#E0A476"/><path d="M-14 100L14 100" stroke="#FFC454" stroke-width="10" stroke-linecap="round"/></g></g></g>
      <rect x="208" y="330" width="64" height="100" rx="22" fill="#CC8C5E"/>
      <g id="chead">
        <circle cx="240" cy="84" r="54" fill="#2B1A14"/>
        <ellipse cx="240" cy="228" rx="134" ry="142" fill="#2B1A14"/>
        <circle cx="132" cy="262" r="19" fill="#E0A476"/><circle cx="348" cy="262" r="19" fill="#E0A476"/>
        <circle cx="130" cy="296" r="10" fill="#FFC454"/><circle cx="350" cy="296" r="10" fill="#FFC454"/>
        <ellipse cx="240" cy="252" rx="106" ry="124" fill="#E0A476"/>
        <path d="M132 240C132 140 198 116 240 120C282 116 348 140 348 240C332 186 292 160 240 163C188 160 148 186 132 240Z" fill="#2B1A14"/>
        <circle cx="240" cy="194" r="7.5" fill="#C81E1E"/>
        <circle cx="166" cy="296" r="22" fill="#E8725A" opacity=".32"/><circle cx="314" cy="296" r="22" fill="#E8725A" opacity=".32"/>
        <g id="browL"><path d="M176 214Q198 201 222 211" fill="none" stroke="#2B1A14" stroke-width="7.5" stroke-linecap="round"/></g>
        <g id="browR"><path d="M258 211Q282 201 304 214" fill="none" stroke="#2B1A14" stroke-width="7.5" stroke-linecap="round"/></g>
        <g transform="translate(199 248)"><g class="eo"><ellipse rx="13.5" ry="17" fill="#2B1A14"/><circle cx="-4" cy="-6" r="4.5" fill="#fff"/></g><path class="eh" d="M-17 5Q0 -15 17 5" fill="none" stroke="#2B1A14" stroke-width="7.5" stroke-linecap="round"/></g>
        <g transform="translate(281 248)"><g class="eo"><ellipse rx="13.5" ry="17" fill="#2B1A14"/><circle cx="-4" cy="-6" r="4.5" fill="#fff"/></g><path class="eh" d="M-17 5Q0 -15 17 5" fill="none" stroke="#2B1A14" stroke-width="7.5" stroke-linecap="round"/></g>
        <path d="M240 262q-9 24 5 27" fill="none" stroke="#BF7D4F" stroke-width="5" stroke-linecap="round"/>
        <g transform="translate(240 322)"><path id="mouth" d="" fill="#7A2318" stroke="#A33A2B" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/></g>
      </g>
    </g>
  </svg>
'''
s=s[:a]+char+'  <div id="bubble" class="abs">\n'+stats+'  </div>\n'+s[b:]
rep("gsap.set(['#h2', '#h3', '#st2', '#st3', '#n2', '#n3', '#flow', '#q'], { autoAlpha: 0 });",
    "gsap.set(['#h2', '#h3', '#st2', '#st3', '#n2', '#n3', '#flow', '#q'], { autoAlpha: 0 });\n"
    "const P = { aR: 6, eR: 0, aL: -6, eL: 0, browY: 0, tilt: 0, eye: 1, happy: 0, smile: .7, head: 0, by: 0 };\n"
    "const ENV = window.__ENV || [];")
rep("tl.from('#chip', { y: -120, autoAlpha: 0, duration: .6 }, 0)",
    "tl.from('#chip', { y: -120, autoAlpha: 0, duration: .6 }, 0)\n"
    "  .from('#char', { y: 700, duration: .7, ease: 'back.out(1.2)' }, .05)\n"
    "  .from('#bubble', { scale: 0, autoAlpha: 0, transformOrigin: '0% 50%', duration: .45, ease: 'back.out(1.8)' }, s1 + .45)")
rep(".from('#st1', { autoAlpha: 0, y: 60, duration: .4 }, s1 + .6);", ".from('#st1', { autoAlpha: 0, y: 40, duration: .4 }, s1 + .6);")
rep(".to('#st1', { scale: .5, y: -40, autoAlpha: 0", ".to('#st1', { scale: .5, autoAlpha: 0")
rep("tl.to(['#pill1', '#q'], { y: -70, autoAlpha: 0", "tl.to('#q', { autoAlpha: 0, duration: .25 }, s2 - .15).to('#pill1', { y: -70, autoAlpha: 0")
rep(".from('#st2 .n', { scale: 3, autoAlpha: 0", ".from('#st2 .n', { scale: 2.2, autoAlpha: 0")
rep("tl.to(['#h2', '#st2', '#n2'], { y: -60, autoAlpha: 0", "tl.to('#st2', { scale: .5, autoAlpha: 0, duration: .3, ease: 'power2.in' }, s3 - .15).to(['#h2', '#n2'], { y: -60, autoAlpha: 0")
rep(".fromTo('#st3 .n', { color: '#FF6B57' }, { color: '#6FE39A'", ".fromTo('#st3 .n', { color: '#D4301F' }, { color: '#15803D'")
rep("tl.to('#wipe', { scale: 260", "tl.to('#char', { y: 700, duration: .45, ease: 'power2.in' }, s4 - .35)\n  .to('#wipe', { scale: 260")
act = '''
// ---------- Character acting ----------
const qT = M[0].end - 1.5;
tl.to(P, { aR: -112, eR: -42, duration: .5, ease: 'back.out(1.6)' }, s1 + .5)
  .to(P, { browY: -7, duration: .3 }, s1 + .5)
  .to(P, { aR: -62, eR: -86, aL: 62, eL: 86, head: -7, browY: -12, smile: .2, duration: .4, ease: 'back.out(1.8)' }, qT)
  .to(P, { aR: 8, eR: 0, aL: -8, eL: 0, head: 0, browY: 0, duration: .4 }, s2 - .1)
  .to(P, { tilt: 9, smile: -.35, browY: -3, duration: .4 }, s2 + .5)
  .to(P, { aR: -128, eR: -30, duration: .45, ease: 'back.out(1.5)' }, s2 + .9)
  .to(P, { eye: 1.35, tilt: 15, smile: -.9, browY: -12, duration: .2 }, fly + .1)
  .to(P, { head: 6, duration: .12, yoyo: true, repeat: 5, ease: 'sine.inOut' }, fly + .45)
  .to(P, { aR: 10, eR: 0, by: 16, eye: 1, browY: 2, duration: .5 }, fly + .5)
  .to(P, { tilt: 0, smile: 1, browY: -6, by: 0, head: 0, duration: .4, ease: 'back.out(2)' }, s3 + .3)
  .to(P, { aR: -158, eR: -18, aL: 158, eL: 18, happy: 1, duration: .4, ease: 'back.out(2)' }, s3 + 2.15)
  .to(P, { by: -22, duration: .16, yoyo: true, repeat: 3, ease: 'power2.out' }, s3 + 2.15)
  .to(P, { aL: -8, eL: 0, aR: -138, eR: -36, happy: 0, duration: .45 }, mid3 - .1)
  .to(P, { aR: -116, eR: -40, happy: 1, duration: .4 }, mid3 + 1.7);
const blinkAt = [1.4, 3.9, 6.2, 8.9, 11.0, 13.6, 15.4];
const armT = (id, a, e) => { $(id + ' .up').setAttribute('transform', `rotate(${a})`); $(id + ' .fore').setAttribute('transform', `translate(0 140) rotate(${e})`); };
const drawChar = (t) => {
  const f = Math.max(0, Math.min(ENV.length - 1, Math.round(t * 30))); const o = ENV.length ? ENV[f] : 0;
  const bl = blinkAt.some(b => t >= b && t < b + .13) ? .12 : 1;
  const breathe = Math.sin(t * 2.4) * 3, nod = Math.sin(t * 3.1) * 1.2 + o * 2.2;
  $('#cbody').setAttribute('transform', `translate(0 ${P.by + breathe})`);
  $('#chead').setAttribute('transform', `translate(0 ${-breathe * .5 - o * 3}) rotate(${P.head + nod} 240 380)`);
  armT('#armR', P.aR + Math.sin(t * 5) * (P.aR < -40 ? 3 : 0), P.eR); armT('#armL', P.aL, P.eL);
  $('#browL').setAttribute('transform', `translate(0 ${P.browY - o * 3}) rotate(${-P.tilt} 199 210)`);
  $('#browR').setAttribute('transform', `translate(0 ${P.browY - o * 3}) rotate(${P.tilt} 281 210)`);
  $$('#char .eo').forEach(e => { e.setAttribute('transform', `scale(1 ${P.eye * bl})`); e.style.opacity = 1 - P.happy; });
  $$('#char .eh').forEach(e => e.style.opacity = P.happy);
  const s = P.smile, yc = -7 * s, w = 27 - o * 5;
  $('#mouth').setAttribute('d', `M${-w} ${yc}Q0 ${6 * s - 5 * o} ${w} ${yc}Q0 ${17 * s + 46 * o} ${-w} ${yc}Z`);
};
'''
act += """
tl.to('#bubble', { scale: 0, autoAlpha: 0, duration: .25, ease: 'power2.in' }, s2 - .15)
  .to('#bubble', { scale: 1, autoAlpha: 1, duration: .4, ease: 'back.out(1.8)' }, fly + .2)
  .to('#bubble', { scale: 0, autoAlpha: 0, duration: .25, ease: 'power2.in' }, s3 - .15)
  .to('#bubble', { scale: 1, autoAlpha: 1, duration: .4, ease: 'back.out(1.8)' }, s3 + .8);
"""
rep("// ---------- Scene 4: outro ----------", act + "\n// ---------- Scene 4: outro ----------")
rep("  // idle float for tiles", "  drawChar(t);\n  // idle float for tiles")
open('commission_char.html','w').write(s)
