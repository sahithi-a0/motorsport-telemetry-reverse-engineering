import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── CONFIG ──────────────────────────────────────────────────────────────────
FILES = {
    # NOTE: Data files are not included in this repository.
    # To run this code, replace CSV_PATH with your own 
    # telemetry data file path in the same format.
    'Driver 3': r'Driver 3 Qualifying 1.csv',
    'Driver 4': r'Driver 4  Qualifying 1.csv',
    'Driver 5': r'Driver 5  Qualifying 1.csv',
}
BEST_LAPS = {
    'Driver 3': (607.530, 678.718),
    'Driver 4': (527.833, 597.620),
    'Driver 5': (581.397, 649.906),
}
COLORS = {
    'Driver 3': '#378ADD',
    'Driver 4': '#E24B4A',
    'Driver 5': '#1D9E75',
}
BEST_TIMES = {
    'Driver 3': '1:11.20',
    'Driver 4': '1:09.80',
    'Driver 5': '1:08.50',
}
DT = 0.05

# ── HELPERS ──────────────────────────────────────────────────────────────────
def load(path):
    df = pd.read_csv(path, skiprows=6, header=0, low_memory=False)
    df = df[df['Time'] != 's'].dropna(subset=['Time']).reset_index(drop=True)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def get_best_lap(df, start, end):
    bl = df[(df['Time'] >= start) & (df['Time'] <= end)].copy()
    bl['Lap_Time'] = bl['Time'] - start
    bl['Dist'] = bl['Distance on GPS Speed'] - bl['Distance on GPS Speed'].iloc[0]
    return bl.reset_index(drop=True)

def parse_seg_times(path):
    raw = pd.read_csv(path, skiprows=0, header=None, nrows=10)
    def pt(t):
        try: p=str(t).split(':'); return float(p[0])*60+float(p[1])
        except: return None
    beacons  = [float(x) for x in raw.iloc[3,1:] if str(x) not in ['nan','']]
    segtimes = [pt(x) for x in raw.iloc[4,1:] if str(x) not in ['nan','']]
    return beacons, segtimes

def stat_panel(ax, lines, title=''):
    ax.set_facecolor('#111111')
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_edgecolor('#333333')
    if title:
        ax.text(0.5, 0.97, title, transform=ax.transAxes,
                fontsize=8, color='#EF9F27', fontweight='bold',
                ha='center', va='top')
    y = 0.86
    for label, value, color in lines:
        ax.text(0.05, y, label, transform=ax.transAxes,
                fontsize=7.5, color='#888888', va='top')
        ax.text(0.95, y, value, transform=ax.transAxes,
                fontsize=7.5, color=color, va='top',
                ha='right', fontweight='bold')
        y -= 0.11

plt.rcParams.update({
    'figure.facecolor': '#0f0f0f', 'axes.facecolor':  '#1a1a1a',
    'axes.edgecolor':   '#333333', 'axes.labelcolor': '#cccccc',
    'axes.titlecolor':  '#ffffff', 'xtick.color':     '#888888',
    'ytick.color':      '#888888', 'text.color':      '#cccccc',
    'grid.color':       '#2a2a2a', 'grid.linewidth':  0.5,
    'font.family':      'monospace','axes.titlesize':  10,
    'axes.labelsize':   9,         'xtick.labelsize': 8,
    'ytick.labelsize':  8,
})

# ── LOAD ─────────────────────────────────────────────────────────────────────
data = {}
for drv, path in FILES.items():
    df = load(path)
    s, e = BEST_LAPS[drv]
    bl = get_best_lap(df, s, e)
    beacons, segtimes = parse_seg_times(path)
    valid_times = segtimes[1:-1]
    data[drv] = {
        'full': df, 'lap': bl,
        'beacons': beacons, 'segtimes': segtimes,
        'valid_times': valid_times,
        'lap_time': len(bl) * DT,
        'lap_len':  bl['Dist'].iloc[-1],
    }

# ── P1 · Lap Time Progression ────────────────────────────────────────────────
fig1 = plt.figure(figsize=(16, 7))
fig1.suptitle('Qualifying — P1: Lap Time Progression  |  all 3 drivers',
              color='white', fontsize=12)
fig1.canvas.manager.set_window_title('Q P1 — Lap Time Progression')

gs1 = gridspec.GridSpec(1, 2, figure=fig1, width_ratios=[5, 1],
                         wspace=0.05, top=0.88, bottom=0.10,
                         left=0.07, right=0.97)

