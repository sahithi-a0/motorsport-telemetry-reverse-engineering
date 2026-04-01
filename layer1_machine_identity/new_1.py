import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── CONFIG ─────────────────────────────────────────────────────────────────
CSV_PATH = r'C:\Users\sahit\OneDrive\Documents\assignments_ARCVD\Driver 3 Qualifying 1.csv'

BEACON_MARKERS = [0, 164.395, 241.9, 317.015, 390.191,
                  464.121, 536.206, 607.53, 678.718, 772.486, 832.994]

BEST_LAP_START = 607.53
BEST_LAP_END   = 678.718
FLYING_START   = 317.015
FLYING_END     = 678.718

GEAR_COLORS = {1: '#E24B4A', 2: '#EF9F27', 3: '#1D9E75',
               4: '#378ADD', 5: '#7F77DD'}

# ── LOAD & CLEAN ───────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH, skiprows=6, header=0, low_memory=False)
df = df[df['Time'] != 's'].dropna(subset=['Time']).reset_index(drop=True)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Gear_int'] = df['Gear'].round().astype('Int64')
df.loc[df['Gear_int'] < 1, 'Gear_int'] = pd.NA
df.loc[df['Gear_int'] > 5, 'Gear_int'] = pd.NA

best_lap = df[(df['Time'] >= BEST_LAP_START) & (df['Time'] <= BEST_LAP_END)].copy()
best_lap['Lap_Time'] = best_lap['Time'] - BEST_LAP_START
flying   = df[(df['Time'] >= FLYING_START) & (df['Time'] <= FLYING_END)].copy()
rev_limit = df['Engine RPM'].max()

# ── STYLE ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f0f0f',
    'axes.facecolor':   '#1a1a1a',
    'axes.edgecolor':   '#333333',
    'axes.labelcolor':  '#cccccc',
    'axes.titlecolor':  '#ffffff',
    'xtick.color':      '#888888',
    'ytick.color':      '#888888',
    'text.color':       '#cccccc',
    'grid.color':       '#2a2a2a',
    'grid.linewidth':   0.6,
    'font.family':      'monospace',
    'axes.titlesize':   12,
    'axes.labelsize':   10,
    'xtick.labelsize':  9,
    'ytick.labelsize':  9,
})

# ── PLOT 1 · Speed over Time ───────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(16, 6))
fig1.canvas.manager.set_window_title('Plot 1 — Speed over Time')

ax1.plot(df['Time'], df['Speed'],
         color='#378ADD', linewidth=0.8, alpha=0.9, label='Vehicle Speed')
ax1.plot(df['Time'], df['GPS Speed'],
         color='#E24B4A', linewidth=0.7, alpha=0.5, label='GPS Speed')
ax1.axvspan(BEST_LAP_START, BEST_LAP_END,
            color='#1D9E75', alpha=0.12, label='Best lap (L8)')
ax1.axvspan(678.718, 772.486,
            color='#E24B4A', alpha=0.10, label='Anomaly lap (L9)')

for t in BEACON_MARKERS[1:]:
    ax1.axvline(t, color='#555555', linewidth=0.7, linestyle='--')

lap_mids = [(BEACON_MARKERS[i] + BEACON_MARKERS[i+1]) / 2
            for i in range(len(BEACON_MARKERS)-1)]
for lx, ln in zip(lap_mids, [f'L{i+1}' for i in range(len(lap_mids))]):
    ax1.text(lx, 198, ln, fontsize=8, color='#666666', ha='center', va='top')

max_s_idx = df['Speed'].idxmax()
ax1.annotate(f"  {df['Speed'].max():.0f} km/h",
             xy=(df.loc[max_s_idx, 'Time'], df['Speed'].max()),
             fontsize=8, color='#EF9F27')

ax1.set_title('PLOT 1 — Speed over Time  |  full session  |  peaks=straights  troughs=corners', loc='left')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Speed (km/h)')
ax1.set_ylim(-5, 210)
ax1.set_xlim(0, 835)
ax1.legend(loc='upper right', fontsize=8, framealpha=0.3)
ax1.grid(True, axis='y')
fig1.tight_layout()

# ── PLOT 2 · RPM over Time ─────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(16, 6))
fig2.canvas.manager.set_window_title('Plot 2 — RPM over Lap Time (Best Lap)')

ax2.plot(best_lap['Lap_Time'], best_lap['Engine RPM'],
         color='#333333', linewidth=0.9, zorder=1)

for g in [1, 2, 3, 4, 5]:
    seg = best_lap[best_lap['Gear_int'] == g]
    if seg.empty: continue
    ax2.scatter(seg['Lap_Time'], seg['Engine RPM'],
                s=4, color=GEAR_COLORS[g], alpha=0.85,
                label=f'Gear {g}', zorder=3)

