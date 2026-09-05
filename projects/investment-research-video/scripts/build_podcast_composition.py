#!/usr/bin/env python3
"""Build a company-agnostic HyperFrames podcast composition from episode.json and segments.json."""
import argparse, html, json, re, shutil
from pathlib import Path

CSS=r'''
*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#f7f9fc;color:#10213d;font-family:Arial,"Noto Sans SC","Microsoft YaHei",sans-serif}@font-face{font-family:"Noto Sans SC";src:local("Noto Sans CJK SC"),local("Microsoft YaHei")}@font-face{font-family:"Microsoft YaHei";src:local("Microsoft YaHei"),local("Noto Sans CJK SC")}#root{position:relative;width:1920px;height:1080px;background:#f7f9fc}.header{position:absolute;left:80px;right:80px;top:34px;height:82px;border-bottom:1px solid #dce3ed;display:flex;align-items:center;justify-content:space-between}.show{font-size:26px;font-weight:900;color:#173d78}.show small{font-size:18px;margin-left:16px;color:#4e6c98}.disclaimer{font-size:16px;color:#4f5e74;text-align:right;line-height:1.5}.topic-layer{position:absolute;inset:0}.title{position:absolute;left:80px;top:145px;font-size:54px;font-weight:900;color:#101820}.title .index{color:#d17c1d;margin-right:18px}.subtitle{position:absolute;left:80px;top:225px;font-size:28px;font-weight:700;color:#2166d1}.metrics{position:absolute;left:80px;right:80px;top:300px;height:235px;display:flex;gap:24px}.metric{flex:1;background:white;border-radius:18px;padding:24px 30px;box-shadow:0 8px 0 #e8edf4;border-top:6px solid #2166d1}.metric.red{border-color:#d52b2b}.metric.green{border-color:#1d9a58}.metric.orange{border-color:#d17c1d}.metric.blue{border-color:#2166d1}.metric .label{font-size:20px;color:#5d5d5d}.metric .value{font-size:62px;font-weight:900;margin:14px 0 6px}.metric .desc{font-size:20px;color:#47566d}.speaker{position:absolute;left:80px;top:575px;width:220px;height:90px;border-radius:45px;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:900;color:#13213b;background:var(--speaker-bg,#e4a33d)}.caption{position:absolute;left:160px;right:160px;bottom:137px;text-align:center;font-size:31px;font-weight:900;color:var(--speaker-accent,#6e43b5);text-shadow:1px 1px #fff}.turn{position:absolute;inset:0}.turn .speaker{top:735px}.turn .caption{bottom:137px}.chart-zone{position:absolute;left:80px;right:80px;top:555px;height:180px;background:#fff;border-radius:16px;padding:16px 28px;box-shadow:0 8px 0 #e8edf4;border-top:5px solid #2166d1}.chart-title{font-size:18px;font-weight:800;color:#243653;margin-bottom:8px}.chart-row{display:flex;align-items:center;gap:14px;height:32px;font-size:16px}.chart-row>span{width:150px}.chart-track{height:12px;flex:1;background:#e5eaf2;border-radius:8px;overflow:hidden}.chart-track i{display:block;height:100%;background:var(--chart-color,#2166d1);border-radius:8px}.chart-row b{width:80px;text-align:right}.validation{display:flex;gap:14px;align-items:center}.validation-item{flex:1;border-left:4px solid #e88920;padding:16px;background:#fbfcfe}.validation-item b,.validation-item span{display:block}.validation-item span{margin-top:8px;color:#5d5d5d}.agenda-zone{position:absolute;left:80px;right:80px;top:555px;height:150px;background:#fff;border-radius:16px;padding:18px 28px;box-shadow:0 8px 0 #e8edf4;border-top:5px solid #d17c1d}.agenda-label{font-size:18px;font-weight:900;color:#243653;margin-bottom:12px}.agenda-items{display:flex;flex-wrap:wrap;gap:10px 12px}.agenda-item{font-size:18px;color:#173d78;background:#f1f5fb;border-radius:14px;padding:8px 14px}.svg-chart{width:100%;height:115px;display:block}.chart-footnote{font-size:13px;color:#6a778a;margin-top:3px}
@font-face{font-family:"__DISPLAY_FONT__";src:url("assets/fonts/__DISPLAY_REGULAR__") format("opentype");font-weight:400}@font-face{font-family:"__DISPLAY_FONT__";src:url("assets/fonts/__DISPLAY_BOLD__") format("opentype");font-weight:700}@font-face{font-family:"Source Han Serif SC";src:local("Source Han Serif SC"),local("Source Han Serif CN")}@font-face{font-family:"Songti SC";src:local("Songti SC"),local("STSong") }@font-face{font-family:"STSong";src:local("STSong"),local("Songti SC")}
'''

