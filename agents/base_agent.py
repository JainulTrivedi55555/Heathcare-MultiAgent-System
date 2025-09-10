from typing import List, Dict, Callable, Any
import json
import re
import os
from openai import OpenAI

class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description

    def execute(self, **kwargs):
        return self.func(**kwargs)

def tool(func: Callable) -> Tool:
    return Tool(func.__name__, func, func.__doc__)

class BaseAgent:
    def __init__(self, name: str, tools: List[Tool], system_prompt: str):
        self.name = name
        self.tools = {tool.name: tool for tool in tools}
        self.system_prompt = system_prompt
        self.conversation_history = []
        # Initialize OpenAI client with your API key from environment variable
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def format_tools(self) -> str:
        tool_descriptions = "\n".join([f"- {t.name}: {t.description}" for t in self.tools.values()])
        return f"Available tools:\n{tool_descriptions}"

    def call_openai(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
            max_tokens=500,
        )
        return response.choices[0].message.content

    def extract_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        pattern = r"<tool_call>(.*?)</tool_call>"
        matches = re.findall(pattern, text, re.DOTALL)
        calls = []
        for match in matches:
            try:
                calls.append(json.loads(match.strip()))
            except json.JSONDecodeError:
                continue
        return calls

    def run(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self.system_prompt + "\n\n" + self.format_tools()}]
        messages.extend(self.conversation_history)

        response = self.call_openai(messages)
        self.conversation_history.append({"role": "assistant", "content": response})

        tool_calls = self.extract_tool_calls(response)
        if tool_calls:
            results = []
            for call in tool_calls:
                tool_name = call.get("name")
                args = call.get("arguments", {})
                if tool_name in self.tools:
                    try:
                        result = self.tools[tool_name].execute(**args)
                    except Exception as e:
                        result = f"Error executing tool {tool_name}: {str(e)}"
                    results.append(result)
                else:
                    results.append(f"Tool {tool_name} not found.")
            observation = f"<observation>{json.dumps(results)}</observation>"
            self.conversation_history.append({"role": "user", "content": observation})
            return self.run("")
        else:
            return response
