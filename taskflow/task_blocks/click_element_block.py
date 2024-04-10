import logging
from typing import Dict

from taskflow.block_context import BlockContext

from taskflow.task_blocks.block import Block, BlockExecuteParams, register_block


class ClickElementBlock(Block):

    def __init__(self,
                 name: str,
                 context: BlockContext,
                 xpath: str,
                 need_track=True,
                 **kwargs):
        super().__init__(name, context)
        self.xpath = xpath
        self.need_track = need_track

    def click(self, xpath: str):
        if self.need_track:
            self.browser.click_element_and_track(xpath)
        else:
            self.browser.click_element(xpath)

    def execute(self, params: BlockExecuteParams) -> any:
        if self.use_relative_xpath:
            if params.in_loop:
                loop_xpath = params.get_loop_item(self.depth - 1)
                self.click(loop_xpath + self.xpath)
            else:
                logging.error("relative xpath is not supported in no-loop context")
        else:
            self.click(self.xpath)

    def load_from_config(self, control_flow, config: Dict):
        use_relative_xpath = config.get("use_relative_xpath", "False")
        if use_relative_xpath == "True":
            self.use_relative_xpath = True
        else:
            self.use_relative_xpath = False


register_block("ClickElementBlock", ClickElementBlock)
