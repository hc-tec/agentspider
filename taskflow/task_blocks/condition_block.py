from abc import abstractmethod

from taskflow.block_context import BlockContext
from taskflow.task_blocks.block import Block, BlockExecuteParams, register_block


class ConditionBlock(Block):

    def __init__(self, name: str, context: BlockContext, **kwargs):
        Block.__init__(self, name, context)

    @abstractmethod
    def should_run(self, params: BlockExecuteParams) -> bool:
        ...

    def execute(self, params: BlockExecuteParams):
        for inner in self.inners:
            inner.run(params)


class PassConditionBlock(ConditionBlock):

    def __init__(self, name: str, context: BlockContext, **kwargs):
        ConditionBlock.__init__(self, name, context)

    def should_run(self, params: BlockExecuteParams) -> bool:
        return True


class ExecJavaScriptConditionBlock(ConditionBlock):

    def __init__(self, name: str, context: BlockContext, js_script: str, **kwargs):
        ConditionBlock.__init__(self, name, context)
        self.js_script = js_script

    def should_run(self, params: BlockExecuteParams) -> bool:
        loop_item_element = params.get_loop_item_element(self.depth - 1)
        return self.browser.execute_script(self.js_script, loop_item_element)

    def execute(self, params: BlockExecuteParams):
        loop_item_element = params.get_loop_item_element(self.depth - 1)
        params.set_loop_item_element(self.depth, loop_item_element)
        params.set_loop_item(self.depth, params.get_loop_item(self.depth - 1))
        for inner in self.inners:
            inner.run(params)


register_block("PassConditionBlock", PassConditionBlock)
register_block("ExecJavaScriptConditionBlock", ExecJavaScriptConditionBlock)