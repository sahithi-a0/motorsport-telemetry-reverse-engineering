import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── CONFIG ─────────────────────────────────────────────────────────────────
# NOTE: Data files are not included in this repository.
# To run this code, replace CSV_PATH with your own 
# telemetry data file path in the same format.
CSV_PATH = r'Driver 3 Qualifying 1.csv'

BEST_LAP_START = 607.53
BEST_LAP_END   = 678.718
FLYING_START   = 164.395
FLYING_END     = 678.718

# ── LOAD & CLEAN ───────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH, skiprows=6, header=0, low_memory=False)
df = df[df['Time'] != 's'].dropna(subset=['Time']).reset_index(drop=True)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

flying   = df[(df['Time'] >= FLYING_START) & (df['Time'] <= FLYING_END)].copy()
best_lap = df[(df['Time'] >= BEST_LAP_START) & (df['Time'] <= BEST_LAP_END)].copy()
best_lap['Lap_Time'] = best_lap['Time'] - BEST_LAP_START

# ── FIX DISTANCE — reset to 0 at lap start ─────────────────────────────────
dist_offset      = best_lap['Distance on GPS Speed'].iloc[0]
best_lap['Dist'] = best_lap['Distance on GPS Speed'] - dist_offset
lap_length       = best_lap['Dist'].iloc[-1]

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

# ── PLOT 1 · Track Map ─────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(10, 10))
fig1.canvas.manager.set_window_title('Plot 1 — Track Map')

track = flying[
    (flying['GPS PosAccuracy'] < 10) &
    (flying['GPS Nsat'] >= 4)
].copy()

sc = ax1.scatter(
    track['GPS Longitude'],
    track['GPS Latitude'],
    c=track['Speed'],
    cmap='RdYlGn_r',
    s=2, alpha=0.8
)

cbar = plt.colorbar(sc, ax=ax1, pad=0.02)
cbar.set_label('Speed (km/h)', color='#cccccc')
cbar.ax.yaxis.set_tick_params(color='#cccccc')
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#cccccc')

sf = best_lap.iloc[0]
ax1.scatter(sf['GPS Longitude'], sf['GPS Latitude'],
            color='white', s=120, zorder=5, marker='*', label='Start/Finish')

ax1.set_title('PLOT 1 — Track Map  |  flying laps  |  colour = speed  |  red=fast  green=slow',
              loc='left', pad=10)
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.legend(fontsize=8, framealpha=0.3)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.2)
fig1.tight_layout()

# ── PLOT 2 · Elevation Profile ─────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(16, 6))
fig2.canvas.manager.set_window_title('Plot 2 — Elevation Profile')

# use corrected lap distance
elev = best_lap[['Dist', 'GPS Altitude', 'Speed']].dropna()

from matplotlib.collections import LineCollection

points = np.array([elev['Dist'], elev['GPS Altitude']]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

norm = plt.Normalize(elev['Speed'].min(), elev['Speed'].max())
lc   = LineCollection(segments, cmap='RdYlGn_r', norm=norm,
                       linewidth=2.5, alpha=0.9)
lc.set_array(elev['Speed'].values)
ax2.add_collection(lc)

cbar2 = plt.colorbar(lc, ax=ax2, pad=0.02)
cbar2.set_label('Speed (km/h)', color='#cccccc')
cbar2.ax.yaxis.set_tick_params(color='#cccccc')
plt.setp(cbar2.ax.yaxis.get_ticklabels(), color='#cccccc')

ax2.fill_between(elev['Dist'], elev['GPS Altitude'],
                 elev['GPS Altitude'].min(),
                 color='#378ADD', alpha=0.08)

ax2.set_xlim(0, lap_length + 20)
ax2.set_ylim(elev['GPS Altitude'].min() - 5, elev['GPS Altitude'].max() + 5)
ax2.set_xticks(np.arange(0, lap_length + 1, 200))

# annotate high and low points
max_alt_idx = elev['GPS Altitude'].idxmax()
min_alt_idx = elev['GPS Altitude'].idxmin()
ax2.annotate(f"  highest: {elev['GPS Altitude'].max():.1f}m",
             xy=(elev.loc[max_alt_idx, 'Dist'], elev['GPS Altitude'].max()),
             fontsize=8, color='#EF9F27')
ax2.annotate(f"  lowest: {elev['GPS Altitude'].min():.1f}m",
             xy=(elev.loc[min_alt_idx, 'Dist'], elev['GPS Altitude'].min()),
             fontsize=8, color='#378ADD')

total_rise = elev['GPS Altitude'].max() - elev['GPS Altitude'].min()
ax2.set_title(f'PLOT 2 — Elevation Profile  |  best lap  |  lap length: {lap_length:.0f}m  |  elevation change: {total_rise:.1f}m  |  colour = speed',
              loc='left', pad=8)
ax2.set_xlabel('Distance from lap start (m)')
ax2.set_ylabel('Altitude (m)')
ax2.grid(True, alpha=0.3)
fig2.tight_layout()

# ── PLOT 3 · Corner Map (GPS Radius) ──────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(16, 6))
fig3.canvas.manager.set_window_title('Plot 3 — Corner Map (GPS Radius)')

corner = best_lap[['Dist', 'GPS Radius', 'Speed']].dropna().copy()
corner['GPS Radius'] = corner['GPS Radius'].clip(upper=500)

points3   = np.array([corner['Dist'], corner['GPS Radius']]).T.reshape(-1, 1, 2)
segments3 = np.concatenate([points3[:-1], points3[1:]], axis=1)
norm3     = plt.Normalize(corner['Speed'].min(), corner['Speed'].max())
lc3       = LineCollection(segments3, cmap='RdYlGn_r', norm=norm3,
                            linewidth=2.5, alpha=0.9)
lc3.set_array(corner['Speed'].values)
ax3.add_collection(lc3)

cbar3 = plt.colorbar(lc3, ax=ax3, pad=0.02)
cbar3.set_label('Speed (km/h)', color='#cccccc')
cbar3.ax.yaxis.set_tick_params(color='#cccccc')
plt.setp(cbar3.ax.yaxis.get_ticklabels(), color='#cccccc')

# shade tight corners
ax3.fill_between(corner['Dist'], 0, corner['GPS Radius'],
                 where=corner['GPS Radius'] < 50,
                 color='#E24B4A', alpha=0.15, label='Tight corners (<50m radius)')

# reference lines
for r, label, col in [(50,  'tight corner',  '#E24B4A'),
                       (150, 'medium corner', '#EF9F27'),
                       (300, 'fast sweeper',  '#1D9E75')]:
    ax3.axhline(r, color=col, linewidth=0.8, linestyle='--', alpha=0.5)
    ax3.text(lap_length + 8, r, label, fontsize=7, color=col, va='center')

ax3.set_xlim(0, lap_length + 60)
ax3.set_ylim(0, 520)
ax3.set_xticks(np.arange(0, lap_length + 1, 200))

ax3.set_title(f'PLOT 3 — Corner Map (GPS Radius)  |  best lap  |  lap length: {lap_length:.0f}m  |  low radius = tight corner  |  colour = speed',
              loc='left', pad=8)
ax3.set_xlabel('Distance from lap start (m)')
ax3.set_ylabel('Corner Radius (m)')
ax3.legend(fontsize=8, framealpha=0.3)
ax3.grid(True, alpha=0.3)
fig3.tight_layout()

plt.show()