from playwright.sync_api import sync_playwright
from pathlib import Path
import time

out = Path(r'D:\desktop\_blueyard_research\repro')
BASE = 'http://127.0.0.1:8897/hybrid.html'
errors = []


def hold_shot(page, name, phase):
    page.evaluate(f'window.__beat.hold({phase})')
    time.sleep(0.4)
    page.screenshot(path=str(out / name))
    page.evaluate('window.__beat.hold(null)')


with sync_playwright() as p:
    browser = p.chromium.launch(args=['--use-angle=swiftshader'])
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.on('pageerror', lambda e: errors.append(str(e)[:300]))
    page.on('console', lambda m: errors.append('console.' + m.type + ': ' + m.text[:200]) if m.type == 'error' else None)

    for shape in ['ding', 'galaxy', 'horse']:
        page.goto(f'{BASE}?auto=1&clean=1&beat=1&shape={shape}', wait_until='networkidle', timeout=30000)
        time.sleep(16)
        amp = page.evaluate('window.__beat.amp')
        hold_shot(page, f'beat_{shape}_sys.png', 0.14)
        hold_shot(page, f'beat_{shape}_dia.png', 0.70)
        print(f'{shape}: amp={amp:.3f}')

    # ECG overlay + tag visible (no clean)
    page.goto(f'{BASE}?auto=1&beat=1&shape=ding', wait_until='networkidle', timeout=30000)
    time.sleep(16)
    hold_shot(page, 'beat_ding_ecg.png', 0.14)

    # breath comparison at same visual moment
    page.goto(f'{BASE}?auto=1&clean=1&beat=breath&shape=ding', wait_until='networkidle', timeout=30000)
    time.sleep(16)
    hold_shot(page, 'beat_ding_breath.png', 0.10)

    # propagation mode
    page.goto(f'{BASE}?auto=1&clean=1&beat=1&shape=ding', wait_until='networkidle', timeout=30000)
    time.sleep(16)
    page.keyboard.press('p')
    time.sleep(1.0)
    hold_shot(page, 'beat_ding_prop.png', 0.24)

    # bpm proximity evidence
    page.mouse.move(640, 400)
    time.sleep(3.5)
    bpm_near = page.evaluate('Math.round(window.__beat.bpm)')
    page.mouse.move(30, 760)
    time.sleep(6.0)
    bpm_far = page.evaluate('Math.round(window.__beat.bpm)')
    print(f'BPM near/far: {bpm_near} / {bpm_far}')

    browser.close()

print('ERRORS:', errors if errors else 'none')
print('BEAT SHOTS DONE')
