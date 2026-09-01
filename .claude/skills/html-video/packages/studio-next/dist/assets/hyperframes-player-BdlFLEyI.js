var ce=Object.defineProperty;var me=(e,t,i)=>t in e?ce(e,t,{enumerable:!0,configurable:!0,writable:!0,value:i}):e[t]=i;var h=(e,t,i)=>me(e,typeof t!="symbol"?t+"":t,i);function fe(e){return e.hasRuntime||e.runtimeInjected?!1:!!(e.hasNestedCompositions||e.hasTimelines&&e.attempts>=5)}function D(e){return typeof e=="object"&&e!==null}function ge(e){return D(e)&&typeof e.getDuration=="function"}function _e(e){return D(e)&&typeof e.duration=="function"&&typeof e.time=="function"&&typeof e.seek=="function"&&typeof e.play=="function"&&typeof e.pause=="function"}var ve="https://cdn.jsdelivr.net/npm/@hyperframes/core/dist/hyperframe.runtime.iife.js";function $(e){if(e===null)return null;let t=Number.parseInt(e,10);return Number.isFinite(t)&&t>0?t:null}function be(e){let t=(e==null?void 0:e.querySelector("[data-composition-id][data-width][data-height]"))??(e==null?void 0:e.querySelector("[data-width][data-height]"));if(!t)return null;let i=$(t.getAttribute("data-width")),r=$(t.getAttribute("data-height"));return i!==null&&r!==null?{width:i,height:r}:null}var ye=class{constructor(e,t){h(this,"_iframe");h(this,"_callbacks");h(this,"_interval",null);h(this,"_runtimeInjected",!1);this._iframe=e,this._callbacks=t}get runtimeInjected(){return this._runtimeInjected}start(){this.stop(),this._runtimeInjected=!1;let e=0;this._interval=setInterval(()=>{var t;e++;try{let i=this._iframe.contentWindow;if(!i)return;let r=!!(i.__hf||i.__player),a=!!(i.__timelines&&Object.keys(i.__timelines).length>0),s=!!((t=this._iframe.contentDocument)!=null&&t.querySelector("[data-composition-src]"));if(fe({hasRuntime:r,hasTimelines:a,hasNestedCompositions:s,runtimeInjected:this._runtimeInjected,attempts:e})){this._injectRuntime();return}if(this._runtimeInjected&&!r)return;let n=this._resolvePlaybackDurationAdapter(i);if(n&&n.getDuration()>0){this.stop();let d=be(this._iframe.contentDocument);this._callbacks.onReady({duration:n.getDuration(),adapter:n,compositionSize:d});return}}catch{}e>=40&&(this.stop(),this._callbacks.onError("Composition timeline not found after 8s"))},200)}stop(){this._interval!==null&&(clearInterval(this._interval),this._interval=null)}resolveDirectTimelineAdapter(){try{let e=this._iframe.contentWindow;return e?this._resolveDirectTimelineAdapterFromWindow(e):null}catch{return null}}resolveDirectTimelineAdapterFromWindow(e){return this._resolveDirectTimelineAdapterFromWindow(e)}hasRuntimeBridge(e){return Reflect.get(e,"__hf")!==void 0||D(Reflect.get(e,"__player"))}_injectRuntime(){var e,t;this._runtimeInjected=!0;try{let i=this._iframe.contentDocument;if(!i)return;let r=i.createElement("script");r.src=ve,(i.head||i.documentElement).appendChild(r),(t=(e=this._callbacks).onRuntimeInjected)==null||t.call(e)}catch{}}_resolveDirectTimelineAdapterFromWindow(e){var n,d;if(this.hasRuntimeBridge(e))return null;let t=Reflect.get(e,"__timelines");if(!D(t))return null;let i=Object.keys(t);if(i.length===0)return null;let r=(d=(n=this._iframe.contentDocument)==null?void 0:n.querySelector("[data-composition-id]"))==null?void 0:d.getAttribute("data-composition-id"),a=r&&r in t?r:i[i.length-1],s=t[a];return _e(s)?s:null}_resolvePlaybackDurationAdapter(e){let t=Reflect.get(e,"__player");if(ge(t))return{kind:"runtime",getDuration:()=>t.getDuration()};let i=this._resolveDirectTimelineAdapterFromWindow(e);return i?{kind:"direct-timeline",timeline:i,getDuration:()=>i.duration()}:null}},we=`
  :host {
    display: block;
    position: relative;
    overflow: hidden;
    background: #000;
    contain: layout style;
  }

  .hfp-container {
    position: absolute;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
  }


  .hfp-iframe {
    position: absolute;
    top: 50%;
    left: 50%;
    border: none;
    pointer-events: none;
  }

  /* Opt-in: an interactive composition (e.g. a live slideshow/app with playable
     media or controls) — let pointer events reach the iframe content. */
  :host([interactive]) .hfp-container,
  :host([interactive]) .hfp-iframe {
    pointer-events: auto;
  }

  .hfp-poster {
    position: absolute;
    inset: 0;
    object-fit: contain;
    z-index: 1;
    pointer-events: none;
  }

  .hfp-shader-loader {
    position: absolute;
    inset: 0;
    z-index: 20;
    display: grid;
    place-items: center;
    visibility: hidden;
    opacity: 0;
    pointer-events: none;
    background: #030504;
    color: #f4f7fb;
    cursor: default;
    user-select: none;
    -webkit-user-select: none;
    transition: opacity 420ms ease-out, visibility 420ms ease-out;
  }

  .hfp-shader-loader.hfp-visible,
  .hfp-shader-loader.hfp-hiding {
    visibility: visible;
  }

  .hfp-shader-loader.hfp-visible {
    opacity: 1;
    pointer-events: auto;
  }

  .hfp-shader-loader.hfp-hiding {
    opacity: 0;
    pointer-events: none;
  }

  .hfp-shader-loader-panel {
    display: grid;
    grid-template-rows: 86px 40px 26px 12px 44px;
    justify-items: center;
    align-items: center;
    gap: 8px;
    width: min(620px, 82%);
    text-align: center;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }

  .hfp-shader-loader-mark {
    width: 86px;
    height: 86px;
    display: grid;
    place-items: center;
    overflow: visible;
  }

  .hfp-shader-loader-mark svg {
    display: block;
    overflow: visible;
    filter: drop-shadow(0 0 5px rgba(79, 219, 94, 0.16));
    pointer-events: none;
  }

  .hfp-shader-loader-title {
    width: 100%;
    height: 40px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-size: 26px;
    line-height: 40px;
    font-weight: 700;
    letter-spacing: 0;
  }

  .hfp-shader-loader-title-text {
    color: transparent;
    background: linear-gradient(
      90deg,
      rgba(244, 247, 251, 0.84) 0%,
      #ffffff 42%,
      #80efe4 52%,
      #ffffff 62%,
      rgba(244, 247, 251, 0.84) 100%
    );
    background-size: 220% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    animation: hfp-shader-loader-sheen 1.9s linear infinite;
  }

  .hfp-shader-loader-detail {
    width: 100%;
    height: 26px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: rgba(244, 247, 251, 0.62);
    font-size: 15px;
    line-height: 26px;
    font-weight: 500;
  }

  .hfp-shader-loader-track {
    width: min(360px, 100%);
    height: 8px;
    overflow: hidden;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.1);
  }

  .hfp-shader-loader-fill {
    width: 100%;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #06e3fa, #4fdb5e);
    transform: scaleX(0);
    transform-origin: left center;
    transition: transform 160ms ease;
  }

  .hfp-shader-loader-progress {
    width: min(420px, 100%);
    height: 44px;
    display: grid;
    grid-template-rows: repeat(2, 22px);
    color: rgba(244, 247, 251, 0.48);
    font: 600 13px/22px "IBM Plex Mono", "SF Mono", "Fira Code", "Courier New", monospace;
    font-variant-numeric: tabular-nums;
  }

  .hfp-shader-loader-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 74px;
    align-items: center;
    column-gap: 20px;
    width: 100%;
    white-space: nowrap;
  }

  .hfp-shader-loader-label {
    min-width: 0;
    overflow: hidden;
    text-align: left;
    text-overflow: ellipsis;
  }

  .hfp-shader-loader-value {
    text-align: right;
  }

  @keyframes hfp-shader-loader-sheen {
    from {
      background-position: 140% 0;
    }
    to {
      background-position: -140% 0;
    }
  }

  /* ── Theming via CSS custom properties ──
   *
   * Override from outside the shadow DOM:
   *   hyperframes-player {
   *     --hfp-controls-bg: linear-gradient(transparent, rgba(0,0,0,0.9));
   *     --hfp-accent: #ff6b6b;
   *     --hfp-font: "Inter", sans-serif;
   *   }
   */

  .hfp-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    gap: var(--hfp-controls-gap, 12px);
    padding: var(--hfp-controls-padding, 8px 16px);
    background: var(--hfp-controls-bg, linear-gradient(transparent, rgba(0, 0, 0, 0.7)));
    color: var(--hfp-color, #fff);
    font-family: var(--hfp-font, system-ui, -apple-system, sans-serif);
    font-size: var(--hfp-font-size, 13px);
    z-index: 10;
    pointer-events: auto;
    opacity: 1;
    transition: opacity 0.3s ease;
    user-select: none;
  }

  .hfp-controls.hfp-hidden {
    opacity: 0;
    pointer-events: none;
  }

  .hfp-play-btn {
    background: none;
    border: none;
    color: var(--hfp-color, #fff);
    cursor: pointer;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    flex-shrink: 0;
    z-index: 10;
  }

  .hfp-play-btn:hover {
    opacity: 0.8;
  }

  .hfp-play-btn svg,
  .hfp-play-btn svg * {
    pointer-events: none;
  }

  .hfp-scrubber {
    flex: 1;
    min-width: 0;
    height: var(--hfp-scrubber-height, 4px);
    background: var(--hfp-scrubber-bg, rgba(255, 255, 255, 0.3));
    border-radius: var(--hfp-scrubber-radius, 2px);
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .hfp-scrubber:hover {
    height: var(--hfp-scrubber-height-hover, 6px);
  }

  .hfp-progress {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background: var(--hfp-accent, #fff);
    pointer-events: none;
  }

  .hfp-time {
    flex-shrink: 0;
    font-variant-numeric: tabular-nums;
    opacity: 0.9;
  }

  .hfp-speed-wrap {
    position: relative;
    flex-shrink: 0;
  }

  .hfp-speed-btn {
    background: var(--hfp-speed-btn-bg, rgba(255, 255, 255, 0.15));
    border: none;
    border-radius: var(--hfp-speed-btn-radius, 4px);
    color: var(--hfp-color, #fff);
    cursor: pointer;
    font-family: var(--hfp-font, system-ui, -apple-system, sans-serif);
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    padding: 4px 8px;
    min-width: 40px;
    text-align: center;
    transition: background 0.15s ease;
  }

  .hfp-speed-btn:hover {
    background: var(--hfp-speed-btn-bg-hover, rgba(255, 255, 255, 0.3));
  }

  .hfp-speed-menu {
    position: absolute;
    bottom: calc(100% + 8px);
    right: 0;
    background: var(--hfp-menu-bg, rgba(20, 20, 20, 0.95));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--hfp-menu-border, rgba(255, 255, 255, 0.1));
    border-radius: var(--hfp-menu-radius, 8px);
    padding: 4px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 80px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(4px);
    transition: opacity 0.15s ease, transform 0.15s ease, visibility 0.15s;
    box-shadow: var(--hfp-menu-shadow, 0 8px 24px rgba(0, 0, 0, 0.4));
  }

  .hfp-speed-menu.hfp-open {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }

  .hfp-speed-option {
    background: none;
    border: none;
    border-radius: 4px;
    color: var(--hfp-menu-color, rgba(255, 255, 255, 0.7));
    cursor: pointer;
    font-family: var(--hfp-font, system-ui, -apple-system, sans-serif);
    font-size: 13px;
    font-variant-numeric: tabular-nums;
    padding: 6px 12px;
    text-align: left;
    transition: background 0.1s ease, color 0.1s ease;
    white-space: nowrap;
  }

  .hfp-speed-option:hover {
    background: var(--hfp-menu-hover-bg, rgba(255, 255, 255, 0.1));
    color: var(--hfp-color, #fff);
  }

  .hfp-speed-option.hfp-active {
    color: var(--hfp-accent, #fff);
    font-weight: 600;
  }

  .hfp-volume-wrap {
    position: relative;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 0;
  }

  .hfp-mute-btn {
    background: none;
    border: none;
    color: var(--hfp-color, #fff);
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    flex-shrink: 0;
  }

  .hfp-mute-btn:hover {
    opacity: 0.8;
  }

  .hfp-mute-btn svg,
  .hfp-mute-btn svg * {
    pointer-events: none;
  }

  .hfp-volume-slider-wrap {
    width: 0;
    overflow: hidden;
    transition: width 0.2s ease;
    display: flex;
    align-items: center;
  }

  .hfp-volume-wrap:hover .hfp-volume-slider-wrap {
    width: 64px;
  }

  .hfp-volume-slider {
    width: 56px;
    height: var(--hfp-scrubber-height, 4px);
    background: var(--hfp-scrubber-bg, rgba(255, 255, 255, 0.3));
    border-radius: var(--hfp-scrubber-radius, 2px);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    margin-left: 4px;
    margin-right: 4px;
  }

  .hfp-volume-fill {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background: var(--hfp-accent, #fff);
    pointer-events: none;
  }
`,se='<svg width="24" height="24" viewBox="0 0 18 18" fill="currentColor"><polygon points="4,2 16,9 4,16"/></svg>',ke='<svg width="24" height="24" viewBox="0 0 18 18" fill="currentColor"><rect x="3" y="2" width="4" height="14"/><rect x="11" y="2" width="4" height="14"/></svg>',ne='<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3z"/><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/><path d="M14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>',oe='<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3z"/><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/></svg>',Ae='<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3z"/><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z" opacity="0.3"/><line x1="18" y1="7" x2="14" y2="17" stroke="currentColor" stroke-width="2"/></svg>',Ee=[.25,.5,1,1.5,2,4];function z(e){return Number.isInteger(e)?`${e}x`:`${e}x`}function le(e){if(!Number.isFinite(e)||e<0)return"0:00";let t=Math.floor(e),i=Math.floor(t/60),r=t%60;return`${i}:${r.toString().padStart(2,"0")}`}function Ce(e,t,i={}){let r=i.speedPresets??Ee,a=document.createElement("div");a.className="hfp-controls",a.addEventListener("click",o=>{o.stopPropagation()});let s=document.createElement("button");s.className="hfp-play-btn",s.type="button",s.innerHTML=se,s.setAttribute("aria-label","Play");let n=document.createElement("div");n.className="hfp-scrubber";let d=document.createElement("div");d.className="hfp-progress",d.style.width="0%",n.appendChild(d);let p=document.createElement("span");p.className="hfp-time",p.textContent="0:00 / 0:00";let u=document.createElement("div");u.className="hfp-speed-wrap";let m=document.createElement("button");m.className="hfp-speed-btn",m.type="button",m.textContent="1x",m.setAttribute("aria-label","Playback speed");let _=document.createElement("div");_.className="hfp-speed-menu",_.setAttribute("role","menu");for(let o of r){let l=document.createElement("button");l.className="hfp-speed-option",l.type="button",l.setAttribute("role","menuitem"),l.dataset.speed=String(o),l.textContent=z(o),o===1&&l.classList.add("hfp-active"),_.appendChild(l)}u.appendChild(_),u.appendChild(m);let v=document.createElement("div");v.className="hfp-volume-wrap";let f=document.createElement("button");f.className="hfp-mute-btn",f.type="button",f.innerHTML=ne,f.setAttribute("aria-label","Mute");let y=document.createElement("div");y.className="hfp-volume-slider-wrap";let c=document.createElement("div");c.className="hfp-volume-slider",c.setAttribute("role","slider"),c.setAttribute("aria-label","Volume"),c.setAttribute("aria-valuemin","0"),c.setAttribute("aria-valuemax","100"),c.setAttribute("aria-valuenow","100"),c.tabIndex=0;let b=document.createElement("div");b.className="hfp-volume-fill",b.style.width="100%",c.appendChild(b),y.appendChild(c),v.appendChild(y),v.appendChild(f),i.audioLocked&&(v.style.display="none"),a.appendChild(s),a.appendChild(n),a.appendChild(p),a.appendChild(v),a.appendChild(u),e.appendChild(a);let S=!1,A=!1,k=1,T=null;r.indexOf(1);let P=(o,l)=>o?Ae:l===0||l<.5?oe:ne;s.addEventListener("click",o=>{o.stopPropagation(),S?t.onPause():t.onPlay()}),f.addEventListener("click",o=>{o.stopPropagation(),t.onMuteToggle()});let E=!1,I=o=>{let l=c.getBoundingClientRect(),g=Math.max(0,Math.min(1,(o-l.left)/l.width));k=g,b.style.width=`${g*100}%`,c.setAttribute("aria-valuenow",String(Math.round(g*100))),A&&g>0&&t.onMuteToggle(),f.innerHTML=P(A,g),t.onVolumeChange(g)};c.addEventListener("mousedown",o=>{o.stopPropagation(),E=!0,I(o.clientX)});let q=o=>{E&&I(o.clientX)},W=()=>{E=!1};document.addEventListener("mousemove",q),document.addEventListener("mouseup",W),c.addEventListener("touchstart",o=>{E=!0;let l=o.touches[0];l&&I(l.clientX)},{passive:!0});let X=o=>{if(E){let l=o.touches[0];l&&I(l.clientX)}},G=()=>{E=!1};document.addEventListener("touchmove",X,{passive:!0}),document.addEventListener("touchend",G);let Y=.05;c.addEventListener("keydown",o=>{let l=k;if(o.key==="ArrowRight"||o.key==="ArrowUp")l=Math.min(1,k+Y);else if(o.key==="ArrowLeft"||o.key==="ArrowDown")l=Math.max(0,k-Y);else return;o.preventDefault(),o.stopPropagation(),k=l,b.style.width=`${l*100}%`,c.setAttribute("aria-valuenow",String(Math.round(l*100))),A&&l>0&&t.onMuteToggle(),f.innerHTML=P(A,l),t.onVolumeChange(l)});let J=o=>{for(let l of _.querySelectorAll(".hfp-speed-option"))l.classList.toggle("hfp-active",l.dataset.speed===String(o))};m.addEventListener("click",o=>{o.stopPropagation();let l=_.classList.toggle("hfp-open");m.setAttribute("aria-expanded",String(l))}),_.addEventListener("click",o=>{o.stopPropagation();let l=o.target.closest(".hfp-speed-option");if(!l)return;let g=parseFloat(l.dataset.speed);r.indexOf(g),m.textContent=z(g),J(g),_.classList.remove("hfp-open"),m.setAttribute("aria-expanded","false"),t.onSpeedChange(g)});let Z=()=>{_.classList.remove("hfp-open"),m.setAttribute("aria-expanded","false")};document.addEventListener("click",Z);let N=o=>{let l=n.getBoundingClientRect(),g=Math.max(0,Math.min(1,(o-l.left)/l.width));t.onSeek(g)},C=!1;n.addEventListener("mousedown",o=>{o.stopPropagation(),C=!0,N(o.clientX)});let Q=o=>{C&&N(o.clientX)},K=()=>{C=!1};document.addEventListener("mousemove",Q),document.addEventListener("mouseup",K),n.addEventListener("touchstart",o=>{C=!0;let l=o.touches[0];l&&N(l.clientX)},{passive:!0});let ee=o=>{if(C){let l=o.touches[0];l&&N(l.clientX)}},te=()=>{C=!1};document.addEventListener("touchmove",ee,{passive:!0}),document.addEventListener("touchend",te);let ie=()=>{T&&clearTimeout(T),T=setTimeout(()=>{S&&a.classList.add("hfp-hidden")},3e3)},F=e instanceof ShadowRoot?e.host:e,re=()=>{a.classList.remove("hfp-hidden"),ie()},ae=()=>{S&&a.classList.add("hfp-hidden")};return F.addEventListener("mousemove",re),F.addEventListener("mouseleave",ae),{updateTime(o,l){let g=l>0?Math.min(o,l):o,pe=l>0?g/l*100:0;d.style.width=`${pe}%`,p.textContent=`${le(g)} / ${le(l)}`},updatePlaying(o){S=o,s.innerHTML=o?ke:se,s.setAttribute("aria-label",o?"Pause":"Play"),o?ie():a.classList.remove("hfp-hidden")},updateSpeed(o){r.indexOf(o),m.textContent=z(o),J(o)},updateMuted(o){A=o,f.innerHTML=P(o,k),f.setAttribute("aria-label",o?"Unmute":"Mute")},updateVolume(o){k=o,b.style.width=`${o*100}%`,c.setAttribute("aria-valuenow",String(Math.round(o*100))),f.innerHTML=P(A,o)},setVolumeControlsHidden(o){v.style.display=o?"none":""},show(){a.style.display=""},hide(){a.style.display="none"},destroy(){document.removeEventListener("mousemove",Q),document.removeEventListener("mouseup",K),document.removeEventListener("touchmove",ee),document.removeEventListener("touchend",te),document.removeEventListener("mousemove",q),document.removeEventListener("mouseup",W),document.removeEventListener("touchmove",X),document.removeEventListener("touchend",G),document.removeEventListener("click",Z),F.removeEventListener("mousemove",re),F.removeEventListener("mouseleave",ae),T&&clearTimeout(T),a.remove()}}}function xe(e,t,i,r,a,s=!1){let n=r?r.split(",").map(Number).filter(u=>!isNaN(u)&&u>0):void 0,d={...n?{speedPresets:n}:{},audioLocked:s},p=Ce(e,a,d);return p.updateMuted(t),p.updateVolume(i),p}function de(e,t,i){return t?(i||(i=document.createElement("img"),i.className="hfp-poster",e.appendChild(i)),i.src=t,i):(i==null||i.remove(),null)}function Te(e){return e.composedPath().some(t=>t instanceof HTMLElement&&t.classList.contains("hfp-controls"))}var O=null;function Me(e,t){if(typeof CSSStyleSheet<"u")try{O||(O=new CSSStyleSheet,O.replaceSync(t)),e.adoptedStyleSheets=[O];return}catch{}let i=document.createElement("style");i.textContent=t,e.appendChild(i)}function Le(){let e=document.createElement("div");e.className="hfp-container";let t=document.createElement("iframe");return t.className="hfp-iframe",t.sandbox.add("allow-scripts","allow-same-origin"),t.allow="autoplay; fullscreen",t.referrerPolicy="no-referrer",t.title="HyperFrames Composition",e.appendChild(t),{container:e,iframe:t}}function Se(e,t,i,r){let a=e.offsetWidth,s=e.offsetHeight;if(a===0||s===0)return;let n=Math.min(a/i,s/r);t.style.width=`${i}px`,t.style.height=`${r}px`,t.style.transform=`translate(-50%, -50%) scale(${n})`}var Pe=class{constructor(e){h(this,"_callbacks");h(this,"_raf",null);h(this,"_lastUpdateMs",0);this._callbacks=e}start(e,t,i,r){this.stop();let a=()=>{if(r()){this._raf=null;return}let s;try{s=e.time()}catch{this._raf=null;return}let n=i();n>0&&(s=Math.min(s,n));let d=n>0&&s>=n,p=performance.now();if((p-this._lastUpdateMs>100||d)&&(this._lastUpdateMs=p,this._callbacks.onTimeUpdate(s,n)),d){if(this._callbacks.getLoop()){this._callbacks.restart();return}try{e.pause()}catch{}this._callbacks.onPaused(),this._raf=null;return}this._raf=requestAnimationFrame(a)};this._raf=requestAnimationFrame(a)}stop(){this._raf!==null&&(cancelAnimationFrame(this._raf),this._raf=null)}get isRunning(){return this._raf!==null}};function Ie(e){let t=Array.from(e.querySelectorAll("[data-composition-id]"));if(t.length===0)return e.body?[e.body]:[];let i=[];for(let r of t)Fe(r)||i.push(r);return Ne(e),i}function Ne(e){let t=e.body;if(!t||typeof console>"u"||typeof console.warn!="function")return;let i=t.querySelectorAll("audio[data-start], video[data-start]");if(i.length===0)return;let r=[];for(let a of i)a.closest("[data-composition-id]")||r.push(a);r.length!==0&&console.warn(`[hyperframes-player] selectMediaObserverTargets: composition hosts are present, but ${r.length} body-level timed media element(s) sit outside every [data-composition-id] subtree and will not be observed. Move them inside a composition host or the parent-frame proxy will never adopt them.`,r)}function Fe(e){let t=e.parentElement;for(;t;){if(t.hasAttribute("data-composition-id"))return!0;t=t.parentElement}return!1}function j(e){var i;let t=(i=e.ownerDocument)==null?void 0:i.defaultView;return t&&e instanceof t.Element?!0:e instanceof Element}function w(e){var i;if(!j(e)||e.tagName!=="AUDIO"&&e.tagName!=="VIDEO")return!1;let t=(i=e.ownerDocument)==null?void 0:i.defaultView;return t&&e instanceof t.HTMLMediaElement?!0:e instanceof HTMLMediaElement}var Oe=.05,Re=2,De=class{constructor(e){h(this,"_entries",[]);h(this,"_mediaObserver");h(this,"_playbackErrorPosted",!1);h(this,"_audioOwner","runtime");h(this,"_urlAudioEntry",null);h(this,"_urlAudioSrc",null);h(this,"_dispatchEvent");h(this,"_getMuted");h(this,"_getVolume");h(this,"_getPlaybackRate");h(this,"_getCurrentTime");h(this,"_isPaused");this._dispatchEvent=e.dispatchEvent,this._getMuted=e.getMuted,this._getVolume=e.getVolume,this._getPlaybackRate=e.getPlaybackRate,this._getCurrentTime=e.getCurrentTime,this._isPaused=e.isPaused}get audioOwner(){return this._audioOwner}get entries(){return this._entries}resetForIframeLoad(){this._playbackErrorPosted=!1;let e=this._audioOwner==="parent";this._audioOwner="runtime",this.pauseAll(),this.teardownObserver(),e&&this._dispatchEvent(new CustomEvent("audioownershipchange",{detail:{owner:"runtime",reason:"iframe-reload"}}))}destroy(){this.teardownObserver();for(let e of this._entries)e.el.pause(),e.el.src="";this._entries=[],this._urlAudioEntry=null,this._urlAudioSrc=null}updateMuted(e){for(let t of this._entries)t.el.muted=e}updateVolume(e){for(let t of this._entries)t.el.volume=e}updatePlaybackRate(e){for(let t of this._entries)t.el.playbackRate=e}_playEntry(e){e.el.src&&e.el.play().catch(t=>this._reportPlaybackError(t))}_playEntryIfActive(e){this._refreshEntryBounds(e);let t=this._getCurrentTime()-e.start;t<0||t>=e.duration||this._playEntry(e)}_refreshEntryBounds(e){var r;if(!((r=e.source)!=null&&r.isConnected))return;let t=parseFloat(e.source.getAttribute("data-start")||"0");e.start=Number.isFinite(t)?t:0;let i=parseFloat(e.source.getAttribute("data-duration")||"");e.duration=Number.isFinite(i)&&i>0?i:Number.POSITIVE_INFINITY}_gateEntryPlayback(e,t){return t<0||t>=e.duration?(e.el.paused||e.el.pause(),e.driftSamples=0,!1):(this._audioOwner==="parent"&&!this._isPaused()&&e.el.paused&&this._playEntry(e),!0)}playAll(){for(let e of this._entries)this._playEntryIfActive(e)}pauseAll(){for(let e of this._entries)e.el.pause()}stopAdoptedMedia(){for(let e of this._entries)e.source&&e.el.pause()}seekAll(e){for(let t of this._entries){this._refreshEntryBounds(t);let i=e-t.start;i>=0&&i<t.duration&&(t.el.currentTime=i)}}mirrorTime(e,t){let i=(t==null?void 0:t.force)===!0;for(let r of this._entries){this._refreshEntryBounds(r);let a=e-r.start;this._gateEntryPlayback(r,a)&&(Math.abs(r.el.currentTime-a)>Oe?(r.driftSamples+=1,(i||r.driftSamples>=Re)&&(r.el.currentTime=a,r.driftSamples=0)):r.driftSamples=0)}}promoteToParentProxy(e,t){if(this._audioOwner==="parent")return;if(this._audioOwner="parent",e)for(let r of e.querySelectorAll("video, audio"))w(r)&&(r.muted=!0);let i=this._getCurrentTime();t?t(i,{force:!0}):this.mirrorTime(i,{force:!0}),this._isPaused()||this.playAll(),this._dispatchEvent(new CustomEvent("audioownershipchange",{detail:{owner:"parent",reason:"autoplay-blocked"}}))}setupFromIframe(e){let t=e.querySelectorAll("audio[data-start], video[data-start]");for(let i of t)w(i)&&this._adoptIframeMedia(i);this._observeDynamicMedia(e)}setupFromUrl(e){if(this._urlAudioSrc===e&&this._urlAudioEntry)return;this.teardownUrlAudio();let t=this._createEntry(e,"audio",0,1/0);this._urlAudioEntry=t,this._urlAudioSrc=t?e:null,t&&this._audioOwner==="parent"&&!this._isPaused()&&(this.mirrorTime(this._getCurrentTime(),{force:!0}),this.playAll())}teardownUrlAudio(){let e=this._urlAudioEntry;if(this._urlAudioEntry=null,this._urlAudioSrc=null,!e)return;e.el.pause(),e.el.src="";let t=this._entries.indexOf(e);t!==-1&&this._entries.splice(t,1)}teardownObserver(){var e;(e=this._mediaObserver)==null||e.disconnect(),this._mediaObserver=void 0}_reportPlaybackError(e){this._playbackErrorPosted||(this._playbackErrorPosted=!0,this._dispatchEvent(new CustomEvent("playbackerror",{detail:{source:"parent-proxy",error:e}})))}_createEntry(e,t,i,r,a){if(this._entries.some(p=>p.el.src===e))return null;let s=t==="video"?document.createElement("video"):new Audio;s.preload="auto",s.src=e,s.load(),s.muted=this._getMuted(),s.volume=this._getVolume();let n=this._getPlaybackRate();n!==1&&(s.playbackRate=n);let d={el:s,start:i,duration:r,driftSamples:0,source:a};return this._entries.push(d),d}_resolveIframeMediaSrc(e){var i;let t=e.getAttribute("src")||((i=e.querySelector("source"))==null?void 0:i.getAttribute("src"));return t?new URL(t,e.ownerDocument.baseURI).href:null}_adoptIframeMedia(e){if(e.preload==="metadata"||e.preload==="none")return;let t=this._resolveIframeMediaSrc(e);if(!t)return;let i=parseFloat(e.getAttribute("data-start")||"0"),r=parseFloat(e.getAttribute("data-duration")||"Infinity"),a=e.tagName==="VIDEO"?"video":"audio",s=this._createEntry(t,a,i,r,e);s&&this._audioOwner==="parent"&&(this.mirrorTime(this._getCurrentTime(),{force:!0}),this._isPaused()||this._playEntryIfActive(s))}_detachIframeMedia(e){let t=this._resolveIframeMediaSrc(e);if(!t)return;let i=this._entries.findIndex(a=>a.el.src===t);if(i===-1)return;let r=this._entries[i];r.el.pause(),r.el.src="",this._entries.splice(i,1)}_observeDynamicMedia(e){if(this.teardownObserver(),typeof MutationObserver>"u"||!e.body)return;let t=new MutationObserver(a=>{for(let s of a){if(s.type==="attributes"&&s.attributeName==="preload"){let n=s.target;w(n)&&n.matches("audio[data-start], video[data-start]")&&n.preload==="auto"&&this._adoptIframeMedia(n);continue}for(let n of s.addedNodes){if(!j(n))continue;let d=[];w(n)&&n.matches("audio[data-start], video[data-start]")&&d.push(n);let p=n.querySelectorAll("audio[data-start], video[data-start]");for(let u of p)w(u)&&d.push(u);for(let u of d)this._adoptIframeMedia(u)}for(let n of s.removedNodes){if(!j(n))continue;let d=[];w(n)&&n.matches("audio[data-start], video[data-start]")&&d.push(n);let p=n.querySelectorAll("audio[data-start], video[data-start]");for(let u of p)w(u)&&d.push(u);for(let u of d)this._detachIframeMedia(u)}}}),i={childList:!0,subtree:!0,attributes:!0,attributeFilter:["preload"]},r=Ie(e);for(let a of r)t.observe(a,i);this._mediaObserver=t}};function $e(e,t,i,r){let a=(e.frame??0)/t,s=i.duration>0?Math.min(a,i.duration):a,n=!i.paused,d=!e.isPlaying,p=i.duration>0&&s>=i.duration&&(n||e.isPlaying);if(p&&r.getLoop())return r.media.audioOwner==="parent"&&r.media.pauseAll(),r.seek(0),r.play(),{...i,currentTime:s,paused:!1};let u={...i,currentTime:s,paused:d};r.media.audioOwner==="parent"&&(n&&d?r.media.pauseAll():!n&&!d&&r.media.playAll(),r.media.mirrorTime(s));let m=performance.now(),_=d!==i.paused;return(m-i.lastUpdateMs>100||_)&&(u.lastUpdateMs=m,r.updateControlsTime(s,i.duration),r.updateControlsPlaying(!d),r.dispatchEvent(new CustomEvent("timeupdate",{detail:{currentTime:s}}))),p&&(r.media.audioOwner==="parent"&&r.media.pauseAll(),u.paused=!0,r.updateControlsPlaying(!1),r.dispatchEvent(new Event("ended"))),u}var he=30;function ze(e){return Array.isArray(e)?e.filter(t=>typeof t=="object"&&t!==null&&typeof t.id=="string"&&typeof t.start=="number"&&typeof t.duration=="number"):[]}function He(e,t,i){var a;if(e.source!==t)return;let r=e.data;if(!(!r||r.source!=="hf-preview")){if(r.type==="shader-transition-state"){let s=r.state&&typeof r.state=="object"?r.state:{};i.shaderLoader.update(s,i.getShaderLoadingMode()),i.dispatchEvent(new CustomEvent("shadertransitionstate",{detail:{compositionId:r.compositionId,state:s}}));return}if(r.type==="ready"){i.onRuntimeReady();return}if(r.type==="state"){i.setPlaybackState($e({frame:r.frame??0,isPlaying:!!r.isPlaying},he,i.getPlaybackState(),i));return}if(r.type==="media-autoplay-blocked"){if(((a=i.shouldPromoteMediaAutoplayFallback)==null?void 0:a.call(i))===!1)return;let s=null;try{s=i.getIframeDoc()}catch{}i.media.promoteToParentProxy(s,(n,d)=>i.media.mirrorTime(n,d)),i.sendControl("set-media-output-muted",{muted:!0});return}if(r.type==="timeline"&&r.durationInFrames>0){if(Number.isFinite(r.durationInFrames)){let s=i.getPlaybackState(),n=r.durationInFrames/he;i.setPlaybackState({...s,duration:n}),i.updateControlsTime(s.currentTime,n)}i.setScenes(ze(r.scenes));return}r.type==="stage-size"&&Number.isFinite(r.width)&&r.width>0&&Number.isFinite(r.height)&&r.height>0&&i.setCompositionSize(r.width,r.height)}}var x="shader-capture-scale",M="shader-loading",Ue="__hf_shader_capture_scale",Ve="__hf_shader_loading",R=["Preparing scene transitions","Sampling outgoing scene motion","Sampling incoming scene motion","Caching transition frames","Finalizing transition preview"];function B(e){if(e===null)return null;let t=Number(e);return!Number.isFinite(t)||t<=0?null:String(Math.min(1,Math.max(.25,t)))}function je(e){if(e===null||e.trim()==="")return"composition";let t=e.trim().toLowerCase();return t==="none"||t==="false"||t==="0"||t==="off"?"none":t==="player"||t==="true"||t==="1"||t==="on"?"player":"composition"}function ue(e,t,i){i===null?e.delete(t):e.set(t,i)}function Be(e,t,i){let r=e.indexOf("#"),a=r>=0?e.slice(0,r):e,s=r>=0?e.slice(r):"",n=a.indexOf("?"),d=n>=0?a.slice(0,n):a,p=n>=0?a.slice(n+1):"",u=new URLSearchParams(p);ue(u,Ue,t),ue(u,Ve,i==="composition"?null:i);let m=u.toString();return`${d}${m?`?${m}`:""}${s}`}function qe(e,t,i){if(t===null&&i==="composition")return e;let r=[];t!==null&&r.push(`window.__HF_SHADER_CAPTURE_SCALE=${JSON.stringify(t)};`),i!=="composition"&&r.push(`window.__HF_SHADER_LOADING=${JSON.stringify(i)};`);let a=`<script data-hyperframes-player-shader-options>${r.join("")}<\/script>`;return/<head\b[^>]*>/i.test(e)?e.replace(/<head\b[^>]*>/i,s=>`${s}${a}`):/<html\b[^>]*>/i.test(e)?e.replace(/<html\b[^>]*>/i,s=>`${s}${a}`):`${a}${e}`}function L(e){return je(e.getAttribute(M))}function We(e){return Number(B(e.getAttribute(x))??"1")}function H(e,t){return Be(t,B(e.getAttribute(x)),L(e))}function U(e,t){return qe(t,B(e.getAttribute(x)),L(e))}function Xe(){let e=document.createElement("div");e.className="hfp-shader-loader",e.setAttribute("role","status"),e.setAttribute("aria-live","polite"),e.setAttribute("aria-label","Preparing scene transitions"),e.setAttribute("data-hyperframes-ignore",""),e.draggable=!1;let t=f=>{f.preventDefault(),f.stopPropagation()};for(let f of["selectstart","dragstart","pointerdown","mousedown","click","dblclick","contextmenu","touchstart"])e.addEventListener(f,t,{capture:!0});let i=document.createElement("div");i.className="hfp-shader-loader-panel",i.draggable=!1;let r=document.createElement("div");r.className="hfp-shader-loader-mark",r.draggable=!1,r.innerHTML=['<svg width="78" height="78" viewBox="0 0 100 100" fill="none" aria-hidden="true" draggable="false">','<path d="M10.1851 57.8021L33.1145 73.8313C36.2202 75.9978 41.5173 73.5433 42.4816 69.4984L51.7611 30.4271C52.7253 26.3822 48.5802 23.9277 44.4602 26.0942L13.917 42.1235C6.96677 45.7676 4.97564 54.1579 10.1851 57.8021Z" fill="url(#hfp-shader-loader-grad-left)"/>','<path d="M87.5129 57.5141L56.9696 73.5433C52.8371 75.7098 48.7046 73.2553 49.6688 69.2104L58.9483 30.1391C59.9125 26.0942 65.2097 23.6397 68.3154 25.8062L91.2447 41.8354C96.4668 45.4796 94.4631 53.8699 87.5129 57.5141Z" fill="url(#hfp-shader-loader-grad-right)"/>',"<defs>",'<linearGradient id="hfp-shader-loader-grad-left" x1="48.5676" y1="25" x2="44.7804" y2="71.9384" gradientUnits="userSpaceOnUse">','<stop stop-color="#06E3FA"/>','<stop offset="1" stop-color="#4FDB5E"/>',"</linearGradient>",'<linearGradient id="hfp-shader-loader-grad-right" x1="54.8282" y1="73.8392" x2="72.0989" y2="32.8932" gradientUnits="userSpaceOnUse">','<stop stop-color="#06E3FA"/>','<stop offset="1" stop-color="#4FDB5E"/>',"</linearGradient>","</defs>","</svg>"].join("");let a=document.createElement("div");a.className="hfp-shader-loader-title";let s=document.createElement("span");s.className="hfp-shader-loader-title-text",s.textContent=R[0],a.appendChild(s);let n=document.createElement("div");n.className="hfp-shader-loader-detail",n.textContent="Rendering animated scene samples for shader transitions.";let d=document.createElement("div");d.className="hfp-shader-loader-track",d.setAttribute("aria-hidden","true");let p=document.createElement("div");p.className="hfp-shader-loader-fill",d.appendChild(p);let u=document.createElement("div");u.className="hfp-shader-loader-progress";let m=f=>{let y=document.createElement("div");y.className="hfp-shader-loader-row";let c=document.createElement("span");c.className="hfp-shader-loader-label",c.textContent=f;let b=document.createElement("span");return b.className="hfp-shader-loader-value",y.appendChild(c),y.appendChild(b),u.appendChild(y),{row:y,label:c,value:b}},_=m("transition"),v=m("transition frame");return i.appendChild(r),i.appendChild(a),i.appendChild(n),i.appendChild(d),i.appendChild(u),e.appendChild(i),{root:e,fill:p,title:s,detail:n,transitionValue:_.value,frameLabel:v.label,frameValue:v.value,frameRow:v.row}}var Ge=420,Ye=class{constructor(e){h(this,"_el");h(this,"_hideTimeout",null);this._el=e}show(){this._hideTimeout&&(clearTimeout(this._hideTimeout),this._hideTimeout=null),this._el.root.classList.remove("hfp-hiding"),this._el.root.classList.add("hfp-visible")}hide(){if(this._el.root.classList.contains("hfp-hiding")){this._hideTimeout||this._scheduleCleanup();return}this._el.root.classList.contains("hfp-visible")&&(this._el.root.classList.add("hfp-hiding"),this._el.root.classList.remove("hfp-visible"),this._scheduleCleanup())}reset(){this._hideTimeout&&(clearTimeout(this._hideTimeout),this._hideTimeout=null),this._el.root.classList.remove("hfp-visible","hfp-hiding"),this._el.fill.style.transform="scaleX(0)",this._el.transitionValue.textContent="",this._el.frameValue.textContent="",this._el.frameRow.style.visibility="hidden"}update(e,t){if(t!=="player"){this.reset();return}if(e.ready||!e.loading){this.hide();return}let i=typeof e.progress=="number"&&Number.isFinite(e.progress)?e.progress:0,r=typeof e.total=="number"&&Number.isFinite(e.total)?e.total:0,a=r>0?Math.min(1,Math.max(0,i/r)):0,s=Math.min(R.length-1,Math.floor(a*R.length));this._el.title.textContent=R[s]||"Preparing scene transitions",this._el.detail.textContent=e.phase==="cached"?"Loading cached transition frames before playback.":e.phase==="finalizing"?"Uploading transition textures for smooth playback.":"Rendering animated scene samples for shader transitions.",this._el.fill.style.transform=`scaleX(${a})`,this._el.transitionValue.textContent=e.currentTransition!==void 0&&e.transitionTotal!==void 0?`${e.currentTransition}/${e.transitionTotal}`:r>0?`${i}/${r}`:"";let n=e.transitionFrame!==void 0&&e.transitionFrames!==void 0?`${e.transitionFrame}/${e.transitionFrames}`:"";this._el.frameLabel.textContent=e.phase==="cached"?"cached transition frames":e.phase==="finalizing"?"finalizing transition frames":"rendering transition frames",this._el.frameValue.textContent=n,this._el.frameRow.style.visibility=n?"visible":"hidden",this._el.root.setAttribute("aria-valuenow",String(Math.round(a*100))),this.show()}get hideTimeout(){return this._hideTimeout}destroy(){this._hideTimeout&&(clearTimeout(this._hideTimeout),this._hideTimeout=null)}_scheduleCleanup(){this._hideTimeout&&clearTimeout(this._hideTimeout),this._hideTimeout=setTimeout(()=>{this._el.root.classList.remove("hfp-hiding"),this._hideTimeout=null},Ge)}},Je=.1,Ze=5;function V(e){return!Number.isFinite(e)||e<=0?1:Math.max(Je,Math.min(Ze,e))}var Qe=class extends HTMLElement{constructor(){super();h(this,"shadow");h(this,"container");h(this,"iframe");h(this,"posterEl",null);h(this,"controlsApi",null);h(this,"resizeObserver");h(this,"shaderLoader");h(this,"probe");h(this,"_ready",!1);h(this,"_currentTime",0);h(this,"_duration",0);h(this,"_paused",!0);h(this,"_lastUpdateMs",0);h(this,"_volume",1);h(this,"_compositionWidth",1920);h(this,"_compositionHeight",1080);h(this,"_directTimelineAdapter",null);h(this,"_directTimelineClock");h(this,"_parentTickRaf",null);h(this,"_media");h(this,"_scenes",[]);this.shadow=this.attachShadow({mode:"open"}),Me(this.shadow,we),{container:this.container,iframe:this.iframe}=Le(),this.shadow.appendChild(this.container);let t=Xe();this.shadow.appendChild(t.root),this.shaderLoader=new Ye(t),this._media=new De({dispatchEvent:i=>this.dispatchEvent(i),getMuted:()=>this.muted,getVolume:()=>this._volume,getPlaybackRate:()=>this.playbackRate,getCurrentTime:()=>this._currentTime,isPaused:()=>this._paused}),this._directTimelineClock=new Pe({onTimeUpdate:(i,r)=>{var a;this._currentTime=i,(a=this.controlsApi)==null||a.updateTime(i,r),this.dispatchEvent(new CustomEvent("timeupdate",{detail:{currentTime:i}}))},getLoop:()=>this.loop,restart:()=>{this.seek(0),this.play()},onPaused:()=>{var i;this._media.audioOwner==="parent"&&this._media.pauseAll(),this._paused=!0,(i=this.controlsApi)==null||i.updatePlaying(!1),this.dispatchEvent(new Event("ended"))},onEnded:()=>this.loop}),this.probe=new ye(this.iframe,{onReady:i=>this._onProbeReady(i),onError:i=>this.dispatchEvent(new CustomEvent("error",{detail:{message:i}}))}),this.addEventListener("click",i=>{Te(i)||(this._paused?this.play():this.pause())}),this.resizeObserver=new ResizeObserver(()=>this._rescale()),this._onMessage=this._onMessage.bind(this),this._onIframeLoad=this._onIframeLoad.bind(this)}static get observedAttributes(){return["src","srcdoc","width","height","controls","muted","audio-locked","volume","poster","playback-rate","audio-src",x,M]}connectedCallback(){this.resizeObserver.observe(this),window.addEventListener("message",this._onMessage),this.iframe.addEventListener("load",this._onIframeLoad),this.hasAttribute("controls")&&this._setupControls(),this.hasAttribute("poster")&&(this.posterEl=de(this.shadow,this.getAttribute("poster"),this.posterEl)),this.hasAttribute("audio-src")&&this._media.setupFromUrl(this.getAttribute("audio-src")),this.hasAttribute("srcdoc")&&(this.iframe.srcdoc=U(this,this.getAttribute("srcdoc"))),this.hasAttribute("src")&&(this.iframe.src=H(this,this.getAttribute("src"))),!this.hasAttribute("audio-locked")&&this._isLockedHostEnvironment()&&this._applyAudioLock(!0)}disconnectedCallback(){var t;this.resizeObserver.disconnect(),window.removeEventListener("message",this._onMessage),this.iframe.removeEventListener("load",this._onIframeLoad),this.probe.stop(),this._directTimelineClock.stop(),this._stopParentTickClock(),this._directTimelineAdapter=null,this.shaderLoader.destroy(),this._media.destroy(),(t=this.controlsApi)==null||t.destroy()}attributeChangedCallback(t,i,r){var a,s,n,d,p;switch(t){case"src":r&&(this._ready=!1,this.iframe.src=H(this,r));break;case"srcdoc":this._ready=!1,r!==null?this.iframe.srcdoc=U(this,r):this.iframe.removeAttribute("srcdoc");break;case"width":this._compositionWidth=$(r)??1920,this._rescale();break;case"height":this._compositionHeight=$(r)??1080,this._rescale();break;case"controls":r!==null?this._setupControls():((a=this.controlsApi)==null||a.destroy(),this.controlsApi=null);break;case"poster":this.posterEl=de(this.shadow,r,this.posterEl);break;case"playback-rate":{let u=V(parseFloat(r||"1"));this._media.updatePlaybackRate(u),this._sendControl("set-playback-rate",{playbackRate:u}),(n=(s=this._directTimelineAdapter)==null?void 0:s.timeScale)==null||n.call(s,u),(d=this.controlsApi)==null||d.updateSpeed(u),this.dispatchEvent(new Event("ratechange"));break}case"muted":this._handleMutedChange(r);break;case"audio-locked":this._applyAudioLock(r!==null);break;case"volume":{let u=Math.max(0,Math.min(1,parseFloat(r||"1")));this._volume=u,this._media.updateVolume(u),this._sendControl("set-volume",{volume:u}),(p=this.controlsApi)==null||p.updateVolume(u),this.dispatchEvent(new Event("volumechange"));break}case"audio-src":r?this._media.setupFromUrl(r):this._media.teardownUrlAudio();break;case x:case M:this._reloadShaderOptions();break}}get iframeElement(){return this.iframe}get scenes(){return this._scenes}play(){var i,r;(i=this.posterEl)==null||i.remove(),this.posterEl=null,this._duration>0&&this._currentTime>=this._duration&&this.seek(0),this._paused=!1;let t=this._tryDirectTimelinePlay();t||(this._sendControl("play"),this._ready&&!this._directTimelineAdapter&&this._startParentTickClock()),this._media.audioOwner==="parent"&&this._media.playAll(),(r=this.controlsApi)==null||r.updatePlaying(!0),this.dispatchEvent(new Event("play")),t&&this._directTimelineAdapter&&this._directTimelineClock.start(this._directTimelineAdapter,()=>this._currentTime,()=>this._duration,()=>this._paused)}pause(){var t;this._tryDirectTimelinePause()||this._sendControl("pause"),this._directTimelineClock.stop(),this._stopParentTickClock(),this._media.audioOwner==="parent"&&this._media.pauseAll(),this._paused=!0,(t=this.controlsApi)==null||t.updatePlaying(!1),this.dispatchEvent(new Event("pause"))}stopMedia(){this._sendControl("stop-media"),this._stopIframeMedia(),this._media.stopAdoptedMedia()}seek(t){var i,r;!this._trySyncSeek(t)&&!this._tryDirectTimelineSeek(t)&&this._sendControl("seek",{frame:Math.round(t*30)}),this._directTimelineClock.stop(),this._stopParentTickClock(),this._currentTime=t,this._media.audioOwner==="parent"&&(this._media.pauseAll(),this._media.seekAll(t)),this._paused=!0,(i=this.controlsApi)==null||i.updatePlaying(!1),(r=this.controlsApi)==null||r.updateTime(this._currentTime,this._duration)}setColorGrading(t,i){this._sendControl("set-color-grading",{target:t,grading:i})}clearColorGrading(t){this._sendControl("set-color-grading",{target:t,grading:null})}setColorGradingCompare(t,i){this._sendControl("set-color-grading-compare",{target:t,compare:i})}clearColorGradingCompare(t){this._sendControl("set-color-grading-compare",{target:t,compare:{enabled:!1}})}get currentTime(){return this._currentTime}set currentTime(t){this.seek(t)}get duration(){return this._duration}get paused(){return this._paused}get ready(){return this._ready}get playbackRate(){return V(parseFloat(this.getAttribute("playback-rate")||"1"))}set playbackRate(t){this.setAttribute("playback-rate",String(V(t)))}get shaderCaptureScale(){return We(this)}set shaderCaptureScale(t){this.setAttribute(x,String(t))}get shaderLoading(){return L(this)}set shaderLoading(t){t==="composition"?this.removeAttribute(M):this.setAttribute(M,t)}get muted(){return this.hasAttribute("muted")}set muted(t){t?this.setAttribute("muted",""):this.removeAttribute("muted")}get audioLocked(){return this.hasAttribute("audio-locked")}set audioLocked(t){t?this.setAttribute("audio-locked",""):this.removeAttribute("audio-locked")}_isLockedHostEnvironment(){if(typeof navigator>"u")return!1;let t=navigator.userAgent||"";return/\bClaude\/\d/.test(t)&&/\bElectron\b/.test(t)}_isAudioLocked(){return this.hasAttribute("audio-locked")||this._isLockedHostEnvironment()}_isSlideshowPlayer(){return this.closest("hyperframes-slideshow")!==null}_handleMutedChange(t){var i;if(t===null&&this._isAudioLocked()){this.setAttribute("muted","");return}this._media.updateMuted(t!==null),this._setIframeMediaMuted(t!==null),this._sendControl("set-muted",{muted:t!==null}),(i=this.controlsApi)==null||i.updateMuted(t!==null),this.dispatchEvent(new Event("volumechange"))}_applyAudioLock(t){var i;t&&(this.muted=!0),(i=this.controlsApi)==null||i.setVolumeControlsHidden(t)}get volume(){return this._volume}set volume(t){this.setAttribute("volume",String(Math.max(0,Math.min(1,t))))}get loop(){return this.hasAttribute("loop")}set loop(t){t?this.setAttribute("loop",""):this.removeAttribute("loop")}_sendControl(t,i={}){var r;try{(r=this.iframe.contentWindow)==null||r.postMessage({source:"hf-parent",type:"control",action:t,...i},"*")}catch{}}_getSameOriginIframeDocument(){try{return this.iframe.contentDocument}catch{return null}}_setIframeMediaMuted(t){let i=this._getSameOriginIframeDocument();if(i)for(let r of i.querySelectorAll("video, audio"))w(r)&&(r.muted=t||r.defaultMuted)}_stopIframeMedia(){let t=this._getSameOriginIframeDocument();if(t)for(let i of t.querySelectorAll("video, audio"))w(i)&&i.pause()}_replayBridgeState(){this._sendControl("set-muted",{muted:this.muted}),this._sendControl("set-volume",{volume:this._volume}),this._sendControl("set-playback-rate",{playbackRate:this.playbackRate}),this._sendControl("set-native-media-sync-disabled",{disabled:this._isSlideshowPlayer()}),this._sendControl("set-web-audio-media-disabled",{disabled:this._isSlideshowPlayer()})}_reloadShaderOptions(){if(L(this)!=="player"&&this.shaderLoader.reset(),this.hasAttribute("srcdoc")){this.iframe.srcdoc=U(this,this.getAttribute("srcdoc")||"");return}this.hasAttribute("src")&&(this.iframe.src=H(this,this.getAttribute("src")||""))}_trySyncSeek(t){var i;try{let r=(i=this.iframe.contentWindow)==null?void 0:i.__player;return typeof(r==null?void 0:r.seek)!="function"?!1:(r.seek.call(r,t),!0)}catch{return!1}}_withDirectTimeline(t){let i=this._directTimelineAdapter||this.probe.resolveDirectTimelineAdapter();if(!i)return!1;try{return t(i),this._directTimelineAdapter=i,!0}catch{return!1}}_tryDirectTimelineSeek(t){return this._withDirectTimeline(i=>{i.seek(t,!1),i.pause()})}_tryDirectTimelinePlay(){return this._withDirectTimeline(t=>{t.play()})}_tryDirectTimelinePause(){return this._withDirectTimeline(t=>{t.pause()})}_startParentTickClock(){this._stopParentTickClock();let t=()=>{if(this._paused){this._parentTickRaf=null;return}this._sendControl("tick"),this._parentTickRaf=requestAnimationFrame(t)};this._parentTickRaf=requestAnimationFrame(t)}_stopParentTickClock(){this._parentTickRaf!==null&&(cancelAnimationFrame(this._parentTickRaf),this._parentTickRaf=null)}_onMessage(t){He(t,this.iframe.contentWindow,{getPlaybackState:()=>({currentTime:this._currentTime,duration:this._duration,paused:this._paused,lastUpdateMs:this._lastUpdateMs}),setPlaybackState:({currentTime:i,duration:r,paused:a,lastUpdateMs:s})=>{this._currentTime=i,this._duration=r,this._paused=a,this._lastUpdateMs=s},getShaderLoadingMode:()=>L(this),shaderLoader:this.shaderLoader,setCompositionSize:(i,r)=>{this._compositionWidth=i,this._compositionHeight=r,this._rescale()},sendControl:(i,r)=>this._sendControl(i,r),getIframeDoc:()=>this.iframe.contentDocument,onRuntimeReady:()=>this._replayBridgeState(),shouldPromoteMediaAutoplayFallback:()=>!this._isSlideshowPlayer(),setScenes:i=>{this._scenes=i,this.dispatchEvent(new CustomEvent("scenes",{detail:{scenes:i}}))},updateControlsTime:(i,r)=>{var a;return(a=this.controlsApi)==null?void 0:a.updateTime(i,r)},updateControlsPlaying:i=>{var r;return(r=this.controlsApi)==null?void 0:r.updatePlaying(i)},dispatchEvent:i=>this.dispatchEvent(i),seek:i=>this.seek(i),play:()=>this.play(),getLoop:()=>this.loop,media:this._media})}_onProbeReady({duration:t,adapter:i,compositionSize:r}){var a;this._duration=t,this._directTimelineAdapter=i.kind==="direct-timeline"?i.timeline:null,this._ready=!0,(a=this.controlsApi)==null||a.updateTime(0,t),this.dispatchEvent(new CustomEvent("ready",{detail:{duration:t}})),r&&(this._compositionWidth=r.width,this._compositionHeight=r.height,this._rescale());try{let s=this.iframe.contentDocument;s&&this._media.setupFromIframe(s)}catch{}this._setIframeMediaMuted(this.muted),this.hasAttribute("autoplay")&&this.play()}_rescale(){Se(this,this.iframe,this._compositionWidth,this._compositionHeight)}_onIframeLoad(){this._directTimelineAdapter=null,this._directTimelineClock.stop(),this._stopParentTickClock(),this.shaderLoader.reset(),this._media.resetForIframeLoad(),this.probe.start()}_setupControls(){this.controlsApi||(this.controlsApi=xe(this.shadow,this.muted,this._volume,this.getAttribute("speed-presets"),{onPlay:()=>this.play(),onPause:()=>this.pause(),onSeek:t=>this.seek(t*this._duration),onSpeedChange:t=>{this.playbackRate=t},onMuteToggle:()=>{this.muted=!this.muted},onVolumeChange:t=>{this.volume=t}},this._isAudioLocked()))}get _audioOwner(){return this._media.audioOwner}get _parentMedia(){return this._media.entries}_mirrorParentMediaTime(t,i){this._media.mirrorTime(t,i)}_promoteToParentProxy(){let t=null;try{t=this.iframe.contentDocument}catch{}this._media.promoteToParentProxy(t,(i,r)=>this._mirrorParentMediaTime(i,r)),this._sendControl("set-media-output-muted",{muted:!0})}_observeDynamicMedia(t){this._media.setupFromIframe(t)}};customElements.get("hyperframes-player")||customElements.define("hyperframes-player",Qe);export{Qe as HyperframesPlayer,Ee as SPEED_PRESETS,z as formatSpeed,le as formatTime};
