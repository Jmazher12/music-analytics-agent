from agents import Agent, Runner
import json
import asyncio


async def run_with_retry(agent, prompt, max_retries=3):
    """Run an agent with automatic retry on rate limit errors."""
    for attempt in range(max_retries):
        try:
            result = await Runner.run(agent, prompt)
            return result
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "RateLimit" in str(e):
                wait_time = 30 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                await asyncio.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded due to rate limiting. Please try again in a minute.")


async def run_data_agent(query: str) -> str:
    """Run the data agent to collect and explore data."""
    from my_agents.data_agent import data_agent
    result = await run_with_retry(data_agent, query)
    return result.final_output


async def run_analyst_agent(findings: str) -> dict:
    """Run the analyst agent to form hypotheses and create visualizations."""
    from my_agents.analyst_agent import analyst_agent
    result = await run_with_retry(analyst_agent, findings)

    # Extract charts from tool call results in the run history
    charts = []
    for item in result.new_items:
        if hasattr(item, 'output') and isinstance(item.output, str):
            try:
                chart_data = json.loads(item.output)
                if isinstance(chart_data, dict) and "image" in chart_data:
                    charts.append(chart_data)
            except (json.JSONDecodeError, TypeError):
                pass
        if hasattr(item, 'raw_item'):
            raw = item.raw_item
            if hasattr(raw, 'output') and isinstance(raw.output, str):
                try:
                    chart_data = json.loads(raw.output)
                    if isinstance(chart_data, dict) and "image" in chart_data:
                        charts.append(chart_data)
                except (json.JSONDecodeError, TypeError):
                    pass

    return {
        "text": result.final_output,
        "charts": charts,
    }


async def orchestrate(user_query: str) -> dict:
    """Run the full pipeline: collect data -> analyze -> hypothesize."""

    data_prompt = f"""The user asked: "{user_query}"

Collect relevant data from the Spotify database and explore it.
Search the knowledge base if you need to understand any audio features or genres.
Run multiple SQL queries to gather comprehensive data.
Summarize your findings with specific numbers and patterns."""

    data_findings = await run_data_agent(data_prompt)

    # Wait between agents to avoid rate limit
    await asyncio.sleep(15)

    analyst_prompt = f"""The user's original question: "{user_query}"

Here are the data findings from the Data Agent:

{data_findings}

Analyze these findings, form a hypothesis, create a visualization, and present
your conclusions with specific evidence from the data."""

    analyst_result = await run_analyst_agent(analyst_prompt)

    return {
        "data_findings": data_findings,
        "analysis": analyst_result["text"],
        "charts": analyst_result["charts"],
    }