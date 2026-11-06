import * as THREE from './three.module.js';

const params = new URLSearchParams(location.search);
const SHAPE = params.get('shape') || 'galaxy';
const AUTO = params.has('auto');
const CLEAN = params.has('clean');
const BEAT_ARG = (params.get('beat') || '').toLowerCase();
const BM = { OFF: 0, HEART: 1, BREATH: 2 };
const BM_LABEL = ['OFF', 'HEART lub-dub', 'BREATH'];
let beatMode = BEAT_ARG === 'breath' ? BM.BREATH : (BEAT_ARG && BEAT_ARG !== '0' ? BM.HEART : BM.OFF);

const TILE_GRID = 8, TILE_W = 256, TILE_H = 128, N = TILE_W * TILE_H, LAST_TILE = 63;

const renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance' });
renderer.autoClear = false;
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x000000, 1);
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 100);
const scene = new THREE.Scene();

async function loadRaw(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(url + ' ' + r.status);
  return r.arrayBuffer();
}
const [posBuf, colBuf, sclBuf] = await Promise.all([
  loadRaw(`data/pos_${SHAPE}.f32`),
  loadRaw('data/color.rgba'),
  loadRaw('data/scale.rgba'),
]);
const posTex = new THREE.DataTexture(new Float32Array(posBuf), 2048, 1024, THREE.RGBAFormat, THREE.FloatType);
const colTex = new THREE.DataTexture(new Uint8Array(colBuf), 2048, 1024, THREE.RGBAFormat, THREE.UnsignedByteType);
const sclTex = new THREE.DataTexture(new Uint8Array(sclBuf), TILE_W, TILE_H, THREE.RGBAFormat, THREE.UnsignedByteType);
for (const t of [posTex, colTex, sclTex]) { t.needsUpdate = true; t.minFilter = t.magFilter = THREE.NearestFilter; }

const geo = new THREE.BufferGeometry();
{
  const uv = new Float32Array(N * 2), rnd = new Float32Array(N);
  let i = 0;
  for (let y = 0; y < TILE_H; y++)
    for (let x = 0; x < TILE_W; x++) {
      uv[i * 2] = x / TILE_W; uv[i * 2 + 1] = y / TILE_H;
      rnd[i] = Math.random();
      i++;
    }
  geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(N * 3), 3));
  geo.setAttribute('aUv', new THREE.BufferAttribute(uv, 2));
  geo.setAttribute('aRand', new THREE.BufferAttribute(rnd, 1));
}

const particleUniforms = {
  uPosTex: { value: posTex }, uColTex: { value: colTex }, uSclTex: { value: sclTex },
  uProgress: { value: 0 }, uTime: { value: 0 }, uWorld: { value: 2.6 },
  uSizeMul: { value: 0.095 }, uPixelRatio: { value: Math.min(devicePixelRatio, 2) },
  uFocal: { value: 4.3 }, uAperture: { value: 4.2 }, uFade: { value: 0 },
  uLegacy: { value: 0 },
  uBeatVal: { value: 0 }, uBeatAmp: { value: 0 }, uBeatPhase: { value: 0 }, uProp: { value: 0 },
};

