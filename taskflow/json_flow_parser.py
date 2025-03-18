import json
from typing import Optional, List, Any

from taskflow.control_flow import ControlFlow
from taskflow.field_saver import FieldSaver
from taskflow.task_blocks.block import BlockFactory, Block
from taskflow.data_exporter import ExcelExporter
from taskflow.task_blocks.end_block import EndBlock


class JsonFlowParser:

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def parse(self, debug_mode: bool = False) -> ControlFlow:
        data_exporter = ExcelExporter(name='data.xlsx')
        field_saver = FieldSaver()
        field_saver.set_data_exporter(data_exporter)

        control_flow = ControlFlow()
        control_flow.set_field_saver(field_saver)
        if debug_mode:
            control_flow.enable_debug_mode(True)
        
        block_factory = BlockFactory(control_flow.get_context())

        with open(self.json_file_path, "r", encoding="utf-8") as f:
            json_flow: List[Any] = json.load(f)

        self.parse_block(json_flow, None, control_flow, block_factory)

        return control_flow

    def parse_block(self,
                    json_flow: List[Any],
                    outer_block: Optional[Block],
                    control_flow: ControlFlow,
                    block_factory: BlockFactory):
        last_block: Optional[Block] = None
        for json_config in json_flow:
            block_name = json_config["block"]
            block = block_factory.create_block(block_name, json_config)
            block.load_from_config(control_flow, json_config)
            
            if json_config.get("breakpoint", False):
                block.set_breakpoint(True)

            if "wait_time" in json_config:
                wait_time = float(json_config["wait_time"])
                block.set_wait_time(wait_time)

            if block_name == "StartBlock":
                control_flow.set_start_block(block)
            if block_name == "EndBlock":
                block = block  # type: EndBlock
                block.observe(control_flow.field_saver.save)
            if outer_block:
                outer_block.add_inner(block)
            if last_block:
                last_block.set_next_block(block)
            last_block = block
            if json_config.get("inners", False):
                self.parse_block(json_config["inners"], block, control_flow, block_factory)