CSS += r''' .topic-nav{position:absolute;left:80px;right:80px;bottom:35px;height:62px;border-top:1px solid #dce3ed;display:flex;align-items:end;gap:12px;color:#4f5e74;font-size:17px;white-space:nowrap}.topic-nav span{padding:8px 10px}.topic-nav .active{background:#2166d1;color:#fff;border-radius:18px;padding:8px 16px}.progress{position:absolute;left:80px;right:80px;bottom:102px;height:5px;background:#e1e7f0;border-radius:5px}.progress-fill{height:100%;background:#2166d1;border-radius:5px}'''
CSS += r''' :root{--speaker-bg:#f3efe6;--speaker-accent:#a6192e;--chart-color:#a6192e}@font-face{font-family:"Noto Sans SC";src:url("assets/fonts/NotoSerifSC-Regular.otf") format("opentype");font-weight:400}@font-face{font-family:"Microsoft YaHei";src:url("assets/fonts/NotoSerifSC-Regular.otf") format("opentype");font-weight:400}@font-face{font-family:"Source Han Serif SC";src:url("assets/fonts/NotoSerifSC-Regular.otf") format("opentype");font-weight:400}@font-face{font-family:"Songti SC";src:url("assets/fonts/NotoSerifSC-Regular.otf") format("opentype");font-weight:400}@font-face{font-family:"STSong";src:url("assets/fonts/NotoSerifSC-Regular.otf") format("opentype");font-weight:400}.metrics{min-height:0;overflow:hidden}.metric{min-width:0;min-height:0;overflow:hidden;padding:12px 24px;box-shadow:none}.metric .label,.metric .value,.metric .desc{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.metric .value{height:80px;line-height:1.25}.metric .desc{line-height:1.15}'''
CSS += r''' .header-brand{display:flex;align-items:center;gap:18px}.account-logo{width:142px;height:54px;object-fit:contain;object-position:left center}.account-avatar{width:46px;height:46px;border-radius:50%;object-fit:cover;border:2px solid #d17c1d}.disclaimer{display:flex;align-items:center;gap:14px;justify-content:flex-end}'''
CSS += r''' .topic-nav{gap:6px;font-size:14px}.topic-nav span{padding:6px 5px}.topic-nav .active{padding:6px 8px}'''
CSS += r''' .topic-nav{position:absolute;left:80px;right:80px;bottom:35px;height:62px;border-top:1px solid #dce3ed;display:flex;align-items:end;gap:6px;color:#4f5e74;font-size:14px;white-space:nowrap}.topic-nav span{padding:6px 5px}.topic-nav .active{background:#2166d1;color:#fff;border-radius:18px;padding:6px 8px}.progress{position:absolute;left:80px;right:80px;bottom:102px;height:5px;background:#e1e7f0;border-radius:5px}.progress-fill{height:100%;background:#2166d1;border-radius:5px}.chart-track{position:relative}.chart-track em{position:absolute;top:-4px;width:3px;height:20px;background:#d17c1d;transform:translateX(-50%)}.risk-matrix{position:relative;height:105px;margin:4px 24px;background:linear-gradient(90deg,#d5f0df 0 33%,#fff1c6 33% 66%,#f5d2d2 66%);border:1px solid #dce3ed}.risk-matrix i{position:absolute;left:50%;top:0;bottom:0;border-left:1px dashed #8793a5}.risk-matrix:after{content:"";position:absolute;left:0;right:0;top:50%;border-top:1px dashed #8793a5}.risk-matrix span{position:absolute;width:15px;height:15px;border-radius:50%;background:#2166d1;border:3px solid #fff;box-shadow:0 1px 4px #8793a5;transform:translate(-50%,-50%)}.flow-map{position:relative;height:105px}.flow-node{position:absolute;top:32px;width:128px;text-align:center;padding:12px 8px;background:#eef4ff;border:1px solid #aac5ef;border-radius:12px;font-weight:800}.flow-node:not(:last-child):after{content:"→";position:absolute;left:135px;top:8px;font-size:25px;color:#2166d1}'''
CSS += r''' .metric.pink{border-color:#e998be} .chart-title small{font-size:13px;font-weight:600;color:#6a778a}.chart-stage{position:absolute;inset:0}'''
CSS += r''' .show,.title,.metric .value,.speaker,.caption{font-family:"__DISPLAY_FONT__","Source Han Serif SC","Songti SC","STSong",serif}.title{letter-spacing:.01em}.caption{-webkit-text-stroke:.18px currentColor}'''
CSS += r''' .nav-state{position:absolute;inset:0;z-index:20;pointer-events:none}.persistent-nav{position:absolute;left:48px;right:48px;bottom:8px;height:34px;color:rgba(20,36,58,.72);font-size:12px}.chapter-strip{position:absolute;left:0;right:0;bottom:9px;height:18px;display:flex;overflow:hidden;border-radius:9px;background:rgba(255,255,255,.24);border:1px solid rgba(20,36,58,.14);backdrop-filter:blur(6px)}.chapter{display:flex;align-items:center;justify-content:center;min-width:1px;overflow:hidden;border-right:1px solid rgba(20,36,58,.14);white-space:nowrap}.chapter b{font-size:11px;font-weight:700;opacity:.72}.chapter.active{background:rgba(33,102,209,.18);color:#173d78}.persistent-progress{position:absolute;left:0;right:0;bottom:0;height:2px;background:rgba(20,36,58,.16)}.persistent-progress-fill{height:100%;background:rgba(20,36,58,.52)}'''
CSS += r''' .caption-line{position:absolute;left:160px;right:160px;bottom:84px;text-align:center;font-size:31px;font-weight:900;color:var(--speaker-accent,#6e43b5);text-shadow:1px 1px #fff}.caption,.turn .caption{bottom:84px}
.cover-scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:10;background:inherit}
.cover-company{font-size:52px;font-weight:900;letter-spacing:6px;margin-bottom:40px}
.cover-title{font-size:80px;font-weight:900;line-height:1.2;text-align:center;margin-bottom:24px}
.cover-subtitle{font-size:32px;font-weight:400;opacity:.7}.chart-stack{position:absolute;left:80px;right:80px;top:555px;height:220px;display:grid;grid-template-columns:1fr 1fr;gap:20px}.chart-stack .chart-zone{position:relative;left:auto;right:auto;top:auto;height:220px}.chart-stack .chart-zone.validation{display:block}'''
CSS += r''' .agenda-zone{height:224px}.agenda-items{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px 16px}.agenda-item{min-width:0;display:flex;align-items:flex-start;background:#f1f5fb;border-left:4px solid #d17c1d;border-radius:8px;padding:11px 14px;font-size:20px;line-height:1.25}.agenda-item b{color:#d17c1d;margin-right:10px;flex:none}.summary-zone{position:absolute;left:80px;right:80px;top:300px;height:330px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}.summary-card{position:relative;background:#fff;border-radius:18px;padding:26px 28px;box-shadow:0 8px 0 #e8edf4;border-top:7px solid #2166d1}.summary-card:nth-child(2){border-color:#d17c1d}.summary-card:nth-child(3){border-color:#d52b2b}.summary-card .kicker{font-size:20px;color:#5d6b7d}.summary-card .headline{font-size:34px;font-weight:900;margin:28px 0 12px;color:#10213d}.summary-card .detail{font-size:21px;line-height:1.45;color:#47566d}.summary-footer{position:absolute;left:80px;right:80px;top:690px;padding:22px 28px;border-left:6px solid #d17c1d;background:#fff8eb;color:#6b4918;font-size:27px;font-weight:800}.motion-rule{transform-origin:left center}.topic-layer:after{content:"";position:absolute;right:80px;top:132px;width:180px;height:2px;background:#d17c1d;transform-origin:left center;opacity:.75}'''