const particleMaterial = new THREE.ShaderMaterial({
  uniforms: particleUniforms,
  transparent: true, depthWrite: false, depthTest: false,
  blending: THREE.AdditiveBlending,
  vertexShader: /* glsl */`
    precision highp float;
    uniform sampler2D uPosTex; uniform sampler2D uColTex; uniform sampler2D uSclTex;
    uniform float uProgress, uTime, uWorld, uSizeMul, uPixelRatio, uFocal, uAperture, uFade;
    uniform float uBeatVal, uBeatAmp, uBeatPhase, uProp;
    attribute vec2 aUv; attribute float aRand;
    varying vec3 vColor; varying float vAlpha; varying float vStar;
    vec2 tileUv(float t) {
      float tx = mod(t, 8.0), ty = floor(t / 8.0);
      return (vec2(tx, ty) + aUv) / 8.0;
    }
    vec3 decodePos(float t) {
      vec3 p = texture2D(uPosTex, tileUv(t)).rgb;
      return (p * 2.0 - 1.0) * uWorld;
    }
    float smoother(float x) { return x * x * x * (x * (x * 6.0 - 15.0) + 10.0); }
    float beatAt(float ph) {
      float x1 = (ph - 0.12) * 16.0;
      float x2 = (ph - 0.34) * 20.0;
      return exp(-x1 * x1) + 0.5 * exp(-x2 * x2);
    }
    void main() {
      float t = clamp(uProgress, 0.0, 63.999);
      float t0 = floor(t);
      vec3 p = mix(decodePos(t0), decodePos(t0 + 1.0), smoother(t - t0));

      float b = uBeatAmp * mix(uBeatVal, beatAt(fract(uBeatPhase - length(p) * 0.10)), uProp);
      p *= 1.0 - 0.018 * b;

      vec4 sc = texture2D(uSclTex, aUv);
      float s = (0.45 + sc.r * 0.9) * (0.6 + 0.8 * aRand);
      float star = step(0.992, aRand);

      vec4 mv = modelViewMatrix * vec4(p, 1.0);
      float dist = max(-mv.z, 0.001);
      float defocus = smoothstep(0.0, uAperture, abs(dist - uFocal));

      float size = uSizeMul * s * (1.0 + defocus * 1.6) * (1.0 + 0.07 * b);
      size = mix(size, 0.30, star);
      gl_PointSize = clamp(size * uPixelRatio * 120.0 / dist, 1.0, 48.0);

      float tw = 0.85 + 0.15 * sin(uTime * (0.6 + aRand * 1.4) + aRand * 40.0);
      float central = 0.4 + 0.6 * smoothstep(0.0, 0.9, length(p));
      vec3 cTex = texture2D(uColTex, tileUv(t0)).rgb;
      float cLum = dot(cTex, vec3(0.3, 0.5, 0.2));
      vAlpha = uFade * mix(1.0, 0.35, defocus) * tw * central
             * smoothstep(0.12, 0.34, cLum) * mix(1.0, 1.8, star)
             * (1.0 + 0.12 * b);
      vColor = cTex * (1.0 + 0.4 * b);
      vStar = star;
      gl_Position = projectionMatrix * mv;
    }
  `,
  fragmentShader: /* glsl */`
    precision highp float;
    uniform float uLegacy;
    varying vec3 vColor; varying float vAlpha; varying float vStar;
    void main() {
      vec2 d = gl_PointCoord - 0.5;
      float r = length(d) * 2.0;
      float edge = smoothstep(1.0, 0.72, r);
      float core = 0.35 * smoothstep(0.15, 0.0, r);
      float halo = 0.22 * exp(-r * r * 2.5);
      float ray = exp(-abs(d.x) * 30.0) * exp(-abs(d.y) * 4.0)
                + exp(-abs(d.y) * 30.0) * exp(-abs(d.x) * 4.0);
      float a = mix(edge + core + halo, 1.2 * exp(-r * r * 5.0) + 0.5 * ray, vStar);
      vec3 col = vColor * a * vAlpha;
      if (uLegacy > 0.5) col = 1.0 - exp(-col * 1.5);
      gl_FragColor = vec4(col, 1.0);
    }
  `,
});
const points = new THREE.Points(geo, particleMaterial);
points.rotation.z = SHAPE === 'galaxy' ? 0.18 : 0;
points.frustumCulled = false;
points.renderOrder = 1;
scene.add(points);

