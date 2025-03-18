from typing import Optional

from browser.browser_automation import BrowserAutomation


class BlockContext:
    def __init__(self):
        self.browser: Optional[BrowserAutomation] = None
        self._debug_mode = False  # 调试模式标志

    def set_browser(self, browser: BrowserAutomation):
        self.browser = browser
        return self

    def set_debug_mode(self, debug_mode: bool):
        """设置调试模式开关"""
        self._debug_mode = debug_mode
        return self

    def is_debug_mode(self) -> bool:
        """获取当前调试模式状态"""
        return self._debug_mode









