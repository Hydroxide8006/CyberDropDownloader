import asyncio
import os
from cyberdrop_dl.clients.stealth_browser import StealthBrowser

async def verify():
    # We use headless=True as default, but let's test specifically
    print("[INFO] Initializing Enhanced Stealth Browser...")
    browser = StealthBrowser(headless=True)
    try:
        url = "https://bot.sannysoft.com/"
        screenshot_path = "stealth_check.png"
        
        print(f"[INFO] Navigating to {url} and taking screenshot...")
        await browser.take_screenshot(url, screenshot_path)
        
        print(f"[SUCCESS] Screenshot captured: {os.path.abspath(screenshot_path)}")
        
        # Also print evaluated internal states for immediate feedback
        await browser._ensure_browser()
        page = await browser._context.new_page()
        await page.goto("about:blank")
        
        stats = {
            "webdriver": await page.evaluate("navigator.webdriver"),
            "userAgent": await page.evaluate("navigator.userAgent"),
            "languages": await page.evaluate("navigator.languages"),
            "plugins": await page.evaluate("navigator.plugins.length"),
            "chrome": await page.evaluate("!!window.chrome"),
            "webgl": await page.evaluate('''() => {
                const canvas = document.createElement("canvas");
                const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
                if (!gl) return "NULL";
                const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
                return debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_ID) : "YES (no extension)";
            }''')
        }
        
        print("\n--- INTERNAL STEALTH REPORT ---")
        for k, v in stats.items():
            print(f"{k}: {v}")
        print("-------------------------------\n")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
