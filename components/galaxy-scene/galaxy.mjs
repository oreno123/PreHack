import * as THREE from './three.module.js';

const AUTO = new URLSearchParams(location.search).has('auto');
const SHAPE = new URLSearchParams(location.search).get('shape') || 'galaxy';
let dofOn = true;
addEventListener('keydown', e => {
  const hud = document.getElementById('hud');
  if (e.key === '[' || e.key === ']') {
    uniforms.uSizeMul.value *= e.key === ']' ? 1.15 : 1 / 1.15;
  } else if (e.key === '-' || e.key === '=') {
    uniforms.uExposure.value *= e.key === '=' ? 1.15 : 1 / 1.15;
  } else if (e.key === 'g' || e.key === 'G') {
    glowPts.visible = !glowPts.visible;
  } else if (e.key === 'b' || e.key === 'B') {
    dofOn = !dofOn;
    uniforms.uAperture.value = dofOn ? 4.2 : 1000.0;
  } else return;
  hud.textContent = `SIZE ${uniforms.uSizeMul.value.toFixed(3)} · EXPO ${uniforms.uExposure.value.toFixed(2)} · GLOW ${glowPts.visible ? 'ON' : 'OFF'} · DOF ${dofOn ? 'ON' : 'OFF'} · [ ]size - =expo G B`;
  hud.classList.add('on');
});
const CLEAN = new URLSearchParams(location.search).has('clean');
if (CLEAN) {
  document.getElementById('hud').style.display = 'none';
  document.getElementById('tag').style.display = 'none';
}
const TILE_GRID = 8;          // 8x8 tiles
const TILE_W = 256, TILE_H = 128;
const N = TILE_W * TILE_H;    // 32768 particles
const LAST_TILE = 63;

const renderer = new THREE.WebGLRenderer({ antialias: false });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x000000, 1);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 100);

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

const posTex = new THREE.DataTexture(
  new Float32Array(posBuf), 2048, 1024, THREE.RGBAFormat, THREE.FloatType);
posTex.needsUpdate = true;
posTex.minFilter = posTex.magFilter = THREE.NearestFilter;

const colTex = new THREE.DataTexture(
  new Uint8Array(colBuf), 2048, 1024, THREE.RGBAFormat, THREE.UnsignedByteType);
colTex.needsUpdate = true;
colTex.minFilter = colTex.magFilter = THREE.NearestFilter;

const sclTex = new THREE.DataTexture(
  new Uint8Array(sclBuf), TILE_W, TILE_H, THREE.RGBAFormat, THREE.UnsignedByteType);
sclTex.needsUpdate = true;

const geo = new THREE.BufferGeometry();
{
  const uv = new Float32Array(N * 2);
  const rnd = new Float32Array(N);
  let i = 0;
  for (let y = 0; y < TILE_H; y++)
    for (let x = 0; x < TILE_W; x++) {
      uv[i * 2] = x / TILE_W; uv[i * 2 + 1] = y / TILE_H;
      rnd[i] = Math.random();
      i++;
    }
  geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(N * 3), 3)); // dummy, required
  geo.setAttribute('aUv', new THREE.BufferAttribute(uv, 2));
  geo.setAttribute('aRand', new THREE.BufferAttribute(rnd, 1));
}

const uniforms = {
  uPosTex:   { value: posTex },
  uColTex:   { value: colTex },
  uSclTex:   { value: sclTex },
  uProgress: { value: 0 },
  uTime:     { value: 0 },
  uWorld:    { value: 2.6 },
  uSizeMul:  { value: 0.095 },
  uPixelRatio: { value: Math.min(devicePixelRatio, 2) },
  uFocal:    { value: 4.3 },
  uAperture: { value: 4.2 },
  uFade:     { value: 0 },
  uExposure: { value: 0.9 },
};

