from typing import Optional

from browser.browser_automation import BrowserAutomation


class BlockContext:
    def __init__(self):
        self.browser: Optional[BrowserAutomation] = None

    def set_browser(self, browser: BrowserAutomation):
        self.browser = browser
        return self









