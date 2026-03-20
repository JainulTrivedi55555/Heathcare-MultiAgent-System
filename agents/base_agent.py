import os
import json
import re
import logging
from typing import List, Dict, Callable, Any, Optional
from groq import Groq
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")


class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description

    def execute(self, **kwargs) -> str:
        return self.func(**kwargs)


def tool(func: Callable) -> Tool:
    """Decorator to convert a function into a Tool."""
    return Tool(func.__name__, func, func.__doc__ or "No description provided.")


class BaseAgent:
    """
    Base class for all healthcare agents.
    Implements a ReAct-style (Reasoning + Acting) loop:
    - The LLM reasons about the task
    - Optionally calls tools via <tool_call> XML tags
    - Observes tool results and continues until a final answer is produced
    """

    MAX_ITERATIONS = 5  # Prevent infinite loops

    def __init__(self, name: str, tools: List[Tool], system_prompt: str):
        self.name = name
        self.tools = {t.name: t for t in tools}
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict[str, str]] = []
        self.logger = logging.getLogger(name)

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY environment variable is not set.")
        self.client = Groq(api_key=api_key)

    def _format_tools(self) -> str:
        if not self.tools:
            return "No tools available."
        descriptions = "\n".join(
            [f"- {name}: {t.description}" for name, t in self.tools.items()]
        )
        return (
            f"Available tools:\n{descriptions}\n\n"
            "To call a tool, respond with:\n"
            '<tool_call>{"name": "tool_name", "arguments": {"param": "value"}}</tool_call>'
        )

    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.3,
                max_tokens=600,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise

    def _extract_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        pattern = r"<tool_call>(.*?)</tool_call>"
        matches = re.findall(pattern, text, re.DOTALL)
        calls = []
        for match in matches:
            try:
                calls.append(json.loads(match.strip()))
            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse tool call: {e}")
        return calls

    def _execute_tools(self, tool_calls: List[Dict[str, Any]]) -> str:
        results = []
        for call in tool_calls:
            tool_name = call.get("name")
            args = call.get("arguments", {})
            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name].execute(**args)
                    self.logger.info(f"Tool '{tool_name}' executed successfully.")
                    results.append({"tool": tool_name, "result": result})
                except Exception as e:
                    results.append({"tool": tool_name, "result": f"Error: {str(e)}"})
            else:
                results.append({"tool": tool_name, "result": f"Tool '{tool_name}' not found."})
        return json.dumps(results)

    def run(self, user_input: str) -> str:
        """Run the agent on a given input using the ReAct loop."""
        self.conversation_history = []  # Reset per run
        self.conversation_history.append({"role": "user", "content": user_input})

        for iteration in range(self.MAX_ITERATIONS):
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\n" + self._format_tools()}
            ]
            messages.extend(self.conversation_history)

            response = self._call_llm(messages)
            self.conversation_history.append({"role": "assistant", "content": response})

            tool_calls = self._extract_tool_calls(response)
            if tool_calls:
                observation = self._execute_tools(tool_calls)
                self.conversation_history.append({
                    "role": "user",
                    "content": f"<observation>{observation}</observation>\nBased on the tool results above, provide your final answer."
                })
            else:
                return response

        self.logger.warning(f"Reached max iterations ({self.MAX_ITERATIONS}). Returning last response.")
        return self.conversation_history[-1]["content"]
