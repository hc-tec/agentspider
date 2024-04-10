import os
import uuid
from pathlib import Path
from functools import partial

from agentscope.message import Msg
from agentscope.msghub import msghub
from agentscope.pipelines.functional import sequentialpipeline
import agentscope
from agentscope.agents.react_agent import ReActAgent
from agentscope.agents.dict_dialog_agent import DictDialogAgent
from agentscope.service import (
    write_text_file,
    ServiceFactory,
    ServiceResponse,
    ServiceExecStatus,
)

from tools.scrape_pages_use_selenium import scrape_pages_use_selenium
from utils.kimi_file_manager import KimiFileManager
from utils.html_operate import compress_html, locate_html_use_xpath
from agents.scrape_page_agent import ScrapePageAgent
from prompts import Prompts


def get_scrape_page_agent():
    tools = [
        ServiceFactory.get(scrape_pages_use_selenium),
    ]

    return ScrapePageAgent(
        name="assistant",
        model_config_name='kimi',
        verbose=True,
        tools=tools,
        max_iters=1,
    )


api_key = "sk-B40WhUzx9fkxAwE8Y8c9d4Z08uRnFIYFdHSA9mXtkxIOyuju"# os.getenv("KIMI_API_KEY")

user_need = "请获取HTML / CSS栏目中所有教程本文以及链接"

kimi_file = KimiFileManager(api_key)
agentscope.init(model_configs="./configs/model_configs.json")

scrape_page_agent = get_scrape_page_agent()

webpage_rate_agent = DictDialogAgent(
    name="assistant",
    model_config_name='kimi',
    sys_prompt=Prompts.to_webpage_rater.format(user_need),
)

msg_question = Msg(
    name="user",
    content="scrape https://zhuanlan.zhihu.com/p/103253120 use selenium, and the xpaths is ['/html/body/div[4]/div/div[2]']",
    role="user"
)

res = scrape_page_agent(msg_question)
(browser, bs_html) = res["content"][0]["result"]
compressed_html = str(compress_html(bs_html))
# target_html = locate_html_use_xpath(compressed_html, ['/html/body/div[4]/div/div[2]'])
file_path = "./page_files/{}.html".format(uuid.uuid4().hex)

res = write_text_file(file_path, compressed_html)

file_id = kimi_file.create(Path(file_path))
file_content = kimi_file.get_file(file_id)
 
file_rate_msg = Msg(
    name="user",
    content=file_content,
    role="user"
)

rate_res = webpage_rate_agent(file_rate_msg)

print(rate_res)
