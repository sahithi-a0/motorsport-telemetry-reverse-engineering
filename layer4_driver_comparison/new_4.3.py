import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

FILES = {
    'Driver 3': r'C:\Users\sahit\OneDrive\Documents\assignments_ARCVD\Driver 3 Qualifying 1.csv',
    'Driver 4': r'C:\Users\sahit\OneDrive\Documents\assignments_ARCVD\Driver 4  Qualifying 1.csv',
    'Driver 5': r'C:\Users\sahit\OneDrive\Documents\assignments_ARCVD\Driver 5  Qualifying 1.csv',
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

data = {}
for drv, path in FILES.items():
    df  = load(path)
    s, e = BEST_LAPS[drv]
    bl  = get_best_lap(df, s, e)
    thr = bl['Throttle Pos']
    brk = bl['Brake Pos']
    bp  = bl['Brake Press'].fillna(0)
    steer = bl['Steering Pos']
    gx  = bl['Lateral Acc']
    gy  = bl['Inline Acc']
    spd = bl['Speed']
    lap_time = len(bl) * DT
    d_thr   = np.gradient(thr.values, DT)
    d_steer = np.gradient(steer.values, DT)
    trail   = (thr > 5) & (brk > 5)
    combined= np.sqrt(gx**2 + gy**2)
    data[drv] = {
        'lap': bl, 'dist': bl['Dist'],
        'thr': thr, 'brk': brk, 'bp': bp,
        'steer': steer, 'gx': gx, 'gy': gy, 'spd': spd,
        'd_thr': d_thr, 'd_steer': d_steer,
        'trail': trail, 'combined': combined,
        'lap_time': lap_time,
        'lap_len':  bl['Dist'].iloc[-1],
    }

max_dist = max(data[d]['lap_len'] for d in data)

# ── P5 · Throttle + Brake Overlay ─────────────────────────────────────────────
fig5 = plt.figure(figsize=(16, 9))
fig5.suptitle('Qualifying — P5: Throttle & Brake Overlay  |  all 3 drivers best lap',
              color='white', fontsize=12)
fig5.canvas.manager.set_window_title('Q P5 — Throttle & Brake')

gs5 = gridspec.GridSpec(2, 2, figure=fig5, width_ratios=[5, 1],
                         hspace=0.3, wspace=0.05,
                         top=0.90, bottom=0.08, left=0.07, right=0.97)

ax5a = fig5.add_subplot(gs5[0, 0])
for drv in data:
    ax5a.plot(data[drv]['dist'], data[drv]['thr'],
              color=COLORS[drv], linewidth=0.9, alpha=0.85, label=drv)
ax5a.set_ylabel('Throttle (%)')
ax5a.set_ylim(-5, 115)
ax5a.legend(fontsize=8, framealpha=0.3, loc='upper right')
ax5a.grid(True, alpha=0.3)
ax5a.set_title('Throttle — who gets on throttle earliest after apex', loc='left', fontsize=9)
ax5a.set_xlim(0, max_dist + 20)

sp5a = fig5.add_subplot(gs5[0, 1])
lines5a = []
for drv in data:
    thr = data[drv]['thr']
    lt  = data[drv]['lap_time']
    lines5a += [
        (f'{drv} full≥99%', f'{(thr>=99).sum()*DT:.1f}s ({(thr>=99).sum()*DT/lt*100:.0f}%)', COLORS[drv]),
        (f'{drv} zero≤1%',  f'{(thr<=1).sum()*DT:.1f}s ({(thr<=1).sum()*DT/lt*100:.0f}%)',  COLORS[drv]),
    ]
stat_panel(sp5a, lines5a, 'Throttle')

ax5b = fig5.add_subplot(gs5[1, 0], sharex=ax5a)
for drv in data:
    ax5b.plot(data[drv]['dist'], data[drv]['brk'],
              color=COLORS[drv], linewidth=0.9, alpha=0.85, label=drv)
ax5b.set_ylabel('Brake (%)')
ax5b.set_ylim(-5, 115)
ax5b.legend(fontsize=8, framealpha=0.3, loc='upper right')
ax5b.grid(True, alpha=0.3)
ax5b.set_title('Brake — who brakes latest into corner  |  note: D4/D5 brake sensor scaling issue', loc='left', fontsize=9)
ax5b.set_xlabel('Distance from lap start (m)')

sp5b = fig5.add_subplot(gs5[1, 1])
lines5b = []
for drv in data:
    brk = data[drv]['brk']
    bp  = data[drv]['bp']
    lt  = data[drv]['lap_time']
    lines5b += [
        (f'{drv} on brake', f'{(brk>5).sum()*DT:.1f}s ({(brk>5).sum()*DT/lt*100:.0f}%)', COLORS[drv]),
        (f'{drv} max press',f'{bp.max():.1f} bar',                                         COLORS[drv]),
    ]
stat_panel(sp5b, lines5b, 'Brake')
fig5.tight_layout(rect=[0, 0, 1, 0.94])

# ── P6 · Trail Braking ────────────────────────────────────────────────────────
fig6 = plt.figure(figsize=(16, 10))
fig6.suptitle('Qualifying — P6: Trail Braking Gate  |  throttle>5% AND brake>5% simultaneously',
              color='white', fontsize=12)
fig6.canvas.manager.set_window_title('Q P6 — Trail Braking')

gs6 = gridspec.GridSpec(3, 2, figure=fig6, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.90, bottom=0.06, left=0.07, right=0.97)

for row, drv in enumerate(data):
    ax = fig6.add_subplot(gs6[row, 0])
    tb   = data[drv]['trail'].astype(int)
    dist = data[drv]['dist']
    ax.fill_between(dist, 0, tb, color=COLORS[drv], alpha=0.75, step='pre')
    ax.set_ylabel('Gate (1=on)', fontsize=8)
    ax.set_ylim(-0.1, 1.3)
    ax.set_yticks([0, 1])
    ax.grid(True, axis='y', alpha=0.3)
    ax.set_xlim(0, max_dist + 20)
    total = data[drv]['trail'].sum() * DT
    zones = sum(1 for i in range(1, len(data[drv]['trail']))
                if data[drv]['trail'].iloc[i] and not data[drv]['trail'].iloc[i-1])
    ax.set_title(f'{drv} — trail braking: {total:.1f}s  zones: {zones}', loc='left', fontsize=9)
    if row == 2: ax.set_xlabel('Distance from lap start (m)')

    sp = fig6.add_subplot(gs6[row, 1])
    lt = data[drv]['lap_time']
    stat_panel(sp, [
        ('Trail time',  f'{total:.1f}s',          COLORS[drv]),
        ('% of lap',    f'{total/lt*100:.0f}%',   COLORS[drv]),
        ('Zones',       f'{zones}',                '#cccccc'),
    ], drv[:6])

fig6.tight_layout(rect=[0, 0, 1, 0.94])

# ── P7 · Throttle Derivative ──────────────────────────────────────────────────
fig7 = plt.figure(figsize=(16, 11))
fig7.suptitle('Qualifying — P7: Throttle Rate dThrottle/dt  |  aggression signature per driver',
              color='white', fontsize=12)
fig7.canvas.manager.set_window_title('Q P7 — Throttle Derivative')

gs7 = gridspec.GridSpec(3, 2, figure=fig7, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.90, bottom=0.06, left=0.07, right=0.97)

for row, drv in enumerate(data):
    ax   = fig7.add_subplot(gs7[row, 0])
    dist = data[drv]['dist']
    dt_  = data[drv]['d_thr']
    ax.fill_between(dist, 0, dt_, where=dt_ >= 0,
                    color=COLORS[drv], alpha=0.75, label='Opening')
    ax.fill_between(dist, 0, dt_, where=dt_ < 0,
                    color='#555555', alpha=0.55, label='Closing')
    ax.axhline(0, color='#444444', linewidth=0.6)
    ax.set_ylabel('%/s', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, framealpha=0.3, loc='upper right')
    ax.set_xlim(0, max_dist + 20)
    ax.set_title(f'{drv}  |  max open: {np.max(dt_):.0f} %/s  max close: {np.min(dt_):.0f} %/s',
                 loc='left', fontsize=9)
    if row == 2: ax.set_xlabel('Distance from lap start (m)')

    sp = fig7.add_subplot(gs7[row, 1])
    stat_panel(sp, [
        ('Max open',    f'{np.max(dt_):.0f} %/s',                COLORS[drv]),
        ('Max close',   f'{np.min(dt_):.0f} %/s',                '#555555'),
        ('Mean open',   f'{np.mean(dt_[dt_>0]):.0f} %/s',        COLORS[drv]),
        ('Mean close',  f'{np.mean(dt_[dt_<0]):.0f} %/s',        '#888888'),
    ], drv[:6])

fig7.tight_layout(rect=[0, 0, 1, 0.94])

# ── P8 · Steering Derivative ──────────────────────────────────────────────────
fig8 = plt.figure(figsize=(16, 11))
fig8.suptitle('Qualifying — P8: Steering Rate dSteering/dt  |  smoothness signature per driver',
              color='white', fontsize=12)
fig8.canvas.manager.set_window_title('Q P8 — Steering Derivative')

gs8 = gridspec.GridSpec(3, 2, figure=fig8, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.90, bottom=0.06, left=0.07, right=0.97)

for row, drv in enumerate(data):
    ax   = fig8.add_subplot(gs8[row, 0])
    dist = data[drv]['dist']
    ds_  = data[drv]['d_steer']
    ax.fill_between(dist, 0, ds_, where=ds_ >= 0,
                    color='#EF9F27', alpha=0.75, label='Right/unwind')
    ax.fill_between(dist, 0, ds_, where=ds_ < 0,
                    color='#378ADD', alpha=0.75, label='Left/unwind')
    ax.axhline(0, color='#444444', linewidth=0.6)
    ax.set_ylabel('deg/s', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, framealpha=0.3, loc='upper right')
    ax.set_xlim(0, max_dist + 20)
    ax.set_title(f'{drv}  |  max R: {np.max(ds_):.0f} deg/s  max L: {np.min(ds_):.0f} deg/s  mean: {np.mean(np.abs(ds_)):.0f} deg/s',
                 loc='left', fontsize=9)
    if row == 2: ax.set_xlabel('Distance from lap start (m)')

    sp = fig8.add_subplot(gs8[row, 1])
    agg = (np.abs(ds_) > 200).sum() * DT
    stat_panel(sp, [
        ('Max rate R',  f'{np.max(ds_):.0f} deg/s',          '#EF9F27'),
        ('Max rate L',  f'{np.min(ds_):.0f} deg/s',          '#378ADD'),
        ('Mean |rate|', f'{np.mean(np.abs(ds_)):.0f} deg/s', '#cccccc'),
        ('>200 deg/s',  f'{agg:.1f}s',                        '#E24B4A'),
    ], drv[:6])

fig8.tight_layout(rect=[0, 0, 1, 0.94])

# ── P9 · GG Diagram ───────────────────────────────────────────────────────────
fig9 = plt.figure(figsize=(11, 10))
fig9.suptitle('Qualifying — P9: GG Diagram Overlay  |  all 3 drivers',
              color='white', fontsize=12)
fig9.canvas.manager.set_window_title('Q P9 — GG Diagram')

gs9 = gridspec.GridSpec(1, 2, figure=fig9, width_ratios=[3, 1],
                         wspace=0.05, top=0.90, bottom=0.08,
                         left=0.08, right=0.97)

ax9 = fig9.add_subplot(gs9[0, 0])
for drv in data:
    gx = data[drv]['gx']
    gy = data[drv]['gy']
    ax9.scatter(gx, gy, s=4, color=COLORS[drv], alpha=0.45, label=drv)
    g_env = np.percentile(np.sqrt(gx**2 + gy**2), 98)
    theta = np.linspace(0, 2*np.pi, 300)
    ax9.plot(g_env*np.cos(theta), g_env*np.sin(theta),
             color=COLORS[drv], linewidth=1.2,
             linestyle='--', alpha=0.7)

ax9.axhline(0, color='#444444', linewidth=0.7)
ax9.axvline(0, color='#444444', linewidth=0.7)
lim = max(np.percentile(np.sqrt(data[d]['gx']**2 + data[d]['gy']**2), 99)
          for d in data) * 1.05
ax9.set_xlim(-lim, lim)
ax9.set_ylim(-lim, lim)
ax9.text( lim*0.55,  lim*0.70, 'Accel\n+Right', fontsize=8, color='#666666', ha='center')
ax9.text(-lim*0.55,  lim*0.70, 'Accel\n+Left',  fontsize=8, color='#666666', ha='center')
ax9.text( lim*0.55, -lim*0.70, 'Brake\n+Right', fontsize=8, color='#666666', ha='center')
ax9.text(-lim*0.55, -lim*0.70, 'Brake\n+Left',  fontsize=8, color='#666666', ha='center')
ax9.set_xlabel('Lateral G  ← Left | Right →')
ax9.set_ylabel('Inline G   ↓ Brake | Accel ↑')
ax9.set_aspect('equal')
ax9.legend(fontsize=9, framealpha=0.3)
ax9.grid(True, alpha=0.25)
ax9.set_title('Dashed circle = grip envelope per driver  |  wider = more grip extracted',
              loc='left', fontsize=9)

sp9 = fig9.add_subplot(gs9[0, 1])
lines9 = []
for drv in data:
    gx = data[drv]['gx']
    gy = data[drv]['gy']
    combined = np.sqrt(gx**2 + gy**2)
    g_env = np.percentile(combined, 98)
    lines9 += [
        (f'{drv} lat G',   f'{gx.abs().max():.2f}g',  COLORS[drv]),
        (f'{drv} brk G',   f'{gy.min():.2f}g',         COLORS[drv]),
        (f'{drv} envelope',f'{g_env:.2f}g',             COLORS[drv]),
    ]
stat_panel(sp9, lines9, 'GG Stats')
fig9.tight_layout(rect=[0, 0, 1, 0.94])

plt.show()