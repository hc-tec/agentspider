import logging

from taskflow.block_context import BlockContext

from taskflow.task_blocks.block import Block, BlockExecuteParams, register_block


class OpenPageBlock(Block):

    def __init__(self, name: str, page_url: str, context: BlockContext, **kwargs):
        super().__init__(name, context)
        self._page_url = page_url

    def execute(self, params: BlockExecuteParams):
        self.browser.open_page(self._page_url)
        logging.info("{} 打开了 {}".format(self.name, self._page_url))




register_block("OpenPageBlock", OpenPageBlock)