ax1 = fig1.add_subplot(gs1[0, 0])
for drv in data:
    vt  = data[drv]['valid_times']
    lns = list(range(2, len(vt)+2))
    ax1.plot(lns, vt, color=COLORS[drv], linewidth=2,
             marker='o', markersize=5,
             label=f'{drv}  (best: {BEST_TIMES[drv]})')
    best_t = min(vt)
    best_l = lns[vt.index(best_t)]
    ax1.scatter(best_l, best_t, color=COLORS[drv],
                s=140, zorder=5, marker='*')
    ax1.annotate(f' {BEST_TIMES[drv]}',
                 xy=(best_l, best_t), fontsize=8, color=COLORS[drv])

ax1.set_xlabel('Lap Number')
ax1.set_ylabel('Lap Time (s)')
ax1.legend(fontsize=9, framealpha=0.3)
ax1.grid(True, alpha=0.3)
ax1.set_title('Star = best lap  |  trend shows tyre warm-up and improvement', loc='left', fontsize=9)

sp1 = fig1.add_subplot(gs1[0, 1])
lines1 = []
for drv in data:
    vt = data[drv]['valid_times']
    lines1 += [
        (f'{drv} best',   BEST_TIMES[drv],         COLORS[drv]),
        (f'{drv} worst',  f'{max(vt):.1f}s',       COLORS[drv]),
        (f'{drv} spread', f'{max(vt)-min(vt):.1f}s', COLORS[drv]),
    ]
stat_panel(sp1, lines1, 'Lap Times')
fig1.tight_layout(rect=[0, 0, 1, 0.94])

# ── P2 · Speed Trace Overlay ─────────────────────────────────────────────────
fig2 = plt.figure(figsize=(16, 7))
fig2.suptitle('Qualifying — P2: Speed Trace Overlay  |  best lap each driver aligned on distance',
              color='white', fontsize=12)
fig2.canvas.manager.set_window_title('Q P2 — Speed Trace')

gs2 = gridspec.GridSpec(1, 2, figure=fig2, width_ratios=[5, 1],
                         wspace=0.05, top=0.88, bottom=0.10,
                         left=0.07, right=0.97)

ax2 = fig2.add_subplot(gs2[0, 0])
for drv in data:
    bl = data[drv]['lap']
    ax2.plot(bl['Dist'], bl['Speed'],
             color=COLORS[drv], linewidth=1.0, alpha=0.85,
             label=f'{drv} ({BEST_TIMES[drv]})')

ax2.set_xlabel('Distance from lap start (m)')
ax2.set_ylabel('Speed (km/h)')
ax2.legend(fontsize=9, framealpha=0.3)
ax2.grid(True, alpha=0.3)
ax2.set_title('Peaks = straights  troughs = corners  |  gap between lines = speed difference',
              loc='left', fontsize=9)
ax2.set_xlim(0, max(data[d]['lap_len'] for d in data) + 20)

sp2 = fig2.add_subplot(gs2[0, 1])
lines2 = []
for drv in data:
    bl = data[drv]['lap']
    lines2 += [
        (f'{drv} top',    f'{bl["Speed"].max():.0f} km/h',         COLORS[drv]),
        (f'{drv} min',    f'{bl["Speed"][bl["Speed"]>10].min():.0f} km/h', COLORS[drv]),
        (f'{drv} avg',    f'{bl["Speed"].mean():.0f} km/h',         COLORS[drv]),
    ]
stat_panel(sp2, lines2, 'Speed')
fig2.tight_layout(rect=[0, 0, 1, 0.94])

# ── P3 · Lap Delta ────────────────────────────────────────────────────────────
fig3 = plt.figure(figsize=(16, 11))
fig3.suptitle('Qualifying — P3: Lap Delta  |  below zero = left driver faster',
              color='white', fontsize=12)
fig3.canvas.manager.set_window_title('Q P3 — Lap Delta')

drivers = list(data.keys())
pairs   = [(drivers[0], drivers[1]),
           (drivers[0], drivers[2]),
           (drivers[1], drivers[2])]

gs3 = gridspec.GridSpec(3, 2, figure=fig3, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.90, bottom=0.06, left=0.07, right=0.97)

