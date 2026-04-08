"""Matplotlib charts for cache simulation results."""
import matplotlib.pyplot as plt


def plot_miss_rates(results, xlabel="Configuration", title="Cache Miss Rates"):
    """Bar chart of miss rates.

    results: list of dicts with keys 'label' and 'miss_rate'.
    """
    labels = [r["label"] for r in results]
    rates = [r["miss_rate"] * 100 for r in results]

    fig, ax = plt.subplots()
    ax.bar(labels, rates)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Miss Rate (%)")
    ax.set_title(title)
    ax.set_ylim(0, 100)
    plt.tight_layout()
    return fig
