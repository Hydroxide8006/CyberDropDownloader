from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from playwright.async_api import BrowserContext, Page, async_playwright
from playwright_stealth import stealth_async

from cyberdrop_dl.utils.logger import log

if TYPE_CHECKING:
    from http.cookies import SimpleCookie
    from collections.abc import AsyncGenerator
    from cyberdrop_dl.data_structures.url_objects import AbsoluteHttpURL


class StealthBrowser:
    """
    A stealthy browser client using Playwright to bypass Cloudflare and other bot protections.
    This acts as a fallback or primary scraper for high-security domains.
    """

    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context: BrowserContext | None = None
        self._lock = asyncio.Lock()

    async def _ensure_browser(self):
        """Ensures the browser and context are initialized."""
        if self._playwright:
            return

        async with self._lock:
            if self._playwright:
                return
            
            log("Initializing Stealth Browser (Playwright)...", 20)
            self._playwright = await async_playwright().start()
            
            # Launch compatible browser - Chromium usually best for Stealth
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars"
                ]
            )
            
            self._context = await self._browser.new_context(
                # Emulate a real desktop browser
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
            )
            
            # Apply stealth scripts to the context
            await stealth_async(self._context)
            log("Stealth Browser Initialized.", 20)

    async def close(self):
        """Closes the browser instance."""
        async with self._lock:
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()
            if self._playwright:
                await self._playwright.stop()
            self._playwright = None
            self._browser = None
            self._context = None

    async def get_cookies_dict(self, url: str, wait_selector: str | None = None) -> dict[str, str]:
        """
        Navigates to a URL and returns the cookies as a dictionary.
        This dictionary can be fed into aiohttp or simplecookie.
        """
        await self._ensure_browser()
        assert self._context
        
        page = await self._context.new_page()
        try:
            log(f"Stealth Browser Navigating to: {url}", 20)
            # Timeout 60s for Cloudflare challenges
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")
            
            if wait_selector:
                try:
                    await page.wait_for_selector(wait_selector, timeout=30000)
                except Exception:
                    log(f"Timeout waiting for selector: {wait_selector}", 30)

            # Wait a bit for JS execution / Challenge solving
            await page.wait_for_timeout(5000)
            
            cookies = await self._context.cookies(url)
            cookie_dict = {c['name']: c['value'] for c in cookies}
            log(f"Extracted {len(cookie_dict)} cookies from {url}", 20)
            return cookie_dict
            
        except Exception as e:
            log(f"Stealth Browser Error on {url}: {e}", 40)
            raise
        finally:
            await page.close()

    async def get_page_content(self, url: str) -> str:
        """Returns the full HTML content after JS execution."""
        await self._ensure_browser()
        assert self._context
        
        page = await self._context.new_page()
        try:
            await page.goto(url, timeout=60000, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            content = await page.content()
            return content
        finally:
            await page.close()
