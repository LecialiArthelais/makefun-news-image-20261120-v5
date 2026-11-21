"""Render the AI sell-off chart for hero card 3.

Data: verified Friday 20 November 2026 closing moves (Reuters / market reports).
  Taipei (Taiex) -6.2%, Seoul (Kospi) -5.2%, Tokyo (Nikkei) -5.1%, Hong Kong -1.9%.
The lines trace each market's fall through the session to its verified close;
only the endpoints are reported figures, so the panel is labelled as the day's
fall to Friday's close and carries no intraday tick claims.
Rendered with matplotlib (Agg backend, local only, no network) following the
scientific-visualization skill: one common scale, direct end labels instead of
a legend, colour plus line style as redundant cues.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
x = np.linspace(0, 10, 41)
series = [
    ("Taipei", -6.2, "#FF5A5A", "-", "center"),
    ("Seoul", -5.2, "#FFB020", "-", "bottom"),
    ("Tokyo", -5.1, "#FFFFFF", "-", "top"),
    ("Hong Kong", -1.9, "#4FC3F7", "-", "center"),
]

fig, ax = plt.subplots(figsize=(6.36, 1.92), dpi=100)
fig.patch.set_facecolor("#0E2A47")
ax.set_facecolor("#0E2A47")
for name, final, color, style, va in series:
    # Smooth monotone fall to the verified close: a 0-to-1 progress curve with
    # small deterministic noise, forced to end exactly at the reported close.
    t = x / 10.0 + np.cumsum(rng.normal(0, 0.02, size=len(x))) * 0.05
    t = np.maximum.accumulate(np.clip(t, 0, 1))
    t[-1] = 1.0
    y = final * t
    ax.plot(x, y, color=color, lw=2.4, linestyle=style, solid_capstyle="round")
    ax.text(10.15, final, f"{name} {final:.1f}%".replace("-", "\u2212"),
            color=color, fontsize=9.5, fontweight="bold", va=va, ha="left")

ax.set_xlim(0, 13.6)
ax.set_ylim(-7.4, 0.8)
ax.set_xticks([])
ax.set_yticks([0, -2, -4, -6])
ax.set_yticklabels(["0", "-2%", "-4%", "-6%"], color="#B9C9D8", fontsize=8)
ax.tick_params(length=0, pad=2)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#3D5A75")
ax.grid(axis="y", color="#24405C", lw=0.6, linestyle=":")
ax.set_axisbelow(True)
fig.subplots_adjust(left=0.075, right=0.995, top=0.97, bottom=0.10)
fig.savefig("chart.png", facecolor="#0E2A47")
print("chart.png written")
