
import json

from groq import Groq
from pydantic import ValidationError

from cloud_tool_config import TOOL_CONFIG

MODEL = "openai/gpt-oss-20b"
MAX_ITERATIONS = 10
MAX_TOOL_EXECUTIONS = 12


def execute_tool(tool_name: str, arguments: dict):
    config = TOOL_CONFIG.get(tool_name)

    if config is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    function = config["function"]
    argument_model = config["arguments"]

    if argument_model is None:
        return function()

    validated = argument_model.model_validate(arguments)
    return function(**validated.model_dump())


def build_groq_tools():
    tools = []

    for name, config in TOOL_CONFIG.items():
        argument_model = config["arguments"]

        if argument_model is None:
            parameters = {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            }
        else:
            parameters = argument_model.model_json_schema()

        tools.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": (
                        config["function"].__doc__
                        or f"Execute {name}"
                    ).strip(),
                    "parameters": parameters,
                },
            }
        )

    return tools


def run_groq_agent(user_message: str) -> tuple[str, list[dict]]:
    client = Groq()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Use calculation tools for arithmetic. "
                "Use search_knowledge_base for questions "
                "about the user's documents. "
                "Use get_current_datetime for the current "
                "date or time. "
                "Use exact tool results in your answers. "
                "Do not invent information."
            ),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    tools = build_groq_tools()
    trace = []
    tool_execution_count = 0

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        if not assistant_message.tool_calls:
            return assistant_message.content or "", trace

        for tool_call in assistant_message.tool_calls:
            if tool_execution_count >= MAX_TOOL_EXECUTIONS:
                return (
                    "Agent stopped: maximum tool executions reached.",
                    trace,
                )

            tool_execution_count += 1

            tool_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = execute_tool(tool_name, arguments)

            except (ValueError, TypeError, ValidationError) as exc:
                arguments = locals().get("arguments", {})
                result = f"Tool execution error: {exc}"

            except Exception as exc:
                arguments = locals().get("arguments", {})
                result = f"Tool execution error: {type(exc).__name__}"

            trace.append(
                {
                    "step": len(trace) + 1,
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result,
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "The agent reached its maximum number of steps.", trace