ax2.axhline(rev_limit, color='#E24B4A', linewidth=1.0, linestyle=':', alpha=0.7)
ax2.annotate(f'Rev limit: {rev_limit:.0f} rpm',
             xy=(1, rev_limit + 80), fontsize=8, color='#E24B4A')

ax2.set_title('PLOT 2 — Engine RPM over Lap Time  |  best lap L8  |  colour=gear  |  flat top=rev limiter', loc='left')
ax2.set_xlabel('Lap Time (s)')
ax2.set_ylabel('Engine RPM')
ax2.set_xlim(0, BEST_LAP_END - BEST_LAP_START + 1)
ax2.set_ylim(0, 7200)
ax2.legend(loc='lower right', fontsize=8, framealpha=0.3, markerscale=4, ncol=3)
ax2.grid(True, axis='y')
fig2.tight_layout()

# ── PLOT 3 · RPM vs Speed (gearbox map) ───────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(14, 8))
fig3.canvas.manager.set_window_title('Plot 3 — Gearbox Map (RPM vs Speed)')

for g in [1, 2, 3, 4, 5]:
    seg = flying[(flying['Gear_int'] == g) & (flying['Speed'] > 5)]
    if seg.empty: continue
    ax3.scatter(seg['Speed'], seg['Engine RPM'],
                s=5, color=GEAR_COLORS[g], alpha=0.6,
                label=f'Gear {g}', zorder=3)
    if len(seg) > 10:
        z  = np.polyfit(seg['Speed'], seg['Engine RPM'], 1)
        xs = np.linspace(seg['Speed'].min(), seg['Speed'].max(), 200)
        ax3.plot(xs, np.poly1d(z)(xs),
                 color=GEAR_COLORS[g], linewidth=2.0, alpha=0.9, zorder=4)
    ax3.text(seg['Speed'].median(),
             seg['Engine RPM'].median() + 220,
             f'G{g}', fontsize=10, color=GEAR_COLORS[g],
             fontweight='bold', ha='center')

ax3.axhline(rev_limit, color='#E24B4A', linewidth=1.0, linestyle=':', alpha=0.6)
ax3.annotate(f'Rev limit: {rev_limit:.0f} rpm',
             xy=(5, rev_limit + 60), fontsize=8, color='#E24B4A')

ax3.set_title('PLOT 3 — RPM vs Speed by Gear  |  flying laps L4–L8  |  each stripe = one gear ratio', loc='left')
ax3.set_xlabel('Vehicle Speed (km/h)')
ax3.set_ylabel('Engine RPM')
ax3.set_xlim(0, 200)
ax3.set_ylim(0, 7200)
ax3.legend(loc='upper left', fontsize=8, framealpha=0.3, markerscale=4)
ax3.grid(True)
fig3.tight_layout()

# ── PLOT 4 · Gear vs Time ──────────────────────────────────────────────────
fig4, ax4 = plt.subplots(figsize=(16, 6))
fig4.canvas.manager.set_window_title('Plot 4 — Gear Staircase (Best Lap)')

ax4.step(best_lap['Lap_Time'], best_lap['Gear_int'],
         where='post', color='#444444', linewidth=1.2, zorder=1)

for g in [1, 2, 3, 4, 5]:
    seg = best_lap[best_lap['Gear_int'] == g]
    if seg.empty: continue
    ax4.scatter(seg['Lap_Time'], seg['Gear_int'],
                s=8, color=GEAR_COLORS[g], alpha=0.9,
                label=f'Gear {g}', zorder=3)

ax4b = ax4.twinx()
ax4b.plot(best_lap['Lap_Time'], best_lap['Speed'],
          color='#378ADD', linewidth=1.0, alpha=0.35, label='Speed')
ax4b.set_ylabel('Speed (km/h)', color='#378ADD', fontsize=9)
ax4b.tick_params(axis='y', colors='#378ADD', labelsize=8)
ax4b.set_ylim(0, 220)

ax4.set_title('PLOT 4 — Gear vs Lap Time  |  best lap L8  |  staircase up=acceleration  drop=braking', loc='left')
ax4.set_xlabel('Lap Time (s)')
ax4.set_ylabel('Gear')
ax4.set_ylim(0, 6)
ax4.set_yticks([1, 2, 3, 4, 5])
ax4.set_xlim(0, BEST_LAP_END - BEST_LAP_START + 1)
ax4.legend(loc='upper right', fontsize=8, framealpha=0.3, markerscale=3, ncol=5)
ax4.grid(True, axis='y')
fig4.tight_layout()

# ── SHOW ALL ───────────────────────────────────────────────────────────────
plt.show()