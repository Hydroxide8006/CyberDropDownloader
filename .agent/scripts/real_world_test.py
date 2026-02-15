import asyncio
import os
from cyberdrop_dl.clients.stealth_browser import StealthBrowser
from cyberdrop_dl.utils.logger import log

async def real_world_test():
    log("--- STARTING REAL WORLD STEALTH TEST ---", 20)
    browser = StealthBrowser(headless=True)
    
    targets = [
        {
            "name": "Cloudflare WAF Test (NowSecure)",
            "url": "https://nowsecure.nl",
            "success_indicator": "Congratulations",
            "screenshot": "nowsecure_test.png"
        },
        {
            "name": "Coomer (Real Work Target)",
            "url": "https://coomer.st/artists",
            "success_indicator": "Artists",
            "screenshot": "coomer_test.png"
        }
    ]
    
    try:
        for target in targets:
            log(f"\n[TEST] Testing against {target['name']}...", 20)
            
            # Using get_page_content which has built-in wait
            content = await browser.get_page_content(target['url'])
            
            # Take screenshot for visual proof
            await browser.take_screenshot(target['url'], target['screenshot'])
            
            if target['success_indicator'].lower() in content.lower():
                log(f"[PASS] {target['name']} successfully bypassed!", 20)
                log(f"Visual proof saved to: {os.path.abspath(target['screenshot'])}", 20)
            else:
                log(f"[FAIL] {target['name']} blocked or challenge not solved.", 40)
                # Dump a bit of content to see why
                log(f"Snippet: {content[:500]}...", 30)

    except Exception as e:
        log(f"[CRITICAL ERROR] Test failed: {e}", 40)
    finally:
        await browser.close()
        log("\n--- REAL WORLD STEALTH TEST FINISHED ---", 20)

if __name__ == "__main__":
    asyncio.run(real_world_test())