const bgUniforms = {
  uTime: { value: 0 }, uAspect: { value: innerWidth / innerHeight },
  uCore: { value: new THREE.Vector2(0.5, 0.5) },
  uCoreScale: { value: 0.5 }, uTheta: { value: 0 },
  uWarm: { value: SHAPE !== 'galaxy' ? 1 : 0 },
  uBeat: { value: 0 },
};
const bgMaterial = new THREE.ShaderMaterial({
  uniforms: bgUniforms, depthTest: false, depthWrite: false,
  vertexShader: `
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
  `,
  fragmentShader: /* glsl */`
    precision highp float;
    uniform float uTime, uAspect, uCoreScale, uTheta, uWarm, uBeat;
    uniform vec2 uCore;
    varying vec2 vUv;
    float hash21(vec2 p) {
      vec3 p3 = fract(vec3(p.xyx) * 0.1031);
      p3 += dot(p3, p3.yzx + 33.33);
      return fract((p3.x + p3.y) * p3.z);
    }
    float noise(vec2 p) {
      vec2 i = floor(p), f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash21(i), hash21(i + vec2(1, 0)), f.x),
                 mix(hash21(i + vec2(0, 1)), hash21(i + vec2(1, 1)), f.x), f.y);
    }
    float fbm(vec2 p) {
      float f = 0.0; mat2 turn = mat2(0.8, -0.6, 0.6, 0.8);
      f += 0.5333 * noise(p); p = turn * p * 2.03 + 13.2;
      f += 0.2667 * noise(p); p = turn * p * 2.01 + 7.1;
      f += 0.1333 * noise(p);
      return f;
    }
    void main() {
      vec2 d = (vUv - uCore) * vec2(uAspect, 1.0);
      float c = cos(uTheta), s = sin(uTheta);
      d = mat2(c, -s, s, c) * d;
      float r = length(d) / max(uCoreScale, 0.001);
      float a = atan(d.y, d.x);
      float swirl = fbm(vec2(a * 3.0 - log(max(r, 0.05)) * 5.0 - uTime * 0.05, r * 4.0));
      float disc = smoothstep(1.15, 0.55, r) * smoothstep(0.03, 0.16, r);
      float filaments = pow(0.5 + 0.5 * sin(a * 3.0 - log(max(r, 0.05)) * 11.0 + swirl * 6.0), 4.0);

      vec3 cold = mix(vec3(0.09, 0.15, 0.32), vec3(0.28, 0.17, 0.08), uWarm);
      vec3 mid  = mix(vec3(0.20, 0.14, 0.38), vec3(0.42, 0.26, 0.10), uWarm);
      vec3 hot  = mix(vec3(1.0, 0.86, 0.72),  vec3(1.0, 0.78, 0.55), uWarm);

      vec3 col = cold * disc * (0.35 + 0.65 * swirl);
      col += mid * disc * filaments * 0.8;
      col += hot * exp(-r * r * 3.2) * 0.55 * (1.0 + uBeat * 0.4);
      col += hot * exp(-r * r * 24.0) * 0.35;

      float bank = fbm(vUv * vec2(5.0, 9.0) + vec2(uTime * 0.01, 0.0));
      float band = exp(-pow((vUv.y - (0.82 - 0.45 * vUv.x)) / 0.11, 2.0));
      col += cold * pow(bank, 3.0) * band * 0.5;

      float vignette = 1.0 - smoothstep(0.45, 1.05, length((vUv - 0.5) * vec2(1.0, 0.85)));
      col *= 0.75 + 0.25 * vignette;
      col += vec3(0.001, 0.002, 0.004);
      gl_FragColor = vec4(col, 1.0);
    }
  `,
});
const bgQuad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), bgMaterial);
bgQuad.frustumCulled = false;
bgQuad.renderOrder = 0;
scene.add(bgQuad);

const rtOpts = { type: THREE.HalfFloatType, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, depthBuffer: false, stencilBuffer: false };
const sceneTarget = new THREE.WebGLRenderTarget(1, 1, rtOpts);
const bloomA = new THREE.WebGLRenderTarget(1, 1, rtOpts);
const bloomB = new THREE.WebGLRenderTarget(1, 1, rtOpts);
const wideA = new THREE.WebGLRenderTarget(1, 1, rtOpts);
const wideB = new THREE.WebGLRenderTarget(1, 1, rtOpts);

const postScene = new THREE.Scene();
const postQuad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.MeshBasicMaterial());
postQuad.frustumCulled = false;
postScene.add(postQuad);
const postCamera = new THREE.Camera();

