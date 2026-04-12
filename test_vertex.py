import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from agents import Agent, Runner, function_tool, set_tracing_disabled
set_tracing_disabled(True)

@function_tool
def add_numbers(a: int, b: int) -> str:
    """Add two numbers together."""
    return str(a + b)

agent = Agent(
    name="Test Agent",
    instructions="You are a helpful assistant. Use the add_numbers tool when asked to add.",
    model="litellm/vertex_ai/gemini-2.5-flash",
    tools=[add_numbers],
)

async def main():
    result = await Runner.run(agent, "What is 17 + 25?")
    print(f"Result: {result.final_output}")

asyncio.run(main())