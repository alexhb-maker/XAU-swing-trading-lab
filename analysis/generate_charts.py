"""
Generates the analysis charts used in the README and statistical summary
from data/operations.csv.

Run from the repo root:
    python analysis/generate_charts.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "operations.csv"
OUT = ROOT / "analysis" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
})

BLUE = "#4C72B0"
ORANGE = "#DD8452"
GREEN = "#55A868"
RED = "#C44E52"
GRAY = "#8C8C8C"

df = pd.read_csv(DATA, parse_dates=["date_start", "date_end"])
executed = df[df["outcome"] != "No entry"].copy()
executed["is_win"] = executed["outcome"] == "Win"

# ---------------------------------------------------------------------------
# 1. Win rate by confluence count
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
grp = executed.groupby("confluences_count")["is_win"].agg(["mean", "count"])
grp["win_rate"] = grp["mean"] * 100
bars = ax.bar(grp.index.astype(str), grp["win_rate"], color=BLUE, width=0.6)
for i, (idx, row) in enumerate(grp.iterrows()):
    ax.text(i, row["win_rate"] + 2, f"{row['win_rate']:.0f}%\n(n={int(row['count'])})",
            ha="center", va="bottom", fontsize=10)
ax.axhline(50, color=GRAY, linestyle="--", linewidth=1, label="Coin-flip (50%)")
ax.set_ylim(0, 100)
ax.set_xlabel("Confluences met (of 4)")
ax.set_ylabel("Win rate (%)")
ax.set_title("Win Rate by Number of Confluences Met")
ax.legend(loc="upper left", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "win_rate_by_confluences.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 2. Long vs Short win rate
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
dir_grp = executed.groupby("direction")["is_win"].agg(["mean", "count"])
dir_grp["win_rate"] = dir_grp["mean"] * 100
colors = [GREEN, ORANGE]
bars = ax.bar(dir_grp.index, dir_grp["win_rate"], color=colors, width=0.5)
for i, (idx, row) in enumerate(dir_grp.iterrows()):
    ax.text(i, row["win_rate"] + 2, f"{row['win_rate']:.0f}%\n(n={int(row['count'])})",
            ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_ylim(0, 100)
ax.set_ylabel("Win rate (%)")
ax.set_title("Win Rate: Long vs. Short")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "win_rate_long_vs_short.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 3. Norm compliance vs outcome
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
comp_grp = executed.groupby("norm_compliant")["is_win"].agg(["mean", "count"])
comp_grp["win_rate"] = comp_grp["mean"] * 100
order = ["Yes", "Partial", "No"]
comp_grp = comp_grp.reindex([o for o in order if o in comp_grp.index])
colors_map = {"Yes": GREEN, "Partial": ORANGE, "No": RED}
bars = ax.bar(comp_grp.index, comp_grp["win_rate"],
              color=[colors_map[i] for i in comp_grp.index], width=0.5)
for i, (idx, row) in enumerate(comp_grp.iterrows()):
    ax.text(i, row["win_rate"] + 2, f"{row['win_rate']:.0f}%\n(n={int(row['count'])})",
            ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_ylim(0, 100)
ax.set_ylabel("Win rate (%)")
ax.set_xlabel("Followed own entry rules?")
ax.set_title("Win Rate by Rule Compliance")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "win_rate_by_compliance.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 4. Timeline of outcomes with emotional state flagged
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 4.5))
color_map = {"Win": GREEN, "Loss": RED, "No entry": GRAY, "BE": ORANGE}
df_sorted = df.sort_values("op_id")
for _, row in df_sorted.iterrows():
    ax.scatter(row["date_start"], row["op_id"], s=140,
               color=color_map[row["outcome"]],
               edgecolor="black" if row["emotional_state"] != "Neutral" else "none",
               linewidth=2, zorder=3)
ax.plot(df_sorted["date_start"], df_sorted["op_id"], color=GRAY, alpha=0.3, zorder=1)

# annotate the May drawdown cluster
may_cluster = df_sorted[df_sorted["op_id"].isin([9, 10, 11])]
ax.annotate("Losing streak\n(emotional dysregulation\nwindow, May 5–19)",
            xy=(may_cluster["date_start"].iloc[1], 10),
            xytext=(pd.Timestamp("2026-03-10"), 13.5),
            fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))

from matplotlib.lines import Line2D
legend_elems = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=GREEN, markersize=10, label="Win"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=RED, markersize=10, label="Loss"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=GRAY, markersize=10, label="No entry"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="white", markeredgecolor="black",
           markeredgewidth=2, markersize=10, label="Non-neutral emotional state"),
]
ax.legend(handles=legend_elems, loc="upper left", frameon=False, ncol=2)
ax.set_ylabel("Trade # (op_id)")
ax.set_title("Trade Timeline — Outcome and Emotional State")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig(OUT / "timeline_outcomes.png", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------------
# 5. Outcome breakdown (donut-free, simple bar)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
outcome_counts = df["outcome"].value_counts().reindex(["Win", "Loss", "No entry", "BE"]).dropna()
colors_list = [color_map[o] for o in outcome_counts.index]
bars = ax.bar(outcome_counts.index, outcome_counts.values, color=colors_list, width=0.5)
for i, v in enumerate(outcome_counts.values):
    ax.text(i, v + 0.15, str(v), ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_ylabel("Number of trades")
ax.set_title(f"Outcome Breakdown (n={len(df)} logged trades)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "outcome_breakdown.png", bbox_inches="tight")
plt.close()

print("Charts written to", OUT)
for f in sorted(OUT.glob("*.png")):
    print(" -", f.name)