const blurUniforms = { uSource: { value: null }, uStep: { value: new THREE.Vector2() }, uThreshold: { value: 0.55 } };
const blurMaterial = new THREE.ShaderMaterial({
  uniforms: blurUniforms, depthTest: false, depthWrite: false,
  vertexShader: `
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
  `,
  fragmentShader: /* glsl */`
    precision highp float;
    varying vec2 vUv;
    uniform sampler2D uSource; uniform vec2 uStep; uniform float uThreshold;
    vec3 fetchLight(vec2 uv) {
      vec3 c = texture2D(uSource, uv).rgb;
      float l = max(c.r, max(c.g, c.b));
      return c * max(l - uThreshold, 0.0) / max(l, 0.0001);
    }
    void main() {
      vec3 c = fetchLight(vUv) * 0.227027;
      c += (fetchLight(vUv + uStep * 1.384615) + fetchLight(vUv - uStep * 1.384615)) * 0.316216;
      c += (fetchLight(vUv + uStep * 3.230769) + fetchLight(vUv - uStep * 3.230769)) * 0.070270;
      gl_FragColor = vec4(c, 1.0);
    }
  `,
});
const compositeUniforms = {
  uScene: { value: sceneTarget.texture }, uBloom: { value: bloomB.texture }, uWide: { value: wideB.texture },
  uExposure: { value: 1.0 }, uStrength: { value: 0.8 }, uBloomOn: { value: 1 }, uLegacy: { value: 0 },
};
const compositeMaterial = new THREE.ShaderMaterial({
  uniforms: compositeUniforms, depthTest: false, depthWrite: false,
  vertexShader: `
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
  `,
  fragmentShader: /* glsl */`
    precision highp float;
    varying vec2 vUv;
    uniform sampler2D uScene, uBloom, uWide;
    uniform float uExposure, uStrength, uBloomOn, uLegacy;
    vec3 aces(vec3 x) { return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0); }
    void main() {
      vec3 c = texture2D(uScene, vUv).rgb;
      c += uStrength * uBloomOn * (texture2D(uBloom, vUv).rgb * 0.70 + texture2D(uWide, vUv).rgb * 0.60);
      if (uLegacy > 0.5) {
        gl_FragColor = vec4(pow(clamp(c * uExposure, 0.0, 1.0), vec3(1.0 / 2.2)), 1.0);
      } else {
        gl_FragColor = vec4(pow(aces(c * uExposure), vec3(1.0 / 2.2)), 1.0);
      }
    }
  `,
});

function resize() {
  renderer.setSize(innerWidth, innerHeight);
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  bgUniforms.uAspect.value = innerWidth / innerHeight;
  const w = Math.round(innerWidth * renderer.getPixelRatio()), h = Math.round(innerHeight * renderer.getPixelRatio());
  sceneTarget.setSize(w, h);
  bloomA.setSize(Math.max(1, w >> 1), Math.max(1, h >> 1));
  bloomB.setSize(Math.max(1, w >> 1), Math.max(1, h >> 1));
  wideA.setSize(Math.max(1, w >> 3), Math.max(1, h >> 3));
  wideB.setSize(Math.max(1, w >> 3), Math.max(1, h >> 3));
}
addEventListener('resize', resize);
resize();

function blur(source, target, x, y, threshold) {
  postQuad.material = blurMaterial;
  blurUniforms.uSource.value = source.texture;
  blurUniforms.uStep.value.set(x / source.width, y / source.height);
  blurUniforms.uThreshold.value = threshold;
  renderer.setRenderTarget(target);
  renderer.render(postScene, postCamera);
}

