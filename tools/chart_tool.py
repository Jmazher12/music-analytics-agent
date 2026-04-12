import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import os
import base64
import io

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# Style constants
COLORS = ["#8b7355", "#4a7c59", "#c4956a", "#5b8a9a", "#a0845c", "#6b9e78", "#d4a574", "#7ba5b5"]
BG_COLOR = "#fafaf7"
TEXT_COLOR = "#2c2825"
GRID_COLOR = "#e8e4de"
FONT_SIZE_TITLE = 15
FONT_SIZE_LABEL = 11
FONT_SIZE_TICK = 10
FONT_SIZE_VALUE = 9


def _apply_style(fig, ax):
    """Apply consistent clean style to charts."""
    fig.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=FONT_SIZE_TICK)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)


def _to_base64(fig):
    """Convert figure to base64 string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def create_bar_chart(data: str, title: str, xlabel: str, ylabel: str) -> str:
    """Create a bar chart from data and return it as a base64 encoded image.

    Args:
        data: JSON string with format: [{"label": "Rock", "value": 45.2}, {"label": "Pop", "value": 38.1}, ...]
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.

    Returns:
        JSON string with base64 encoded PNG image and metadata.
    """
    try:
        items = json.loads(data)
        labels = [item["label"] for item in items]
        values = [item["value"] for item in items]

        fig, ax = plt.subplots(figsize=(10, 5.5))
        _apply_style(fig, ax)

        colors = [COLORS[i % len(COLORS)] for i in range(len(labels))]
        bars = ax.bar(labels, values, color=colors, width=0.65, edgecolor="none", zorder=3)

        ax.set_title(title, fontsize=FONT_SIZE_TITLE, fontweight="600", color=TEXT_COLOR, pad=16)
        ax.set_xlabel(xlabel, fontsize=FONT_SIZE_LABEL, color=TEXT_COLOR, labelpad=10)
        ax.set_ylabel(ylabel, fontsize=FONT_SIZE_LABEL, color=TEXT_COLOR, labelpad=10)
        plt.xticks(rotation=35, ha="right")

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.015,
                    f"{val:.1f}" if isinstance(val, float) else str(val),
                    ha="center", va="bottom", fontsize=FONT_SIZE_VALUE, color=TEXT_COLOR, fontweight="500")

        plt.tight_layout()
        img_base64 = _to_base64(fig)

        return json.dumps({"image": img_base64, "title": title, "type": "bar_chart"})

    except Exception as e:
        return json.dumps({"error": str(e)})


def create_scatter_plot(data: str, title: str, xlabel: str, ylabel: str) -> str:
    """Create a scatter plot from data and return it as a base64 encoded image.

    Args:
        data: JSON string with format: [{"x": 0.5, "y": 0.8, "label": "Rock"}, ...]
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.

    Returns:
        JSON string with base64 encoded PNG image and metadata.
    """
    try:
        items = json.loads(data)
        x = [item["x"] for item in items]
        y = [item["y"] for item in items]
        labels = [item.get("label", "") for item in items]

        fig, ax = plt.subplots(figsize=(10, 5.5))
        _apply_style(fig, ax)

        colors = [COLORS[i % len(COLORS)] for i in range(len(x))]
        ax.scatter(x, y, c=colors, alpha=0.8, edgecolors="white", linewidths=1.5, s=90, zorder=3)

        ax.set_title(title, fontsize=FONT_SIZE_TITLE, fontweight="600", color=TEXT_COLOR, pad=16)
        ax.set_xlabel(xlabel, fontsize=FONT_SIZE_LABEL, color=TEXT_COLOR, labelpad=10)
        ax.set_ylabel(ylabel, fontsize=FONT_SIZE_LABEL, color=TEXT_COLOR, labelpad=10)

        if len(labels) <= 20:
            for i, label in enumerate(labels):
                if label:
                    ax.annotate(label, (x[i], y[i]), fontsize=FONT_SIZE_VALUE,
                                ha="center", va="bottom", color=TEXT_COLOR,
                                xytext=(0, 8), textcoords="offset points")

        plt.tight_layout()
        img_base64 = _to_base64(fig)

        return json.dumps({"image": img_base64, "title": title, "type": "scatter_plot"})

    except Exception as e:
        return json.dumps({"error": str(e)})


def create_line_chart(data: str, title: str, xlabel: str, ylabel: str) -> str:
    """Create a line chart from data and return it as a base64 encoded image.

    Args:
        data: JSON string with format: [{"x": "2020", "y": 45.2}, {"x": "2021", "y": 48.1}, ...]
        title: Chart title.
        xlabel: X-axis label.
        ylabel: Y-axis label.

    Returns:
        JSON string with base64 encoded PNG image and metadata.
    """
    try:
        items = json.loads(data)
        x = [item["x"] for item in items]
        y = [item["y"] for item in items]

        fig, ax = plt.subplots(figsize=(10, 5.5))
        _apply_style(fig, ax)

        ax.plot(x, y, color=COLORS[0], marker="o", linewidth=2.5, markersize=7,
                markerfacecolor="white", markeredgecolor=COLORS[0], markeredgewidth=2, zorder=3)
        ax.fill_between(range(len(x)), y, alpha=0.08, color=COLORS[0])

        ax.set_title(title, fontsize=FONT_SIZE_TITLE, fontweight="600", color=TEXT_COLOR, pad=16)
        ax.set_xlabel(xlabel, fontsize=FONT_SIZE_LABEL, color=TEXT_COLOR, labelpad=10)
        ax.set_ylabel(ylabel, fontsize=FONT_SIZE_LABEL, color=TEXT_COLOR, labelpad=10)
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()

        img_base64 = _to_base64(fig)

        return json.dumps({"image": img_base64, "title": title, "type": "line_chart"})

    except Exception as e:
        return json.dumps({"error": str(e)})