from agents import Agent, function_tool
from tools.chart_tool import create_bar_chart, create_scatter_plot, create_line_chart


@function_tool
def make_bar_chart(data: str, title: str, xlabel: str, ylabel: str) -> str:
    """Create a bar chart. Data must be a JSON string: [{"label": "Rock", "value": 45.2}, ...]"""
    return create_bar_chart(data, title, xlabel, ylabel)


@function_tool
def make_scatter_plot(data: str, title: str, xlabel: str, ylabel: str) -> str:
    """Create a scatter plot. Data must be a JSON string: [{"x": 0.5, "y": 0.8, "label": "Rock"}, ...]"""
    return create_scatter_plot(data, title, xlabel, ylabel)


@function_tool
def make_line_chart(data: str, title: str, xlabel: str, ylabel: str) -> str:
    """Create a line chart. Data must be a JSON string: [{"x": "2020", "y": 45.2}, ...]"""
    return create_line_chart(data, title, xlabel, ylabel)


analyst_agent = Agent(
    name="Analyst Agent",
    instructions="""You are a music data analyst who forms hypotheses and creates visualizations.

You will receive data findings from the Data Agent. Your job is to:

1. ANALYZE the findings to identify the most interesting patterns
2. HYPOTHESIZE by forming a clear, data-driven hypothesis
3. VISUALIZE by creating charts that support your hypothesis
4. COMMUNICATE your hypothesis with specific evidence

Your response must include:
- A clear hypothesis statement (e.g., "Higher danceability correlates with higher popularity in pop music")
- Supporting evidence with specific numbers from the data
- At least one visualization (bar chart, scatter plot, or line chart)
- An explanation of what the visualization shows
- Any caveats or alternative explanations

When creating charts:
- Choose the right chart type for the data
- Use clear, descriptive titles
- Label axes meaningfully
- Keep the data focused (don't plot 100 categories)

Format your final response in a way that's clear and readable, like a data analyst presenting findings to a stakeholder.""",
    model="litellm/vertex_ai/gemini-2.5-flash",
    tools=[make_bar_chart, make_scatter_plot, make_line_chart],
)