const state = { legacy: false, bg: true, bloom: true, dof: true, exposure: 1.0 };
const hud = document.getElementById('hud');
function hudText() {
  return `MODE ${state.legacy ? 'LEGACY 混合前tonemap' : 'ACES 混合后tonemap'} · BG ${state.bg ? 'ON' : 'OFF'} · BLOOM ${state.bloom ? 'ON' : 'OFF'} · DOF ${state.dof ? 'ON' : 'OFF'}\n` +
    `EXPO ${state.exposure.toFixed(2)} · SHAPE ${SHAPE}\n` +
    `BEAT ${BM_LABEL[beatMode]}${propTarget ? ' · 传导' : ''} · ECG ${ecgOn ? 'ON' : 'OFF'} · SND ${soundOn ? 'ON' : 'OFF'}\n` +
    `T tonemap · G 背景 · B bloom · D 景深 · [ ]大小 · - =曝光 · H节拍 · P传导 · E心电图 · S声音 · 拖拽轨道 滚轮缩放`;
}
function syncState() {
  particleUniforms.uLegacy.value = state.legacy ? 1 : 0;
  compositeUniforms.uLegacy.value = state.legacy ? 1 : 0;
  bgQuad.visible = state.bg;
  compositeUniforms.uBloomOn.value = state.bloom ? 1 : 0;
  particleUniforms.uAperture.value = state.dof ? 4.2 : 1000.0;
  compositeUniforms.uExposure.value = state.exposure;
  hud.textContent = hudText();
}
addEventListener('keydown', e => {
  const k = e.key.toLowerCase();
  if (k === 't') state.legacy = !state.legacy;
  else if (k === 'g') state.bg = !state.bg;
  else if (k === 'b') state.bloom = !state.bloom;
  else if (k === 'd') state.dof = !state.dof;
  else if (e.key === '[') particleUniforms.uSizeMul.value /= 1.15;
  else if (e.key === ']') particleUniforms.uSizeMul.value *= 1.15;
  else if (e.key === '-') state.exposure /= 1.15;
  else if (e.key === '=' || e.key === '+') state.exposure *= 1.15;
  else if (k === 'h') beatMode = (beatMode + 1) % 3;
  else if (k === 'e') ecgOn = !ecgOn;
  else if (k === 'p') propTarget = propTarget ? 0 : 1;
  else if (k === 's') soundOn = !soundOn;
  else return;
  syncState();
});

// ---- orbit ----
// horse body runs along world X -> profile view needs camera on the Z axis (theta 0)
const orbit = { theta: SHAPE === 'horse' ? 0.0 : 0.6,
                phi: SHAPE === 'horse' ? 1.3 : 1.08,
                radius: SHAPE === 'horse' ? 2.7 : 4.3 };
function applyCamera() {
  orbit.phi = Math.max(0.15, Math.min(Math.PI - 0.15, orbit.phi));
  orbit.radius = Math.max(1.6, Math.min(11.0, orbit.radius));
  const sp = Math.sin(orbit.phi);
  camera.position.set(
    orbit.radius * sp * Math.sin(orbit.theta),
    orbit.radius * Math.cos(orbit.phi),
    orbit.radius * sp * Math.cos(orbit.theta));
  camera.lookAt(0, 0, 0);
  camera.updateMatrixWorld();
  const v = new THREE.Vector3(0, 0, 0).project(camera);
  bgUniforms.uCore.value.set(v.x * 0.5 + 0.5, v.y * 0.5 + 0.5);
  bgUniforms.uCoreScale.value = 0.42 / orbit.radius;
  bgUniforms.uTheta.value = orbit.theta * 0.5;
}
let dragging = false, px = 0, py = 0;
addEventListener('pointerdown', e => { dragging = true; px = e.clientX; py = e.clientY; });
addEventListener('pointermove', e => {
  if (!dragging) return;
  orbit.theta -= (e.clientX - px) * 0.005;
  orbit.phi -= (e.clientY - py) * 0.005;
  px = e.clientX; py = e.clientY;
});
addEventListener('pointerup', () => dragging = false);
addEventListener('wheel', e => orbit.radius *= (1 + Math.sign(e.deltaY) * 0.08), { passive: true });

// ---- heartbeat: lub-dub ----
let bpm = 45, phase = 0, amp = 0, propTarget = 0, propCur = 0, holdPhase = null;
let pointerX = -1, pointerY = -1, pointerSeen = false;
let soundOn = true, ecgOn = true, actx = null, master = null;
addEventListener('pointermove', e => { pointerX = e.clientX; pointerY = e.clientY; pointerSeen = true; }, { passive: true });