EDITORIAL_PAPER_CSS = r'''
/* editorial-paper: warm financial editorial, adapted from the validated Maotai report direction */
html,body{background:#faf7f1;color:#211d18}
#root{background:#faf7f1}
#root:before{content:"";position:absolute;inset:0;pointer-events:none;z-index:0;opacity:.12;background-image:radial-gradient(rgba(80,50,25,.28) .7px,transparent .8px);background-size:9px 9px}
.header{border-bottom:3px solid #211d18;box-shadow:0 5px 0 #e7e0d2}
.header-brand{display:flex;align-items:center;gap:18px}.account-logo{width:142px;height:54px;object-fit:contain;object-position:left center;mix-blend-mode:multiply}.account-avatar{width:46px;height:46px;border-radius:50%;object-fit:cover;border:2px solid #a6192e}
.show{color:#211d18}.show small{color:#6a6354}.disclaimer{color:#6a6354}
.title{color:#211d18}.title .index{color:#a6192e}.subtitle{color:#6a6354;font-weight:600}
.metric,.metric.red,.metric.green,.metric.orange,.metric.blue,.metric.pink{background:#fffdf8;border-color:#e7e0d2;border-top:4px solid #a6192e;border-radius:2px;box-shadow:none}
.metric.red{border-top-color:#a6192e}.metric.green{border-top-color:#1e6b4c}.metric.orange{border-top-color:#8a5e15}.metric.blue{border-top-color:#a6192e}.metric.pink{border-top-color:#a6192e}
.metric .label{color:#6a6354}.metric .value{color:#211d18}.metric .desc{color:#6a6354}
.speaker{width:auto;height:64px;padding:0 24px;border-radius:2px;border-left:5px solid var(--speaker-accent,#a6192e);background:#f3efe6;color:#211d18;justify-content:flex-start}
.caption{color:var(--speaker-accent,#a6192e);text-shadow:none}
.chart-zone{background:#fffdf8;border:1px solid #e7e0d2;border-top:3px solid #211d18;border-radius:2px;box-shadow:none}
.chart-title{color:#211d18}.chart-title small{color:#6a6354}.chart-track{background:#eadfca;border-radius:0}.chart-track i{border-radius:0}.chart-row{color:#211d18}.chart-row b{color:#211d18}
.validation-item{border-left:0;border-top:3px solid #8a5e15;padding:16px;background:#f3efe6}.validation-item span{color:#6a6354}
.agenda-zone{background:#fffdf8;border:1px solid #e7e0d2;border-top:3px solid #a6192e;border-radius:2px;box-shadow:none}.agenda-label{color:#211d18}.agenda-item{color:#211d18;background:transparent;border-left:0;border-bottom:1px solid #e7e0d2;border-radius:0;padding:11px 8px}.agenda-item b{color:#a6192e}
.summary-card{background:#fffdf8;border:1px solid #e7e0d2;border-top:4px solid #a6192e;border-radius:2px;box-shadow:none}.summary-card:nth-child(2){border-top-color:#8a5e15}.summary-card:nth-child(3){border-top-color:#1e6b4c}.summary-card .kicker,.summary-card .detail{color:#6a6354}.summary-card .headline{color:#211d18;font-family:"__DISPLAY_FONT__","Source Han Serif SC","Songti SC","STSong",serif}
.summary-footer{border-left:0;border-top:3px solid #a6192e;background:#f3efe6;color:#211d18}
.cover-scene .cover-company{color:#a6192e;letter-spacing:8px}.cover-scene .cover-title{color:#211d18;font-family:"__DISPLAY_FONT__","Source Han Serif SC","Songti SC","STSong",serif}.cover-scene .cover-subtitle{color:#6a6354}
.topic-layer:after{background:#a6192e}
.persistent-nav{color:#6a6354}.chapter-strip{border-radius:0;background:transparent;border:0;border-top:1px solid #e7e0d2}.chapter{border-right:1px solid #e7e0d2}.chapter.active{background:transparent;color:#a6192e;border-bottom:3px solid #a6192e}.persistent-progress{background:#e7e0d2}.persistent-progress-fill{background:#a6192e}
.progress{background:#e7e0d2;border-radius:0}.progress-fill{background:#a6192e;border-radius:0}
.risk-matrix{border-color:#e7e0d2}.flow-node{background:#f3efe6;border-color:#c9c0ae;border-radius:2px}.flow-node:not(:last-child):after{color:#a6192e}
'''

STYLE_PALETTES = {
    'default': {
        'primary': '#2166d1', 'secondary': '#d17c1d', 'up': '#d52b2b',
        'down': '#1d9a58', 'positive': '#1d9a58', 'negative': '#d52b2b',
        'neutral': '#c8d9f5', 'grid': '#dce3ed',
    },
    'editorial-paper': {
        'primary': '#a6192e', 'secondary': '#8a5e15', 'up': '#a6192e',
        'down': '#1e6b4c', 'positive': '#1e6b4c', 'negative': '#a6192e',
        'neutral': '#c9c0ae', 'grid': '#e7e0d2',
    },
}


def css_for_style(style, font_family):
    css = CSS + (EDITORIAL_PAPER_CSS if style == 'editorial-paper' else '')
    css = re.sub(r'@font-face\{font-family:"(?:Noto Sans SC|Microsoft YaHei|Source Han Serif SC|Songti SC|STSong)"[^}]*src:local[^}]*\}', '', css)
    return css.replace('__DISPLAY_FONT__', html.escape(font_family))


def reference_cover_html(font_css, account_name, cover_subject, cover_subtitle, cover_title_html, mark_file):
    """Build the light editorial-paper cover direction distilled from the account reference cover."""
    template = r'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1440,height=1080"><style>__FONT_CSS__
