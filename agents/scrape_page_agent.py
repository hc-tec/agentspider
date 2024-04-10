
from agentscope.agents.react_agent import *


class ScrapePageAgent(ReActAgent):

    def reply(self, x: dict = None) -> dict:
        """The reply function that achieves the ReAct algorithm.
        The more details please refer to https://arxiv.org/abs/2210.03629"""
        if self.memory:
            self.memory.add(x)
        # Generate LLM response
        prompt = self.model.format(
            self.memory.get_memory(),
            Msg("system", TOOL_HINT_PROMPT, role="system"),
        )

        res = self.model(
            prompt,
            parse_func=parse_func,
            max_retries=3,
        ).raw

        # Record the response in memory
        msg_thought = Msg(self.name, res, role="assistant")

        # To better display the response, we reformat it by json.dumps here
        self.speak(
            Msg(self.name, json.dumps(res, indent=4), role="assistant"),
        )

        # Step 2: Action

        # Execute functions
        execute_results = []
        for i, func in enumerate(res["function"]):
            # Execute the function
            func_res = self.execute_func(i, func)
            execute_results.append(func_res)

        # Note: Observing the execution results and generate response are
        # finished in the next loop. We just put the execution results
        # into memory, and wait for the next loop to generate response.

        # Record execution results into memory as a message from the system
        msg_res = Msg(
            name="system",
            content=execute_results,
            role="system",
        )
        # self.speak(msg_res)

        return msg_res