function ensureAudio() {
  if (actx) { if (actx.state === 'suspended') actx.resume(); return; }
  try {
    actx = new (window.AudioContext || window.webkitAudioContext)();
    master = actx.createGain(); master.gain.value = 0.22;
    master.connect(actx.destination);
  } catch (e) { actx = null; }
}
addEventListener('pointerdown', ensureAudio);
addEventListener('keydown', e => { if (e.key.toLowerCase() === 's') ensureAudio(); });
function thump(freq, gain, dur) {
  if (!actx || actx.state === 'suspended') return;
  const o = actx.createOscillator(), g = actx.createGain();
  o.type = 'sine'; o.frequency.value = freq;
  g.gain.setValueAtTime(gain, actx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.0001, actx.currentTime + dur);
  o.connect(g); g.connect(master);
  o.start(); o.stop(actx.currentTime + dur + 0.02);
}
function beatVal(ph) {
  const g = (m, w) => Math.exp(-Math.pow((ph - m) / w, 2));
  return g(0.12, 0.0625) + 0.5 * g(0.34, 0.05);
}

const ecgCanvas = document.getElementById('ecg');
const ecgCtx = ecgCanvas ? ecgCanvas.getContext('2d') : null;
const ecgBuf = ecgCanvas ? new Float32Array(ecgCanvas.width).fill(0) : null;
let ecgHead = 0;
function drawEcg(v, ampVal) {
  if (!ecgCtx || !ecgOn || amp < 0.01) return;
  ecgBuf[ecgHead] = v * ampVal;
  ecgHead = (ecgHead + 1) % ecgBuf.length;
  const W = ecgCanvas.width, H = ecgCanvas.height;
  ecgCtx.clearRect(0, 0, W, H);
  ecgCtx.fillStyle = 'rgba(3,9,7,0.55)';
  ecgCtx.fillRect(0, 0, W, H);
  ecgCtx.strokeStyle = 'rgba(108,255,160,0.10)';
  ecgCtx.lineWidth = 1;
  ecgCtx.beginPath();
  for (let x = 20; x < W; x += 24) { ecgCtx.moveTo(x + 0.5, 4); ecgCtx.lineTo(x + 0.5, H - 4); }
  ecgCtx.stroke();
  ecgCtx.strokeStyle = '#6cffa0';
  ecgCtx.lineWidth = 1.4;
  ecgCtx.beginPath();
  for (let i = 0; i < W; i++) {
    const val = ecgBuf[(ecgHead + i) % W];
    const y = H - 9 - val * (H - 20);
    i === 0 ? ecgCtx.moveTo(i, y) : ecgCtx.lineTo(i, y);
  }
  ecgCtx.stroke();
  ecgCtx.strokeStyle = 'rgba(108,255,160,0.8)';
  ecgCtx.beginPath(); ecgCtx.moveTo(ecgHead + 0.5, 3); ecgCtx.lineTo(ecgHead + 0.5, H - 3); ecgCtx.stroke();
  ecgCtx.font = '11px ui-monospace, Consolas, monospace';
  ecgCtx.fillStyle = '#6cffa0';
  ecgCtx.textAlign = 'right';
  ecgCtx.fillText(Math.round(bpm) + ' BPM', W - 8, 16);
  ecgCtx.textAlign = 'left';
  ecgCtx.fillStyle = 'rgba(108,255,160,0.55)';
  ecgCtx.fillText(beatMode === BM.BREATH ? 'BREATH' : 'PULSE', 8, 16);
}

