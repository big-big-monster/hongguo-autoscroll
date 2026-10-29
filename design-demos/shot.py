import sys, pathlib
from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
h = int(sys.argv[4]) if len(sys.argv) > 4 else 900
full = len(sys.argv) > 5 and sys.argv[5] == 'full'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
    pg.goto(src.as_uri())
    pg.wait_for_timeout(600)
    try:
        pg.evaluate("async () => { await document.fonts.ready; }")
    except Exception:
        pass
    pg.wait_for_timeout(1200)
    pg.screenshot(path=str(out), full_page=full)
    print('shot ->', out)
    b.close()
