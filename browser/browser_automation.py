import logging
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from browser.page_tracker import NewPageSWitcher, CurrentPageSWitcher, PageTracker


class BrowserAutomation:

    def __init__(self):
        self.browser = webdriver.Edge()
        self.page_tracker = PageTracker()

    def open_page(self, url: str):
        self.browser.get(url)

    def track_page_switch(self):
        ...

    def rollback_page(self):
        self.page_tracker.back(self.browser)

    def click_element(self, xpath: str) -> bool:
        try:
            element = self.browser.find_element(By.XPATH, xpath)
            ActionChains(self.browser).click(element).perform()
            return True
        except Exception as e:
            logging.log(logging.DEBUG, f"元素{xpath}不存在 Exception: {e}")
            return False

    def click_element_and_track(self, xpath: str):
        self.browser.implicitly_wait(10)

        origin_handle = self.browser.current_window_handle
        origin_url = self.browser.current_url
        origin_handles_len = len(self.browser.window_handles)

        if not self.click_element(xpath):
            return

        current_handle = self.browser.current_window_handle
        current_url = self.browser.current_url
        current_handles_len = len(self.browser.window_handles)

        if origin_handles_len != current_handles_len:
            # 标签页数量不一样，说明在页面在新标签页打开
            new_handle = self.browser.window_handles[1]
            self.browser.switch_to.window(new_handle)
            current_handle = self.browser.current_window_handle
            current_url = self.browser.current_url
            self.page_tracker.track_page_switch(new_handle, NewPageSWitcher(origin_handle))
            logging.info(f"[PageTracking]新标签页打开，网址转变[{origin_url}]->[{current_url}]")
        elif current_url != origin_url:
            # 标签页数量一样，并且网址发生了变化，说明在页面在当前标签页打开
            self.page_tracker.track_page_switch(origin_handle, CurrentPageSWitcher())
            logging.info(f"[PageTracking]当前标签页打开页面，网址转变[{origin_url}]->[{current_url}]")
        if current_handle != origin_handle:
            self.browser.switch_to.window(current_handle)

    def get_element_by_xpath(self, xpath: str) -> Optional[WebElement]:
        self.browser.implicitly_wait(10)
        try:
            return self.browser.find_element(By.XPATH, xpath)
        except Exception as e:
            logging.log(logging.DEBUG, f"元素{xpath}不存在 Exception: {e}")
            return None

    def get_element_text(self, xpath: str) -> str:
        element = self.get_element_by_xpath(xpath)
        return element.text

    def execute_script(self, js_script: str, *args) -> any:
        return self.browser.execute_script(js_script, *args)