for row, (d1, d2) in enumerate(pairs):
    ax = fig3.add_subplot(gs3[row, 0])
    bl1 = data[d1]['lap']
    bl2 = data[d2]['lap']
    dmin = max(bl1['Dist'].min(), bl2['Dist'].min())
    dmax = min(bl1['Dist'].max(), bl2['Dist'].max())
    common = np.linspace(dmin, dmax, 600)
    t1 = np.interp(common, bl1['Dist'].values, bl1['Lap_Time'].values)
    t2 = np.interp(common, bl2['Dist'].values, bl2['Lap_Time'].values)
    delta = t1 - t2

    ax.fill_between(common, 0, delta, where=delta >= 0,
                    color=COLORS[d2], alpha=0.65, label=f'{d2} faster')
    ax.fill_between(common, 0, delta, where=delta < 0,
                    color=COLORS[d1], alpha=0.65, label=f'{d1} faster')
    ax.axhline(0, color='#666666', linewidth=0.8)
    ax.set_ylabel('Delta (s)')
    ax.legend(fontsize=8, framealpha=0.3, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'{d1} vs {d2}', loc='left', fontsize=9)
    if row == 2: ax.set_xlabel('Distance from lap start (m)')

    sp = fig3.add_subplot(gs3[row, 1])
    t1_total = data[d1]['lap_time']
    t2_total = data[d2]['lap_time']
    gap = t1_total - t2_total
    d1_faster_dist = np.sum(delta < 0) / len(delta) * dmax
    d2_faster_dist = np.sum(delta >= 0) / len(delta) * dmax
    stat_panel(sp, [
        (f'{d1} lap',      BEST_TIMES[d1],                     COLORS[d1]),
        (f'{d2} lap',      BEST_TIMES[d2],                     COLORS[d2]),
        ('Gap',            f'{abs(gap):.2f}s',                  '#EF9F27'),
        (f'{d1} faster',   f'{d1_faster_dist:.0f}m',            COLORS[d1]),
        (f'{d2} faster',   f'{d2_faster_dist:.0f}m',            COLORS[d2]),
    ], 'Delta')

fig3.tight_layout(rect=[0, 0, 1, 0.94])

# ── P4 · Lap Time Heatmap ─────────────────────────────────────────────────────
fig4 = plt.figure(figsize=(16, 6))
fig4.suptitle('Qualifying — P4: Lap Time Heatmap  |  green=fast  red=slow',
              color='white', fontsize=12)
fig4.canvas.manager.set_window_title('Q P4 — Lap Heatmap')

gs4 = gridspec.GridSpec(1, 2, figure=fig4, width_ratios=[5, 1],
                         wspace=0.05, top=0.88, bottom=0.10,
                         left=0.07, right=0.97)

ax4 = fig4.add_subplot(gs4[0, 0])
all_segs, drv_names = [], []
for drv in data:
    all_segs.append(data[drv]['valid_times'])
    drv_names.append(drv)

max_laps = max(len(s) for s in all_segs)
matrix   = np.full((len(drv_names), max_laps), np.nan)
for i, segs in enumerate(all_segs):
    matrix[i, :len(segs)] = segs

im   = ax4.imshow(matrix, aspect='auto', cmap='RdYlGn_r', interpolation='nearest')
cbar = plt.colorbar(im, ax=ax4, pad=0.02, fraction=0.03)
cbar.set_label('Lap Time (s)', color='#cccccc', fontsize=8)
cbar.ax.yaxis.set_tick_params(color='#cccccc', labelsize=7)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#cccccc')

ax4.set_yticks(range(len(drv_names)))
ax4.set_yticklabels(drv_names)
ax4.set_xlabel('Lap Number')
ax4.set_title('Each cell = one lap time  |  star marks best lap per driver', loc='left', fontsize=9)

for i in range(matrix.shape[0]):
    best_in_row = np.nanmin(matrix[i])
    for j in range(matrix.shape[1]):
        if not np.isnan(matrix[i, j]):
            t = matrix[i, j]
            txt = f'{int(t//60)}:{t%60:05.2f}'
            ax4.text(j, i, txt, ha='center', va='center',
                     fontsize=6.5, color='white')
            if t == best_in_row:
                ax4.text(j, i-0.35, '★', ha='center',
                         fontsize=7, color='#EF9F27')

sp4 = fig4.add_subplot(gs4[0, 1])
lines4 = []
for drv in data:
    vt = data[drv]['valid_times']
    lines4 += [
        (f'{drv} best',  BEST_TIMES[drv],              COLORS[drv]),
        (f'{drv} avg',   f'{np.mean(vt):.1f}s',        COLORS[drv]),
        (f'{drv} laps',  f'{len(vt)}',                  COLORS[drv]),
    ]
stat_panel(sp4, lines4, 'Summary')
fig4.tight_layout(rect=[0, 0, 1, 0.94])

plt.show()