const material = new THREE.ShaderMaterial({
  uniforms,
  transparent: true,
  depthWrite: false,
  depthTest: false,
  blending: THREE.AdditiveBlending,
  vertexShader: /* glsl */`
    precision highp float;
    uniform sampler2D uPosTex;
    uniform sampler2D uColTex;
    uniform sampler2D uSclTex;
    uniform float uProgress;
    uniform float uTime;
    uniform float uWorld;
    uniform float uSizeMul;
    uniform float uPixelRatio;
    uniform float uFocal;
    uniform float uAperture;
    uniform float uFade;
    attribute vec2 aUv;
    attribute float aRand;
    varying vec3 vColor;
    varying float vAlpha;

    vec2 tileUv(float t) {
      float tx = mod(t, 8.0);
      float ty = floor(t / 8.0);
      return (vec2(tx, ty) + aUv) / 8.0;
    }
    vec3 decodePos(float t) {
      vec3 p = texture2D(uPosTex, tileUv(t)).rgb;
      return (p * 2.0 - 1.0) * uWorld;
    }
    float smoother(float x) { return x * x * x * (x * (x * 6.0 - 15.0) + 10.0); }

    void main() {
      float t = clamp(uProgress, 0.0, 63.999);
      float t0 = floor(t);
      float f = smoother(t - t0);
      vec3 p = mix(decodePos(t0), decodePos(t0 + 1.0), f);

      vec4 sc = texture2D(uSclTex, aUv);
      float s = (0.45 + sc.r * 0.9) * (0.6 + 0.8 * aRand);

      vec4 mv = modelViewMatrix * vec4(p, 1.0);
      float dist = max(-mv.z, 0.001);

      float coc = abs(dist - uFocal);
      float defocus = smoothstep(0.0, uAperture, coc);

      float size = uSizeMul * s * (1.0 + defocus * 1.4);
      gl_PointSize = clamp(size * uPixelRatio * 120.0 / dist, 1.0, 22.0);

      float tw = 0.85 + 0.15 * sin(uTime * (0.6 + aRand * 1.4) + aRand * 40.0);
      float central = 0.4 + 0.6 * smoothstep(0.0, 0.9, length(p));
      vec3 cTex = texture2D(uColTex, tileUv(t0)).rgb;
      float cLum = dot(cTex, vec3(0.3, 0.5, 0.2));
      vAlpha = uFade * mix(1.0, 0.18, defocus) * tw * central
             * smoothstep(0.12, 0.34, cLum);
      vColor = cTex;
      gl_Position = projectionMatrix * mv;
    }
  `,
  fragmentShader: /* glsl */`
    precision highp float;
    uniform float uExposure;
    varying vec3 vColor;
    varying float vAlpha;
    void main() {
      vec2 d = gl_PointCoord - 0.5;
      float r = length(d) * 2.0;
      float a = smoothstep(1.0, 0.72, r);
      a += 0.35 * smoothstep(0.15, 0.0, r);
      float core = smoothstep(0.4, 0.0, r);
      vec3 col = vColor * (0.55 + 0.5 * core);
      col = 1.0 - exp(-col * 1.5);
      float lum = dot(col, vec3(0.299, 0.587, 0.114));
      col = mix(vec3(lum), col, 0.78);
      gl_FragColor = vec4(col * a * vAlpha * uExposure, 1.0);
    }
  `,
});

const points = new THREE.Points(geo, material);
points.rotation.z = SHAPE === 'galaxy' ? 0.18 : 0;
scene.add(points);

// soft core glow (billboard single point)
let glowPts;
{
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([0, 0, 0]), 3));
  const m = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, depthTest: false,
    blending: THREE.AdditiveBlending,
    uniforms: {
      uScale: { value: Math.min(devicePixelRatio, 2) },
      uFade: uniforms.uFade,
    },
    vertexShader: `
      uniform float uScale;
      void main() {
        vec4 mv = modelViewMatrix * vec4(0.0, 0.0, 0.0, 1.0);
        gl_Position = projectionMatrix * mv;
        gl_PointSize = 340.0 * uScale;
      }`,
    fragmentShader: `
      uniform float uFade;
      void main() {
        float r = length(gl_PointCoord - 0.5) * 2.0;
        float a = exp(-r * r * 6.0) * 0.035 + exp(-r * r * 30.0) * 0.072;
        vec3 col = mix(vec3(0.45, 0.66, 1.0), vec3(0.85, 0.93, 1.0), exp(-r * r * 30.0));
        gl_FragColor = vec4(col * a * uFade, 1.0);
      }`,
  });
  const glow = new THREE.Points(g, m);
  glow.rotation.z = 0.18;
  scene.add(glow);
  glowPts = glow;
}

// ---- orbit ----
const orbit = { theta: 0.6, phi: 1.08, radius: 4.3 };

function applyCamera() {
  orbit.phi = Math.max(0.15, Math.min(Math.PI - 0.15, orbit.phi));
  orbit.radius = Math.max(1.6, Math.min(11.0, orbit.radius));
  const sp = Math.sin(orbit.phi);
  camera.position.set(
    orbit.radius * sp * Math.sin(orbit.theta),
    orbit.radius * Math.cos(orbit.phi),
    orbit.radius * sp * Math.cos(orbit.theta));
  camera.lookAt(0, 0, 0);
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
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

// ---- timeline ----
const INTRO_DUR = 11.0;
let startT = null;
function begin() {
  const intro = document.getElementById('intro');
  intro.classList.add('gone');
  setTimeout(() => intro.style.display = 'none', 1300);
  document.getElementById('hud').classList.add('on');
  document.getElementById('tag').classList.add('on');
  startT = performance.now() / 1000;
}
const ring = document.getElementById('ring');
ring.addEventListener('click', begin);
document.getElementById('skip').addEventListener('click', begin);
if (AUTO) setTimeout(begin, 300);

const clock = new THREE.Clock();
function frame() {
  requestAnimationFrame(frame);
  const t = clock.getElapsedTime();
  if (startT === null) { renderer.render(scene, camera); return; }
  const el = performance.now() / 1000 - startT;
  const k = Math.min(el / INTRO_DUR, 1);
  const eased = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
  uniforms.uProgress.value = eased * LAST_TILE;
  uniforms.uTime.value = t;
  uniforms.uFade.value = Math.min(el / 2.0, 1);
  uniforms.uFocal.value = orbit.radius + Math.sin(t * 0.1) * 0.15;
  if (!dragging) orbit.theta += 0.0009;
  applyCamera();
  renderer.render(scene, camera);
}
applyCamera();
document.getElementById('hud').textContent = 'V3 · [ ]size · - =expo · G glow · B dof';
frame();
