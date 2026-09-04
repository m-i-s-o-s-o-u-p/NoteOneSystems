import time
from playwright.sync_api import sync_playwright

def test_actual_scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=True
        )
        page = browser.new_page()
        page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=60000)
        time.sleep(3)

        # 1. 500px スクロールダウン
        page.evaluate("""
            () => {
                const mainEl = document.querySelector('[data-testid="stMain"]') || document.querySelector('.stMain');
                if (mainEl) {
                    mainEl.scrollTop = 500;
                }
            }
        """)
        time.sleep(1)

        scroll_val = page.evaluate("""
            () => {
                const mainEl = document.querySelector('[data-testid="stMain"]') || document.querySelector('.stMain');
                return mainEl ? mainEl.scrollTop : -1;
            }
        """)
        print(f"1. Scroll position after manual scroll down: {scroll_val}")

        # 2. [data-testid="stMain"].scrollTop = 0 を実行して0に戻るか確認
        page.evaluate("""
            () => {
                const targets = [
                    document.querySelector('[data-testid="stMain"]'),
                    document.querySelector('.stMain'),
                    document.querySelector('[data-testid="stAppViewContainer"]'),
                    document.documentElement,
                    document.body,
                    window
                ];
                targets.forEach(t => {
                    if (t) {
                        t.scrollTop = 0;
                        try { t.scrollTo({ top: 0, behavior: 'instant' }); } catch(e) {}
                    }
                });
            }
        """)
        time.sleep(1)

        scroll_after_reset = page.evaluate("""
            () => {
                const mainEl = document.querySelector('[data-testid="stMain"]') || document.querySelector('.stMain');
                return mainEl ? mainEl.scrollTop : -1;
            }
        """)
        print(f"2. Scroll position after resetting [data-testid='stMain']: {scroll_after_reset}")

        browser.close()

if __name__ == "__main__":
    test_actual_scroll()
