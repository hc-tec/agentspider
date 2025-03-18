# AgentSpider
AgentSpider is an automated spider tool, and with the help of LLM, we can make spider simpler

# How to use
1. Install the dependencies 
    
    ```pip install -r requirements.txt```
2. Change the configs/model_configs.json to set your llm api key
    
    ```"api_key": "change-to-your-api-key",```
3. To test the spider, run the following command:
    
    ```python test/taskflow_test.py```
4. More, we are developing the automated spider tool, and waiting for it. We need some time to finish it. 

# 调试模式

为了便于开发和排查问题，AgentSpider现支持调试模式。在调试模式下，可以在任务块中设置断点，程序执行到断点处将会暂停，直到用户按下F9键继续执行。

## 如何使用调试模式

### 方法一：通过代码启用调试模式

```python
# 创建流程控制并启用调试模式
control_flow = ControlFlow()
control_flow.enable_debug_mode(True)  # 启用调试模式

# 在任务块中设置断点
click_block = ClickElementBlock("点击按钮", control_flow.get_context(), xpath)
click_block.set_breakpoint(True)  # 设置断点
```

### 方法二：通过JSON配置启用调试模式

1. 在解析JSON流程时启用调试模式：

```python
control_flow = JsonFlowParser("your_flow.json").parse(debug_mode=True)
control_flow.run()
```

2. 在JSON配置文件中为任务块添加断点：

```json
{
  "block": "ClickElementBlock",
  "name": "点击按钮",
  "xpath": "/path/to/element",
  "breakpoint": true
}
```

### 示例

可以查看`taskflow_test.py`中的`debug_mode_test()`和`debug_json_test()`函数作为示例。 