function updateBeat(dt, el) {
  const active = beatMode !== BM.OFF;
  const formed = startT !== null && el > INTRO_DUR + 0.5;
  const ampTarget = active && formed ? 1 : 0;
  amp += (ampTarget - amp) * Math.min(1, dt * 0.8);
  if (amp < 0.001) amp = 0;

  const baseBpm = beatMode === BM.BREATH ? 12 : 45;
  let target = baseBpm;
  if (active && pointerSeen) {
    const cx = bgUniforms.uCore.value.x * innerWidth;
    const cy = (1 - bgUniforms.uCore.value.y) * innerHeight;
    const d = Math.hypot(pointerX - cx, pointerY - cy) / (0.38 * Math.min(innerWidth, innerHeight));
    target = baseBpm + Math.max(0, 1 - d) * (beatMode === BM.BREATH ? 8 : 28);
  }
  const rate = target > bpm ? 0.7 : 0.22;
  bpm += (target - bpm) * Math.min(1, dt * rate);

  if (holdPhase !== null) {
    phase = holdPhase;
  } else {
    const old = phase;
    phase += dt * bpm / 60;
    phase -= Math.floor(phase);
    if (amp > 0.05 && beatMode === BM.HEART) {
      if (soundOn) {
        ensureAudio();
        const p2 = phase < old ? phase + 1 : phase;
        if (old < 0.12 && 0.12 <= p2) thump(50, 0.6, 0.3);
        if (old < 0.34 && 0.34 <= p2) thump(66, 0.3, 0.2);
      }
    }
  }
  const v = beatMode === BM.BREATH ? 0.5 - 0.5 * Math.cos(phase * 6.28318) : beatVal(phase);
  const vGain = (beatMode === BM.BREATH ? 0.55 : 1.0) * (SHAPE === 'horse' ? 0.62 : 1.0);
  particleUniforms.uBeatVal.value = v * vGain;
  particleUniforms.uBeatAmp.value = amp;
  particleUniforms.uBeatPhase.value = phase;
  propCur += (propTarget - propCur) * Math.min(1, dt * 3);
  particleUniforms.uProp.value = propCur;
  bgUniforms.uBeat.value = v * vGain * amp;
  drawEcg(v * vGain, amp);
}

window.__beat = {
  get phase() { return phase; }, get bpm() { return bpm; }, get amp() { return amp; },
  hold(v) { holdPhase = v; },
};

// ---- timeline ----
const INTRO_DUR = 11.0;
let startT = null;
function begin() {
  const intro = document.getElementById('intro');
  intro.classList.add('gone');
  setTimeout(() => intro.style.display = 'none', 1300);
  hud.classList.add('on');
  if (beatMode !== BM.OFF) document.getElementById('ecg').classList.add('on');
  document.getElementById('tag').classList.add('on');
  startT = performance.now() / 1000;
}
document.getElementById('intro').addEventListener('click', begin);
if (AUTO) setTimeout(begin, 300);

const clock = new THREE.Clock();
const corePos = new THREE.Vector3();
let prevT = 0;
function frame() {
  requestAnimationFrame(frame);
  const t = clock.getElapsedTime();
  const dt = Math.min(Math.max(t - prevT, 0.0001), 0.1);
  prevT = t;
  let el = 0;
  if (startT !== null) {
    el = performance.now() / 1000 - startT;
    const k = Math.min(el / INTRO_DUR, 1);
    const eased = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    particleUniforms.uProgress.value = eased * LAST_TILE;
    particleUniforms.uFade.value = Math.min(el / 2.0, 1);
    if (!dragging) orbit.theta += 0.0009;
  }
  updateBeat(dt, el);
  particleUniforms.uTime.value = t;
  bgUniforms.uTime.value = t;
  particleUniforms.uFocal.value = orbit.radius + Math.sin(t * 0.1) * 0.15;
  applyCamera();

  renderer.setRenderTarget(sceneTarget);
  renderer.clear();
  renderer.render(scene, camera);
  blur(sceneTarget, bloomA, 1, 0, 0.55);
  blur(bloomA, bloomB, 0, 1, 0);
  blur(bloomB, wideA, 2, 0, 0);
  blur(wideA, wideB, 0, 1.5, 0);
  postQuad.material = compositeMaterial;
  renderer.setRenderTarget(null);
  renderer.render(postScene, postCamera);
}
applyCamera();
syncState();
if (beatMode !== BM.OFF) document.getElementById('tag').textContent = '纹样的心跳 · THE PULSE OF PATTERNS';
if (CLEAN) {
  hud.style.display = 'none';
  document.getElementById('tag').style.display = 'none';
  if (ecgCanvas) ecgCanvas.style.display = 'none';
}
frame();