*{box-sizing:border-box}html,body{margin:0;width:1440px;height:1080px;overflow:hidden;background:#f3ede3;color:#171719}.cover{position:relative;width:1440px;height:1080px;overflow:hidden;background:#f3ede3;font-family:"__DISPLAY_FONT__","Source Han Serif SC","Songti SC",serif}.cover:before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 34%,rgba(255,252,245,.98) 0%,rgba(248,242,232,.94) 48%,rgba(224,211,195,.92) 100%),linear-gradient(115deg,#e7ddd0,#faf6ef 44%,#ddd0bf)}.cover:after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(rgba(95,73,49,.18) .55px,transparent .8px),radial-gradient(rgba(255,255,255,.75) .6px,transparent .9px),radial-gradient(ellipse at center,transparent 60%,rgba(88,65,45,.17) 100%);background-size:7px 7px,11px 11px,auto;mix-blend-mode:multiply;opacity:.3}.ledger{position:absolute;inset:0;z-index:1;opacity:.3;background-image:linear-gradient(rgba(118,97,72,.22) 1px,transparent 1px),linear-gradient(90deg,rgba(118,97,72,.17) 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(90deg,black 0 12%,transparent 12% 88%,black 88% 100%)}.side{position:absolute;top:86px;bottom:370px;width:156px;z-index:2;border-right:1px solid rgba(118,97,72,.28);border-left:1px solid rgba(118,97,72,.16);color:#6e655b;font-family:"Noto Sans SC","Source Han Sans SC",sans-serif;font-size:18px;line-height:2.8;letter-spacing:.28em;text-align:center;writing-mode:vertical-rl}.side.left{left:0}.side.right{right:0;border-left:1px solid rgba(118,97,72,.28);border-right:0}.brand{position:absolute;left:50%;top:54px;transform:translateX(-50%);z-index:4;display:flex;align-items:center;gap:24px;color:#171719}.cover-brand-mark{width:92px;height:92px;object-fit:contain}.brand-wordmark{font-size:74px;line-height:1;font-weight:700;letter-spacing:.18em;white-space:nowrap}.brand-tag{position:absolute;left:50%;top:154px;transform:translateX(-50%);z-index:4;color:#252124;font-size:25px;letter-spacing:.42em;white-space:nowrap}.rule{position:absolute;left:310px;right:310px;top:202px;height:1px;background:#373234;z-index:4}.rule:after{content:"";position:absolute;right:0;top:7px;width:92px;height:4px;background:#762532}.subject{position:absolute;left:180px;right:180px;top:267px;z-index:4;text-align:center;font-size:42px;line-height:1.1;letter-spacing:.13em;font-weight:700;white-space:nowrap}.title{position:absolute;left:175px;right:175px;top:350px;z-index:4;text-align:center;font-size:184px;line-height:.98;letter-spacing:.04em;font-weight:700}.title .wine{color:#762532}.title .qm{display:inline-block;width:auto;margin-right:-0.521em}/* 全角「？」墨迹只画在字身左半，负外边距抵消空字身，避免标题视觉左偏（Noto Serif SC Bold 实测 -0.521em） */.subline{position:absolute;left:50%;top:657px;transform:translateX(-50%);z-index:4;display:flex;align-items:center;gap:22px;font-size:27px;letter-spacing:.24em;white-space:nowrap}.subline:before,.subline:after{content:"";width:128px;height:1px;background:#4a4541}.subline:after{background:#762532}.desk{position:absolute;left:0;right:0;bottom:0;height:352px;z-index:2;background:linear-gradient(178deg,rgba(228,215,198,.2),rgba(157,113,75,.35) 66%,rgba(85,54,31,.62));overflow:hidden}.paper-back{position:absolute;left:190px;top:70px;width:1050px;height:400px;background:linear-gradient(170deg,#faf6ef,#e6d9c9);border:1px solid rgba(110,83,56,.2);transform:rotate(-8deg);box-shadow:0 20px 30px rgba(73,46,25,.2)}.paper-back:after{content:"";position:absolute;inset:38px 70px;background-image:linear-gradient(rgba(118,97,72,.18) 1px,transparent 1px),linear-gradient(90deg,rgba(118,97,72,.13) 1px,transparent 1px);background-size:50px 32px;opacity:.5}.paper-front{position:absolute;left:218px;top:104px;width:920px;height:350px;background:linear-gradient(164deg,#fffaf2,#ece1d2);transform:rotate(-4deg);box-shadow:0 25px 42px rgba(57,37,22,.28);border:1px solid rgba(114,87,60,.18)}.paper-front:before{content:"";position:absolute;left:90px;top:80px;width:90px;height:90px;background:linear-gradient(90deg,#171719 0 49%,#762532 50%);clip-path:polygon(0 20%,50% 0,100% 20%,100% 80%,50% 100%,0 80%);opacity:.82}.paper-front:after{content:"FINANCIAL  RESEARCH";position:absolute;left:84px;top:190px;color:#8a7c6d;font-family:Georgia,serif;font-size:16px;letter-spacing:.3em}.pen{position:absolute;right:-90px;bottom:-12px;width:430px;height:42px;border-radius:30px;background:linear-gradient(#1a1a1b,#080809);transform:rotate(-24deg);box-shadow:0 9px 17px rgba(0,0,0,.34)}.pen:after{content:"";position:absolute;right:26px;top:0;width:18px;height:42px;background:#9b7136;box-shadow:14px 0 0 #252525}.desk:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(255,250,240,.42),transparent 45%);pointer-events:none}
@media(max-width:1200px){html,body,.cover{width:1080px;height:1440px}.side{top:90px;bottom:480px;width:92px;font-size:15px}.brand{top:54px;gap:18px}.cover-brand-mark{width:72px;height:72px}.brand-wordmark{font-size:58px}.brand-tag{top:142px;font-size:20px}.rule{left:150px;right:150px;top:205px}.subject{left:74px;right:74px;top:282px;font-size:30px;letter-spacing:.12em}.title{left:55px;right:55px;top:365px;font-size:135px;line-height:1.02}.subline{top:720px;font-size:22px;gap:14px}.subline:before,.subline:after{width:90px}.desk{height:570px}.paper-back{left:88px;top:120px;width:920px;height:470px}.paper-front{left:112px;top:170px;width:820px;height:420px}.pen{right:-120px;bottom:26px}}
</style></head><body><main class="cover"><div class="ledger"></div><div class="side left">财报<br>订单<br>现金流<br>产业<br>—</div><div class="side right">数据<br>市场<br>公司<br>价值<br>—</div><div class="brand"><img class="cover-brand-mark" src="assets/__MARK_FILE__" alt=""><div class="brand-wordmark">账本两面</div></div><div class="brand-tag">看懂数字背后的公司</div><div class="rule"></div><div class="subject">__SUBJECT__</div><h1 class="title">__TITLE__</h1><div class="subline">__SUBTITLE__</div><div class="desk"><div class="paper-back"></div><div class="paper-front"></div><div class="pen"></div></div></main></body></html>'''
    return (template.replace('__FONT_CSS__', font_css)
            .replace('__DISPLAY_FONT__', 'NotoSerifSC')
            .replace('__MARK_FILE__', html.escape(mark_file))
            .replace('__SUBJECT__', html.escape(cover_subject))
            .replace('__TITLE__', cover_title_html)
            .replace('__SUBTITLE__', html.escape(cover_subtitle)))

def metric_cards(metrics):
    if not metrics:
        return ''
    cards=[]
    normalized=[]
    for metric in metrics[:3]:
        if isinstance(metric,dict):
            normalized.append((metric.get('label',''),metric.get('display_value',metric.get('value','')),metric.get('display_desc',metric.get('desc','')),metric.get('color','blue')))
        else:
            normalized.append(tuple(metric))
    for label,value,desc,color in (normalized+[('', '', '', 'blue')]*3)[:3]:
        value_text=str(value)
        match=re.match(r'^([+-]?\d+(?:\.\d+)?)(.*)$', value_text)
        count_attrs=''
        if match:
            numeric=match.group(1)
            decimals=len(numeric.split('.',1)[1]) if '.' in numeric else 0
            count_attrs=f' data-count-target="{html.escape(numeric)}" data-count-decimals="{decimals}" data-count-suffix="{html.escape(match.group(2))}"'
        cards.append(f'<div class="metric {html.escape(str(color))}"><div class="label">{html.escape(str(label))}</div><div class="value"{count_attrs}>{html.escape(value_text)}</div><div class="desc">{html.escape(str(desc))}</div></div>')
    return ''.join(cards)

def validate_metric_semantics(topic_id, metrics):
    """Stop generic placeholder cards from reaching a rendered episode.

    A metric card may be qualitative, but three cards with the same filler
    value (for example, ``观察``) carry no topic information and usually mean
    the manifest generator substituted a default.  Repeated values remain
    available when the manifest explicitly marks ``allow_repeated_value``.
    """
    if not isinstance(metrics, list) or len(metrics) < 3:
        return
    values = []
    for metric in metrics[:3]:
        if isinstance(metric, dict):
            values.append(str(metric.get('display_value', metric.get('value', ''))).strip())
        elif isinstance(metric, (list, tuple)) and len(metric) >= 2:
            values.append(str(metric[1]).strip())
    placeholders = {'观察', '指标', '数据', '待填写', '暂无'}
    if len(values) == 3 and len(set(values)) == 1 and values[0] in placeholders:
        raise SystemExit(f"{topic_id} has three placeholder metric values ({values[0]}); provide topic-specific values")

def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def chart_markup(specs, style='default'):
    if not specs:
        return ''
    palette = STYLE_PALETTES.get(style, STYLE_PALETTES['default'])
    if len(specs)>1:
        return f'<div class="chart-stack">{"".join(chart_markup([spec], style) for spec in specs[:2])}</div>'
    spec=specs[0]; rows=spec.get('data',[]); chart_type=spec.get('type','horizontal-bar')
    # Keep semantic chart names in manifest while mapping them to the
    # renderer's proven primitives. This prevents valid company-specific
    # scene plans from silently producing empty chart zones.
    chart_type = {
        'flow': 'flow-map',
        'network': 'flow-map',
        'progression': 'validation-dashboard',
        'funnel': 'validation-dashboard',
        'milestone': 'validation-dashboard',
        'checklist': 'validation-dashboard',
    }.get(chart_type, chart_type)
    claim=html.escape(str(spec.get('claim', '')))
    unit=html.escape(str(spec.get('unit', '')))
    title=f'{claim} <small>（{unit}）</small>' if unit else claim
    if chart_type in ('dumbbell','diverging-bar','horizontal-bar','bar'):
        maximum=max([abs(number(r.get('value',0))) for r in rows] or [1])
        items=[]
        for index,row in enumerate(rows):
            value=number(row.get('value',0)); width=max(4,round(abs(value)/maximum*100,1)); label=html.escape(str(row.get('label',''))); val=html.escape(str(row.get('value','')))
            color=palette['down'] if value < 0 else palette['up']
            items.append(f'<div class="chart-row"><span>{label}</span><div class="chart-track"><i style="--chart-color:{color};width:{width}%"></i></div><b>{val}</b></div>')
        return f'<div class="chart-zone"><div class="chart-title">{title}</div>{"".join(items)}</div>'
    if chart_type in ('line','multiline','step-line'):
        series=[]
        for index,row in enumerate(rows):
            values=row.get('values', row.get('data', [])) if isinstance(row,dict) else []
            if not values and 'value' in row: values=[row]
            points=[]
            for point_index,point in enumerate(values):
                value=number(point.get('value',point) if isinstance(point,dict) else point)
                x=60 + (point_index * 106)
                y=88 - (value / max([number(p.get('value',p) if isinstance(p,dict) else p) for p in values] or [1])) * 58
                points.append(f'{x:.1f},{y:.1f}')
            if points:
                color=palette['secondary'] if index else palette['primary']
                series.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
        return f'<div class="chart-zone"><div class="chart-title">{title}</div><svg class="svg-chart" viewBox="0 0 720 115" preserveAspectRatio="xMidYMid meet"><line x1="45" y1="88" x2="690" y2="88" stroke="{palette["grid"]}"/>{"".join(series)}</svg></div>'
    if chart_type in ('waterfall','stacked-bar'):
        maximum=max([abs(number(r.get('value',0))) for r in rows] or [1])
        items=[]
        for index,row in enumerate(rows):
            value=number(row.get('value',0)); height=max(8,round(abs(value)/maximum*75,1)); color=palette['positive'] if value>=0 else palette['negative']
            left=34 + index*100
            items.append(f'<rect x="{left}" y="{90-height}" width="58" height="{height}" rx="2" fill="{color}"/><text x="{left+29}" y="108" text-anchor="middle" font-size="12" fill="{palette["secondary"]}">{html.escape(str(row.get("label","")))}</text><text x="{left+29}" y="{max(16,84-height)}" text-anchor="middle" font-size="13" fill="#211d18">{html.escape(str(row.get("value","")))}</text>')
        return f'<div class="chart-zone"><div class="chart-title">{title}</div><svg class="svg-chart" viewBox="0 0 720 115" preserveAspectRatio="xMidYMid meet"><line x1="20" y1="90" x2="700" y2="90" stroke="{palette["grid"]}"/>{"".join(items)}</svg></div>'
    if chart_type=='range-band':
        items=[]
        for row in rows:
            low=number(row.get('low',0)); high=number(row.get('high',0)); estimate=number(row.get('estimate', (low+high)/2)); scale=max(high,1)
            items.append(f'<div class="chart-row"><span>{html.escape(str(row.get("label","")))}</span><div class="chart-track"><i style="width:{max(6,round(high/scale*100,1))}%;background:{palette["neutral"]}"></i><em style="left:{round(estimate/scale*100,1)}%;background:{palette["secondary"]}"></em></div><b>{html.escape(str(row.get("estimate", "")))}</b></div>')
        return f'<div class="chart-zone"><div class="chart-title">{title}</div>{"".join(items)}</div>'
    if chart_type=='risk-matrix':
        items=[]
        for row in rows:
            x=max(5,min(95,number(row.get('likelihood',50)))); y=max(5,min(95,100-number(row.get('impact',50))))
            items.append(f'<span style="left:{x}%;top:{y}%;background:{palette["primary"]}" title="{html.escape(str(row.get("label","")))}"></span>')
        return f'<div class="chart-zone"><div class="chart-title">{title}</div><div class="risk-matrix"><i></i>{"".join(items)}</div></div>'
    if chart_type=='flow-map':
        items=[]
        for index,row in enumerate(rows[:4]):
            left=30+index*170
            items.append(f'<div class="flow-node" style="left:{left}px">{html.escape(str(row.get("label",row.get("name",""))))}</div>')
        return f'<div class="chart-zone"><div class="chart-title">{title}</div><div class="flow-map">{"".join(items)}</div></div>'
    if chart_type=='validation-dashboard':
        items=[]
        for row in rows:
            items.append(f'<div class="validation-item"><b>{html.escape(str(row.get("label","")))}</b><span>{html.escape(str(row.get("status","待验证")))}</span></div>')
        return f'<div class="chart-zone validation"><div class="chart-title">{title}</div>{ "".join(items) }</div>'
    return ''


def split_caption_text(text, max_chars=20):
    """Split text into short segments for subtitle display. Each segment <= max_chars."""
    import re
    # Split at natural breakpoints: commas, periods, semicolons, colons
    parts = re.split(r'([，。；：、])', text)
    segments = []
    current = ''
    for part in parts:
        if not part:
            continue
        if part in '，。；：、':
            current += part
            if len(current) >= max_chars * 0.6:  # breakpoint reached, flush
                segments.append(current.strip())
                current = ''
        elif len(current) + len(part) > max_chars:
            if current:
                segments.append(current.strip())
            # If single part is too long, force split
            while len(part) > max_chars:
                segments.append(part[:max_chars].strip())
                part = part[max_chars:]
            current = part
        else:
            current += part
    if current.strip():
        segments.append(current.strip())
    return segments if segments else [text]


def agenda_markup(items, start=0, labels=None):
    if not items:
        return ''
    labels=labels or [str(item).split('，',1)[0] for item in items]
    pills=''.join(f'<span class="agenda-item"><b>{index+1:02d}</b><span>{html.escape(str(label))}</span></span>' for index,label in enumerate(labels[:12]))
    return f'<div id="episode-agenda" class="agenda-zone clip" data-start="{start}" data-duration="8" data-track-index="80"><div class="agenda-label">本期目录 · 从增长到验证</div><div class="agenda-items">{pills}</div></div>'


def summary_markup(cards, footer, start=0):
    items=[]
    for card in cards[:3]:
        if isinstance(card,dict):
            label=card.get('label',''); headline=card.get('headline',card.get('value','')); detail=card.get('detail',card.get('desc',''))
        else:
            label,headline,detail,_=tuple(card)+('',)*(4-len(card))
        items.append(f'<div class="summary-card"><div class="kicker">{html.escape(str(label))}</div><div class="headline">{html.escape(str(headline))}</div><div class="detail">{html.escape(str(detail))}</div></div>')
    return f'<div id="summary-zone" class="summary-zone clip" data-start="{start}" data-duration="999" data-track-index="82">{"".join(items)}</div><div class="summary-footer">{html.escape(str(footer))}</div>'


def motion_script(runs, total):
    lines=["const tl=window.__timelines.main;", "const add=(target,from,to,at)=>{if(!target || (target.length!==undefined && target.length===0)) return; tl.fromTo(target,from,to,at);};", "const countFormat=(value,decimals,suffix)=>value.toFixed(decimals)+suffix;", "document.querySelectorAll('[data-count-target]').forEach(el=>{el.textContent='0'+el.dataset.countSuffix;});"]
    for index,group in enumerate(runs):
        topic_id=group[0]['topic_id']; start=float(group[0]['start']); end=float(group[-1]['end'])
        selector=f"#topic-{topic_id}-run-{index}"
        lines.append(f"{{const scene=document.querySelector({json.dumps(selector)}); if(scene){{")
        lines.append(f"add(scene.querySelector('.title'),{{y:24,opacity:0}},{{y:0,opacity:1,duration:.55,ease:'power3.out'}},{start+.12});")
        lines.append(f"add(scene.querySelector('.subtitle'),{{x:-18,opacity:0}},{{x:0,opacity:1,duration:.4,ease:'power2.out'}},{start+.28});")
        lines.append(f"add(scene.querySelectorAll('.metric'),{{y:26,opacity:0,scale:.98}},{{y:0,opacity:1,scale:1,duration:.48,stagger:.08,ease:'power3.out'}},{start+.35});")
        lines.append(f"scene.querySelectorAll('[data-count-target]').forEach(el=>{{const target=Number(el.dataset.countTarget),decimals=Number(el.dataset.countDecimals||0),suffix=el.dataset.countSuffix||''; tl.fromTo(el,{{textContent:'0'+suffix}},{{textContent:target,duration:.72,ease:'power2.out',snap:{{textContent:decimals?0.1:1}},onUpdate:()=>{{const raw=Number(el.textContent)||0; el.textContent=countFormat(raw,decimals,suffix);}}}},{start+.48});}});")
        lines.append(f"add(scene.querySelectorAll('.chart-row i'),{{scaleX:0}},{{scaleX:1,duration:.72,stagger:.09,ease:'power3.out'}},{start+.62});")
        lines.append(f"add(scene.querySelectorAll('.flow-node'),{{x:-24,opacity:0}},{{x:0,opacity:1,duration:.42,stagger:.12,ease:'power3.out'}},{start+.62});")
        lines.append(f"add(scene.querySelectorAll('.validation-item,.summary-card'),{{y:24,opacity:0}},{{y:0,opacity:1,duration:.42,stagger:.1,ease:'power3.out'}},{start+.62});")
        lines.append(f"add(scene.querySelectorAll('polyline'),{{strokeDasharray:1200,strokeDashoffset:1200}},{{strokeDashoffset:0,duration:.9,ease:'power2.out'}},{start+.62});")
        lines.append(f"add(scene.querySelectorAll('rect'),{{scaleY:0,transformOrigin:'center bottom'}},{{scaleY:1,duration:.6,stagger:.08,ease:'back.out(1.2)'}},{start+.68});")
        lines.append("}}")
    # Caption lines use data-start/data-duration for hyperframes visibility
    lines.append(f"tl.to('.persistent-progress-fill',{{width:'100%',duration:{total},ease:'none'}},0);")
    return ''.join(lines)


def persistent_nav_markup(runs, topic_order, topics, topic_number, total):
    durations={topic_id:0.0 for topic_id in topic_order}
    for group in runs:
        topic_id=group[0]['topic_id']
        durations[topic_id]=durations.get(topic_id,0.0)+sum(float(s['duration']) for s in group)
    chapters=[]
    for topic_id in topic_order:
        nav_topic=topics.get(topic_id,{})
        label='冷开场' if topic_id=='COLD_OPEN' else ('开场' if topic_id=='INTRO' else ('总结' if topic_id in {'SUMMARY','OUTRO'} else (nav_topic.get('short_label') or nav_topic.get('title',topic_id).split('，')[0])))
        number=f'{topic_number[topic_id]:02d} ' if topic_id in topic_number else ''
        width=max(0.8,round(durations.get(topic_id,0.0)/total*100,3))
        chapters.append((topic_id,number+label,width))
    states=[]
    for index,group in enumerate(runs):
        topic_id=group[0]['topic_id']; start=group[0]['start']; end=group[-1]['end']
        items=''.join(f'<span class="chapter {"active" if chapter_id==topic_id else ""}" style="width:{width}%"><b>{html.escape(label)}</b></span>' for chapter_id,label,width in chapters)
        states.append(f'<div id="persistent-nav-{index}" class="nav-state clip" data-start="{start}" data-duration="{max(0.1,end-start)}" data-track-index="500"><div class="persistent-nav"><div class="chapter-strip">{items}</div><div class="persistent-progress"><div class="persistent-progress-fill" style="width:0%"></div></div></div></div>')
    return ''.join(states)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--episode',type=Path,required=True); ap.add_argument('--segments',type=Path,required=True); ap.add_argument('--charts',type=Path); ap.add_argument('--visual-plan',type=Path); ap.add_argument('--style',choices=sorted(STYLE_PALETTES),default='editorial-paper'); ap.add_argument('--account-media-dir',type=Path,default=Path(__file__).resolve().parents[1]/'account-profile/account'); ap.add_argument('--font-dir',type=Path,default=Path(__file__).resolve().parents[3]/'.ai/assets/fonts/noto-serif-sc'); ap.add_argument('--font-family',default='Noto Serif SC'); ap.add_argument('--font-regular',default='NotoSerifSC-Regular.otf'); ap.add_argument('--font-bold',default='NotoSerifSC-Bold.otf'); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args()
    episode=json.loads(args.episode.read_text(encoding='utf-8')); data=json.loads(args.segments.read_text(encoding='utf-8')); segs=data['segments']; total=data['total_seconds']
    chart_data=json.loads(args.charts.read_text(encoding='utf-8')) if args.charts else {'charts':[]}
    visual_plan=json.loads(args.visual_plan.read_text(encoding='utf-8')) if args.visual_plan else {'version':'v2','agenda':{'mode':'grid','columns':3}}
    charts_by_topic={}
    for chart in chart_data.get('charts',[]): charts_by_topic.setdefault(chart.get('topic_id'),[]).append(chart)
    topics={t['topic_id']:t for t in episode.get('topics',[])}
    account_name=episode.get('account_name') or episode.get('show_name') or '账本两面'
    default_speakers={
        'zhiwei': {'display_name':'林知微','role':'数据与趋势','color':'#e998be','accent':'#7040a8'},
        'shenyan': {'display_name':'顾慎言','role':'风险与反证','color':'#e4a33d','accent':'#9a5c00'},
    }
    if args.style == 'editorial-paper':
        default_speakers={
            'zhiwei': {'display_name':'林知微','role':'数据与趋势','color':'#f3efe6','accent':'#a6192e'},
            'shenyan': {'display_name':'顾慎言','role':'风险与反证','color':'#e4d3ae','accent':'#1e6b4c'},
        }
    speaker_meta={key:{**default_speakers.get(key,{}),**value} for key,value in episode.get('speakers',{}).items()}
    for key,value in default_speakers.items():
        speaker_meta.setdefault(key,value)
    # Main topic numbering comes from the episode manifest, never from render
    # runs.  INTRO/SUMMARY can split a topic into multiple clips, so using the
    # run index here would produce labels such as 00/02 for the same topic.
    main_topic_order=[t['topic_id'] for t in episode.get('topics',[]) if any(s['topic_id']==t['topic_id'] for s in segs)]
    special_order=[]
    for s in segs:
        if s['topic_id'] not in main_topic_order and s['topic_id'] not in special_order:
            special_order.append(s['topic_id'])
    leading_special=[topic_id for topic_id in special_order if topic_id in {'COLD_OPEN','INTRO'}]
    trailing_special=[topic_id for topic_id in special_order if topic_id not in {'COLD_OPEN','INTRO'}]
    topic_order=leading_special + main_topic_order + trailing_special
    topic_number={topic_id:index+1 for index,topic_id in enumerate(main_topic_order)}
    agenda_items=episode.get('agenda') or [topics[topic_id].get('title',topic_id) for topic_id in main_topic_order]
    agenda_labels=visual_plan.get('agenda',{}).get('labels') or [str(item).split('，',1)[0] for item in agenda_items]
    runs=[]
    for s in segs:
        if not runs or runs[-1][0]['topic_id'] != s['topic_id']:
            runs.append([s])
        else:
            runs[-1].append(s)
    layers=[]
    for index,group in enumerate(runs):
        topic_id=group[0]['topic_id']; start=group[0]['start']; end=group[-1]['end']; t=topics.get(topic_id,{})
        if topic_id=='COLD_OPEN':
            visual=episode.get('opening_visual') or {}
            title=visual.get('headline') or t.get('title', '先看三个数字')
            subtitle=visual.get('subheadline') or t.get('subtitle', '增长很快，质量要先核对')
            metrics=visual.get('cards') or episode.get('opening_cards', [])[:4]
        elif topic_id=='INTRO':
            title=''
            subtitle=''
            intro_speakers=list(episode.get('speakers',{}))[:2] or ['zhiwei','shenyan']
            metrics=[]
            for speaker_id in intro_speakers:
                meta=speaker_meta.get(speaker_id,default_speakers['zhiwei'])
                metrics.append((meta.get('display_name','主持人'),meta.get('role','研究视角'),'关注结构、趋势与验证','pink' if speaker_id=='zhiwei' else 'orange'))
            metrics.append(('本期目录',f'{len(agenda_items)} 个话题','从现象走到验证','blue'))
        elif topic_id in {'SUMMARY','OUTRO'}: title='双人总结'; subtitle='把判断交给下一期数据验证'; metrics=[]
        else:
            title=t.get('title',topic_id)
            legend=t.get('entity_legend') or []
            subtitle='｜'.join(str(x.get('name', x) if isinstance(x, dict) else x) for x in legend)
            metrics=t.get('metrics',[])
            validate_metric_semantics(topic_id, metrics)
        labels=[]
        for nav_index, nav_id in enumerate(topic_order):
            nav_topic=topics.get(nav_id,{})
            nav_label='冷开场' if nav_id=='COLD_OPEN' else ('开场' if nav_id=='INTRO' else ('总结' if nav_id in {'SUMMARY','OUTRO'} else (nav_topic.get('short_label') or nav_topic.get('title',nav_id).split('，')[0])))
            nav_number=f'{topic_number[nav_id]:02d} ' if nav_id in topic_number else ''
            labels.append(f'<span class="{"active" if nav_id==topic_id else ""}">{nav_number}{html.escape(nav_label)}</span>')
        progress=min(100, round(end/total*100,1))
        title_index=f'{topic_number[topic_id]:02d}' if topic_id in topic_number else ('' if topic_id=='INTRO' else ('开场' if topic_id=='COLD_OPEN' else '总结'))
        agenda=agenda_markup(agenda_items, start, agenda_labels) if topic_id=='INTRO' else ''
        chart_specs=charts_by_topic.get(topic_id,[])
        if topic_id=='COLD_OPEN' and not chart_specs:
            chart_specs=charts_by_topic.get('T01',[])
        chart_html=chart_markup(chart_specs,args.style)
        if topic_id in {'SUMMARY','OUTRO'}:
            source_topic=topics.get('T09') or (episode.get('topics') or [{}])[-1]
            summary_cards=episode.get('outro_summary') or source_topic.get('metrics',[])[:3]
            footer=visual_plan.get('outro',{}).get('footer') or '下一期，把增长交给毛利、现金流和产能验证。'
            chart_html=summary_markup(summary_cards, footer, start)
        if agenda and chart_html:
            chart_html=f'<div id="chart-stage-{topic_id}-{index}" class="chart-stage clip" data-start="{start+8}" data-duration="{max(0.1,end-(start+8))}" data-track-index="81">{chart_html}</div>'
        layers.append(f'<div id="topic-{topic_id}-run-{index}" class="topic-layer clip" data-start="{start}" data-duration="{max(0.1,end-start)}" data-track-index="{index+2}"><div class="title"><span class="index">{title_index}</span>{html.escape(title)}</div><div class="subtitle">{html.escape(subtitle)}</div><div class="metrics" data-layout-ignore>{metric_cards(metrics)}</div>{chart_html}{agenda}</div>')
    turns=[]
    for i,s in enumerate(segs):
        speaker=s['speaker']; meta=speaker_meta.get(speaker,{'display_name':speaker,'color':'#e4a33d','accent':'#9a5c00'}); label=meta.get('display_name',speaker)
        full_text=s['text']
        style=f'--speaker-bg:{html.escape(str(meta.get("color","#e4a33d")))};--speaker-accent:{html.escape(str(meta.get("accent","#9a5c00")))}'
        dur=s['duration']
        caption_lines=[f'<div class="caption-line clip" data-start="{s["start"]:.2f}" data-duration="{dur:.2f}" data-track-index="{200+i}">{html.escape(label+"："+full_text)}</div>']
        turns.append(f'<div id="turn-{s["turn_id"]}" class="turn clip" style="{style}" data-start="{s["start"]}" data-duration="{dur}" data-track-index="{100+i}">{"".join(caption_lines)}</div>')
    persistent_nav=persistent_nav_markup(runs,topic_order,topics,topic_number,total)
    font_css=css_for_style(args.style,args.font_family).replace('__DISPLAY_REGULAR__',html.escape(Path(args.font_regular).name)).replace('__DISPLAY_BOLD__',html.escape(Path(args.font_bold).name))
    company_label = episode.get('company') or episode.get('company_name') or '公司研究'
    cover_spec = episode.get('cover') or {}
    cover_title = episode.get('cover_title') or cover_spec.get('title') or episode.get('editorial_thesis') or (topics.get(main_topic_order[0],{}).get('title','') if main_topic_order else '')
    cover_subtitle = episode.get('cover_subtitle') or cover_spec.get('subtitle') or f"{company_label} 财报解读"
    cover_subject = cover_spec.get('subject_label') or '英方 · 海量 · 科蓝'
    cover_large_text = cover_spec.get('large_text') or cover_title
    # Shorten cover title if too long
    if len(cover_title) > 20:
        cover_title = cover_title[:18] + '…'
    logo_source=(args.account_media_dir/'zhangben-liangmian-logo.svg')
    if not logo_source.exists():
        logo_source=(args.account_media_dir/'processed/logo-transparent.png')
    if not logo_source.exists():
        logo_source=(args.account_media_dir/'logo.png')
    has_avatar=(args.account_media_dir/'avatar.png').exists()
    logo_file='account-logo.svg' if logo_source.suffix.lower() == '.svg' else 'account-logo.png'
    has_logo=logo_source.exists()
    logo_tag=f'<img class="account-logo" src="assets/{logo_file}" alt="" data-layout-ignore>' if has_logo else ''
    avatar_tag='<img class="account-avatar" src="assets/account-avatar.png" alt="" data-layout-ignore>' if has_avatar else ''
    doc=f'''<!doctype html><html lang="zh-CN" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>{font_css}</style></head><body><div id="root" data-visual-style="{html.escape(args.style)}" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080"><div class="header"><div class="header-brand">{logo_tag}<div class="show">{html.escape(company_label)}<small>{html.escape(account_name)}</small></div></div><div class="disclaimer">{avatar_tag}企业研究内容｜不构成投资建议<br>数据以公司官方披露为准</div></div>{''.join(layers)}{''.join(turns)}{persistent_nav}<audio id="narration" src="assets/narration-full.mp3" data-start="0" data-duration="{total}" data-track-index="1"></audio></div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});{motion_script(runs,total)}</script></body></html>'''
    args.out.write_text(doc,encoding='utf-8')
    audio_src=args.segments.parent/'narration-full.mp3'
    audio_dst=args.out.parent/'assets'/'narration-full.mp3'
    audio_dst.parent.mkdir(parents=True,exist_ok=True)
    if audio_src.exists() and audio_src.resolve() != audio_dst.resolve(): shutil.copy2(audio_src,audio_dst)
    media_dst=args.out.parent/'assets'
    logo_src=logo_source
    avatar_src=args.account_media_dir/'avatar.png'
    if logo_src.exists(): shutil.copy2(logo_src,media_dst/logo_file)
    mark_source=args.account_media_dir/'zhangben-liangmian-mark.svg'
    if not mark_source.exists():
        mark_source=args.account_media_dir/'zhangben-liangmian-mark-transparent.png'
    mark_file='account-mark.svg' if mark_source.suffix.lower() == '.svg' else 'account-mark.png'
    if mark_source.exists(): shutil.copy2(mark_source,media_dst/mark_file)
    cover_brand_tag=f'<img class="cover-brand-mark" src="assets/{mark_file}" alt=""><div class="brand-wordmark">{html.escape(account_name)}</div>' if mark_source.exists() else html.escape(account_name)
    if avatar_src.exists(): shutil.copy2(avatar_src,media_dst/'account-avatar.png')
    font_dst=args.out.parent/'assets'/'fonts'; font_dst.mkdir(parents=True,exist_ok=True)
    for font_name in (Path(args.font_regular).name,Path(args.font_bold).name):
        font_src=args.font_dir/font_name
        font_target=font_dst/font_name
        if font_src.exists() and font_src.resolve() != font_target.resolve(): shutil.copy2(font_src,font_target)
    # 行尾全角标点「？！」在 Noto Serif SC Bold 中墨迹只占字身左半（右半空字身），text-align:center
    # 按完整字身居中会导致视觉左偏；包进 .qm 由负外边距抵消空字身（.title .qm 规则见 reference_cover_html）。
    cover_title_html='<br>'.join(
        re.sub(r'([？！]+)\s*$', r'<span class="qm">\1</span>', html.escape(line))
        for line in cover_large_text.split('\n'))
    cover_doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><style>{font_css}*{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#191a1d;color:#eee8df}}.cover{{position:relative;width:1920px;height:1080px;overflow:hidden;background:#191a1d;font-family:"__DISPLAY_FONT__","Source Han Serif SC","Songti SC",serif}}.cover:before{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 77% 44%,rgba(111,79,62,.52) 0%,rgba(66,53,47,.32) 24%,transparent 51%),linear-gradient(112deg,#101a25 0%,#1d2024 42%,#3b302b 72%,#17181b 100%)}}.cover:after{{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 48%,rgba(0,0,0,.58) 100%),radial-gradient(rgba(245,235,220,.12) .6px,transparent .8px),radial-gradient(rgba(0,0,0,.16) .55px,transparent .8px);background-size:auto,7px 7px,11px 11px;mix-blend-mode:soft-light;opacity:.72}}.ledger-grid{{position:absolute;inset:0;z-index:1;opacity:.16;background-image:linear-gradient(rgba(190,165,145,.11) 1px,transparent 1px),linear-gradient(90deg,rgba(190,165,145,.08) 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(90deg,transparent 0%,black 16%,black 82%,transparent 100%)}}.brand{{position:absolute;left:112px;top:76px;display:flex;align-items:center;gap:16px;z-index:3;font-size:30px;font-weight:700;letter-spacing:.08em}}.cover-brand-mark{{width:46px;height:46px;object-fit:contain;padding:5px;background:rgba(238,232,223,.78);box-shadow:0 5px 20px rgba(0,0,0,.18)}}.brand-wordmark{{color:#eee8df}}.subject{{position:absolute;left:116px;top:292px;z-index:3;color:#b9a99d;font-family:"Noto Sans SC","Source Han Sans SC",sans-serif;font-size:32px;letter-spacing:.16em;font-weight:500}}h1{{position:absolute;left:108px;top:366px;z-index:3;margin:0;color:#eee8df;font-size:162px;line-height:1.07;letter-spacing:.03em;font-weight:700;text-shadow:0 8px 28px rgba(0,0,0,.24)}}h1::first-line{{color:#f0e9df}}.cover-mark{{position:absolute;right:170px;top:188px;width:510px;height:510px;object-fit:contain;z-index:2;opacity:.18;filter:drop-shadow(0 24px 30px rgba(0,0,0,.32))}}.mark-glow{{position:absolute;right:105px;top:138px;width:650px;height:650px;z-index:1;background:radial-gradient(ellipse,rgba(150,116,93,.25),transparent 68%);filter:blur(12px)}}.bottom{{position:absolute;left:116px;right:116px;bottom:112px;z-index:3;color:#b9a99d;font-family:"Noto Sans SC","Source Han Sans SC",sans-serif;font-size:28px;letter-spacing:.16em;display:flex;align-items:center;gap:28px}}.bottom-rule{{display:block;width:210px;height:1px;background:#742b3c;opacity:.9}}.bottom-text{{white-space:nowrap}}@media(max-width:1200px){{html,body,.cover{{width:1080px;height:1440px}}.cover:before{{background:radial-gradient(ellipse at 74% 51%,rgba(111,79,62,.52) 0%,rgba(66,53,47,.3) 26%,transparent 55%),linear-gradient(148deg,#101a25 0%,#1d2024 45%,#3b302b 77%,#17181b 100%)}}.brand{{left:72px;top:70px}}.cover-brand-mark{{width:40px;height:40px}}.subject{{left:74px;top:290px;font-size:27px;letter-spacing:.13em}}h1{{left:68px;top:365px;font-size:124px;line-height:1.1}}.mark-glow{{right:10px;top:592px;width:540px;height:540px}}.cover-mark{{right:44px;top:640px;width:430px;height:430px;opacity:.17}}.bottom{{left:74px;right:74px;bottom:105px;font-size:22px;letter-spacing:.1em;gap:18px}}.bottom-rule{{width:125px}}}}</style></head><body><main class="cover"><div class="ledger-grid"></div><div class="mark-glow"></div><img class="cover-mark" src="assets/{mark_file}" alt=""><div class="brand">{cover_brand_tag}</div><div class="subject">{html.escape(cover_subject)}</div><h1>{cover_title_html}</h1><div class="bottom"><span class="bottom-rule"></span><span class="bottom-text">{html.escape(cover_subtitle)}</span></div></main></body></html>'''.replace('__DISPLAY_FONT__', html.escape(args.font_family))
    # The account reference cover is the source of truth for the platform-cover visual world.
    cover_doc=reference_cover_html(font_css, account_name, cover_subject, cover_subtitle, cover_title_html, mark_file)
    (args.out.parent/'cover.html').write_text(cover_doc,encoding='utf-8')
    print(f"topics={len(topic_order)} turns={len(segs)} duration={total}")

if __name__=='__main__': main()
