from playwright.sync_api import sync_playwright
from pathlib import Path
import time

out = Path(r'D:\desktop\_blueyard_research\repro')
errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--use-angle=swiftshader'])
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.on('pageerror', lambda e: errors.append(str(e)[:300]))
    page.on('console', lambda m: errors.append('console.' + m.type + ': ' + m.text[:200]) if m.type == 'error' else None)

    page.goto('http://127.0.0.1:8897/hybrid.html?auto=1&clean=1&shape=galaxy', wait_until='networkidle', timeout=30000)
    time.sleep(14)
    page.screenshot(path=str(out / 'hyb_1_aces.png'))
    page.keyboard.press('t'); time.sleep(1.2)
    page.screenshot(path=str(out / 'hyb_2_legacy.png'))
    page.keyboard.press('t'); time.sleep(0.5)
    page.keyboard.press('g'); time.sleep(1.2)
    page.screenshot(path=str(out / 'hyb_3_nobg.png'))
    page.keyboard.press('g'); page.keyboard.press('b'); time.sleep(1.2)
    page.screenshot(path=str(out / 'hyb_4_nobloom.png'))

    page.goto('http://127.0.0.1:8897/hybrid.html?auto=1&clean=1&shape=ding', wait_until='networkidle', timeout=30000)
    time.sleep(14)
    page.screenshot(path=str(out / 'hyb_5_ding.png'))
    browser.close()

print('ERRORS:', errors if errors else 'none')
print('SHOTS DONE')
