import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── CONFIG ──────────────────────────────────────────────────────────────────
FILES = {
    # NOTE: Data files are not included in this repository.
    # To run this code, replace CSV_PATH with your own 
    # telemetry data file path in the same format.
    'Driver 3': r'Driver 3 Race 1.csv',
    'Driver 4': r'Driver 4 Race 1.csv',
    'Driver 5': r'Driver 5  Race 1.csv',
}
BEST_LAPS = {
    'Driver 3': (1510.440, 1584.420),
    'Driver 4': (1781.990, 1853.920),
    'Driver 5': (1761.430, 1832.170),
}
COLORS = {
    'Driver 3': '#378ADD',
    'Driver 4': '#E24B4A',
    'Driver 5': '#1D9E75',
}
DT = 0.05

# ── HELPERS ─────────────────────────────────────────────────────────────────
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
    for sp in ax.spines.values():
        sp.set_edgecolor('#333333')
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
        y -= 0.115

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
    data[drv] = {'full': df, 'lap': bl}

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 1 — THERMAL LOAD PROGRESSION (Water Temp + Oil Temp full race)
# ═══════════════════════════════════════════════════════════════════════════
fig1 = plt.figure(figsize=(17, 10))
fig1.suptitle('Layer 4 — P1: Thermal Load Progression  |  Race  |  all 3 drivers  |  full session',
              color='white', fontsize=12)
fig1.canvas.manager.set_window_title('L4 P1 — Thermal Load')

gs1 = gridspec.GridSpec(2, 2, figure=fig1, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.91, bottom=0.07, left=0.07, right=0.97)

# Water Temp
ax1a = fig1.add_subplot(gs1[0, 0])
for drv in data:
    df   = data[drv]['full']
    vals = df[['Time', 'Water Temp']].dropna()
    vals = vals[vals['Water Temp'] > 0]
    ax1a.plot(vals['Time'], vals['Water Temp'],
              color=COLORS[drv], linewidth=0.8, alpha=0.9, label=drv)
    # shade best lap window
    s, e = BEST_LAPS[drv]
    ax1a.axvspan(s, e, color=COLORS[drv], alpha=0.10)

# warning band
ax1a.axhspan(103, 120, color='#E24B4A', alpha=0.08, label='Warning zone >103°C')
ax1a.axhline(103, color='#E24B4A', linewidth=0.8,
             linestyle='--', alpha=0.6)
ax1a.set_ylabel('Water Temp (°C)')
ax1a.set_ylim(75, 115)
ax1a.legend(fontsize=7.5, framealpha=0.3, loc='upper left')
ax1a.grid(True, alpha=0.3)
ax1a.set_title('Water temperature — shaded = best lap window  |  red zone = thermal ceiling',
               loc='left', fontsize=9)

sp1a = fig1.add_subplot(gs1[0, 1])
lines1a = []
for drv in data:
    v     = data[drv]['full']['Water Temp'].dropna()
    v     = v[v > 0]
    start = v.iloc[:400].mean()
    end   = v.iloc[-400:].mean()
    lines1a += [
        (f'{drv} max',   f'{v.max():.1f}°C',    COLORS[drv]),
        (f'{drv} rise',  f'{end-start:+.1f}°C', COLORS[drv]),
    ]
stat_panel(sp1a, lines1a, 'Water Temp')

# Oil Temp
ax1b = fig1.add_subplot(gs1[1, 0], sharex=ax1a)
for drv in data:
    df   = data[drv]['full']
    vals = df[['Time', 'Oil Temp']].dropna()
    vals = vals[vals['Oil Temp'] > 0]
    ax1b.plot(vals['Time'], vals['Oil Temp'],
              color=COLORS[drv], linewidth=0.8, alpha=0.9, label=drv)
    s, e = BEST_LAPS[drv]
    ax1b.axvspan(s, e, color=COLORS[drv], alpha=0.10)

ax1b.axhspan(118, 135, color='#E24B4A', alpha=0.08, label='Warning zone >118°C')
ax1b.axhline(118, color='#E24B4A', linewidth=0.8,
             linestyle='--', alpha=0.6)
ax1b.set_ylabel('Oil Temp (°C)')
ax1b.set_ylim(65, 130)
ax1b.legend(fontsize=7.5, framealpha=0.3, loc='upper left')
ax1b.grid(True, alpha=0.3)
ax1b.set_title('Oil temperature — steeper rise = harder drivetrain load  |  >118°C = viscosity degradation',
               loc='left', fontsize=9)
ax1b.set_xlabel('Session Time (s)')

sp1b = fig1.add_subplot(gs1[1, 1])
lines1b = []
for drv in data:
    v     = data[drv]['full']['Oil Temp'].dropna()
    v     = v[v > 0]
    start = v.iloc[:400].mean()
    end   = v.iloc[-400:].mean()
    lines1b += [
        (f'{drv} max',   f'{v.max():.1f}°C',    COLORS[drv]),
        (f'{drv} rise',  f'{end-start:+.1f}°C', COLORS[drv]),
    ]
stat_panel(sp1b, lines1b, 'Oil Temp')
fig1.tight_layout(rect=[0, 0, 1, 0.95])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 2 — OIL PRESSURE vs RPM (best lap scatter + full session drop)
# ═══════════════════════════════════════════════════════════════════════════
fig2 = plt.figure(figsize=(17, 10))
fig2.suptitle('Layer 4 — P2: Oil Pressure vs RPM  |  Race  |  best lap scatter + full session trend',
              color='white', fontsize=12)
fig2.canvas.manager.set_window_title('L4 P2 — Oil Pressure')

gs2 = gridspec.GridSpec(2, 2, figure=fig2, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.91, bottom=0.07, left=0.07, right=0.97)

# Scatter — oil press vs RPM best lap
ax2a = fig2.add_subplot(gs2[0, 0])
stat_lines2a = []
for drv in data:
    bl    = data[drv]['lap']
    valid = bl[['Engine RPM', 'Oil Press']].dropna()
    valid = valid[valid['Oil Press'] > 0]
    ax2a.scatter(valid['Engine RPM'], valid['Oil Press'],
                 s=5, color=COLORS[drv], alpha=0.5, label=drv)
    if len(valid) > 20:
        z  = np.polyfit(valid['Engine RPM'], valid['Oil Press'], 1)
        xs = np.linspace(valid['Engine RPM'].min(),
                         valid['Engine RPM'].max(), 200)
        ax2a.plot(xs, np.poly1d(z)(xs),
                  color=COLORS[drv], linewidth=1.8, alpha=0.85)
        stat_lines2a += [
            (f'{drv} max',   f'{valid["Oil Press"].max():.2f} bar', COLORS[drv]),
            (f'{drv} min',   f'{valid["Oil Press"].min():.2f} bar', COLORS[drv]),
            (f'{drv} slope', f'{z[0]*1000:.3f} bar/krpm',           COLORS[drv]),
        ]

# warning band low pressure
ax2a.axhspan(0, 2.0, color='#E24B4A', alpha=0.10, label='Low pressure danger (<2 bar)')
ax2a.axhline(2.0, color='#E24B4A', linewidth=0.8, linestyle='--', alpha=0.6)
ax2a.set_xlabel('Engine RPM')
ax2a.set_ylabel('Oil Pressure (bar)')
ax2a.set_ylim(0, 6)
ax2a.legend(fontsize=7.5, framealpha=0.3)
ax2a.grid(True, alpha=0.3)
ax2a.set_title('Oil pressure vs RPM — healthy = rising slope  |  trend line = relationship per driver',
               loc='left', fontsize=9)

sp2a = fig2.add_subplot(gs2[0, 1])
stat_panel(sp2a, stat_lines2a, 'Best Lap\nOil Press')

# Full session oil pressure over time
ax2b = fig2.add_subplot(gs2[1, 0])
stat_lines2b = []
for drv in data:
    df   = data[drv]['full']
    vals = df[['Time', 'Oil Press']].dropna()
    vals = vals[vals['Oil Press'] > 0.5]
    # smooth with rolling window
    smoothed = vals['Oil Press'].rolling(window=100, center=True).mean()
    ax2b.plot(vals['Time'], smoothed,
              color=COLORS[drv], linewidth=1.2, alpha=0.85, label=drv)
    ax2b.fill_between(vals['Time'], smoothed, 0,
                      color=COLORS[drv], alpha=0.07)
    s, e = BEST_LAPS[drv]
    ax2b.axvspan(s, e, color=COLORS[drv], alpha=0.10)
    start_avg = vals['Oil Press'].iloc[:400].mean()
    end_avg   = vals['Oil Press'].iloc[-400:].mean()
    stat_lines2b += [
        (f'{drv} start', f'{start_avg:.2f} bar', COLORS[drv]),
        (f'{drv} end',   f'{end_avg:.2f} bar',   COLORS[drv]),
        (f'{drv} drop',  f'{start_avg-end_avg:.2f} bar', COLORS[drv]),
    ]

ax2b.axhspan(0, 2.0, color='#E24B4A', alpha=0.08)
ax2b.axhline(2.0, color='#E24B4A', linewidth=0.8, linestyle='--', alpha=0.6)
ax2b.set_ylabel('Oil Pressure (bar)')
ax2b.set_ylim(0, 6)
ax2b.set_xlabel('Session Time (s)')
ax2b.legend(fontsize=7.5, framealpha=0.3)
ax2b.grid(True, alpha=0.3)
ax2b.set_title('Oil pressure full race — smoothed 5s rolling mean  |  drop over race = oil degradation',
               loc='left', fontsize=9)

sp2b = fig2.add_subplot(gs2[1, 1])
stat_panel(sp2b, stat_lines2b, 'Full Race\nOil Press')
fig2.tight_layout(rect=[0, 0, 1, 0.95])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 3 — BATTERY VOLTAGE (full race + zoom on best lap)
# ═══════════════════════════════════════════════════════════════════════════
fig3 = plt.figure(figsize=(17, 10))
fig3.suptitle('Layer 4 — P3: Battery Voltage  |  Race  |  electrical health across full session',
              color='white', fontsize=12)
fig3.canvas.manager.set_window_title('L4 P3 — Battery Voltage')

gs3 = gridspec.GridSpec(2, 2, figure=fig3, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.91, bottom=0.07, left=0.07, right=0.97)

# Full session
ax3a = fig3.add_subplot(gs3[0, 0])
stat_lines3a = []
for drv in data:
    df   = data[drv]['full']
    vals = df[['Time', 'Battery Voltage']].dropna()
    vals = vals[vals['Battery Voltage'] > 5]
    ax3a.plot(vals['Time'], vals['Battery Voltage'],
              color=COLORS[drv], linewidth=0.8, alpha=0.9, label=drv)
    s, e = BEST_LAPS[drv]
    ax3a.axvspan(s, e, color=COLORS[drv], alpha=0.10)
    bv = vals['Battery Voltage']
    stat_lines3a += [
        (f'{drv} min',  f'{bv.min():.2f}V',  COLORS[drv]),
        (f'{drv} max',  f'{bv.max():.2f}V',  COLORS[drv]),
        (f'{drv} mean', f'{bv.mean():.2f}V', COLORS[drv]),
    ]

# warning bands
ax3a.axhspan(0, 11.5, color='#E24B4A', alpha=0.10,
             label='Sensor instability zone (<11.5V)')
ax3a.axhline(11.5, color='#E24B4A', linewidth=1.0,
             linestyle='--', alpha=0.7, label='11.5V threshold')
ax3a.axhspan(11.5, 11.8, color='#EF9F27', alpha=0.07,
             label='Marginal zone (11.5–11.8V)')
ax3a.set_ylabel('Battery Voltage (V)')
ax3a.set_ylim(10, 12.8)
ax3a.legend(fontsize=7, framealpha=0.3, loc='lower left', ncol=2)
ax3a.grid(True, alpha=0.3)
ax3a.set_title('Full race battery voltage — red zone = ECU/sensor instability risk',
               loc='left', fontsize=9)
ax3a.set_xlabel('Session Time (s)')

sp3a = fig3.add_subplot(gs3[0, 1])
stat_panel(sp3a, stat_lines3a, 'Battery V\nFull Race')

# Best lap zoom — voltage vs distance
ax3b = fig3.add_subplot(gs3[1, 0])
stat_lines3b = []
for drv in data:
    bl   = data[drv]['lap']
    vals = bl[['Dist', 'Battery Voltage']].dropna()
    vals = vals[vals['Battery Voltage'] > 5]
    ax3b.plot(vals['Dist'], bl.loc[vals.index, 'Battery Voltage'],
              color=COLORS[drv], linewidth=1.2, alpha=0.9, label=drv)
    bv = bl['Battery Voltage'].dropna()
    bv = bv[bv > 5]
    stat_lines3b += [
        (f'{drv} min', f'{bv.min():.2f}V', COLORS[drv]),
        (f'{drv} drop', f'{bv.max()-bv.min():.3f}V', COLORS[drv]),
    ]

ax3b.axhspan(0, 11.5, color='#E24B4A', alpha=0.10)
ax3b.axhline(11.5, color='#E24B4A', linewidth=0.8,
             linestyle='--', alpha=0.6)
ax3b.set_ylabel('Battery Voltage (V)')
ax3b.set_ylim(10, 12.8)
ax3b.set_xlabel('Distance from lap start (m)')
ax3b.legend(fontsize=7.5, framealpha=0.3)
ax3b.grid(True, alpha=0.3)
ax3b.set_title('Best lap zoom — voltage sag under high electrical load visible as dips',
               loc='left', fontsize=9)

sp3b = fig3.add_subplot(gs3[1, 1])
stat_panel(sp3b, stat_lines3b, 'Battery V\nBest Lap')
fig3.tight_layout(rect=[0, 0, 1, 0.95])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 4 — BRAKE PRESSURE vs ENTRY SPEED SCATTER (braking fingerprint)
# ═══════════════════════════════════════════════════════════════════════════
fig4 = plt.figure(figsize=(17, 10))
fig4.suptitle('Layer 4 — P4: Brake Pressure vs Entry Speed  |  Race best lap  |  braking fingerprint',
              color='white', fontsize=12)
fig4.canvas.manager.set_window_title('L4 P4 — Brake Fingerprint')

gs4 = gridspec.GridSpec(2, 2, figure=fig4, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.91, bottom=0.07, left=0.07, right=0.97)

# Scatter — entry speed vs peak brake pressure per zone
ax4a = fig4.add_subplot(gs4[0, 0])
stat_lines4a = []
for drv in data:
    bl        = data[drv]['lap']
    bp        = bl['Brake Press'].fillna(0)
    spd       = bl['Speed']
    threshold = bp.max() * 0.15
    in_ev = False; events = []; pv = 0; ev_spd = 0
    for sv, bpv in zip(spd, bp):
        if bpv > threshold and not in_ev:
            in_ev = True; pv = bpv; ev_spd = sv
        elif bpv > threshold and in_ev:
            if bpv > pv: pv = bpv; ev_spd = sv
        elif bpv <= threshold and in_ev:
            in_ev = False; events.append((ev_spd, pv))

    if events:
        e_spd  = [e[0] for e in events]
        e_vals = [e[1] for e in events]
        ax4a.scatter(e_spd, e_vals, s=80, color=COLORS[drv],
                     alpha=0.85, label=drv, zorder=4,
                     edgecolors='white', linewidths=0.5)
        # annotate hardest braking event
        max_i = e_vals.index(max(e_vals))
        ax4a.annotate(f'{e_vals[max_i]:.1f}b\n@{e_spd[max_i]:.0f}kmh',
                      xy=(e_spd[max_i], e_vals[max_i]),
                      xytext=(e_spd[max_i]-25, e_vals[max_i]+1.5),
                      fontsize=7, color=COLORS[drv],
                      arrowprops=dict(arrowstyle='->', color=COLORS[drv], lw=0.7))
        stat_lines4a += [
            (f'{drv} max press', f'{max(e_vals):.2f} bar',   COLORS[drv]),
            (f'{drv} max entry', f'{max(e_spd):.0f} km/h',   COLORS[drv]),
            (f'{drv} zones',     f'{len(events)}',            COLORS[drv]),
        ]

ax4a.set_xlabel('Corner Entry Speed (km/h)')
ax4a.set_ylabel('Peak Brake Pressure (bar)')
ax4a.legend(fontsize=8, framealpha=0.3)
ax4a.grid(True, alpha=0.3)
ax4a.set_title('Each dot = one braking zone  |  top-right = hardest braking  |  cluster shape = braking style',
               loc='left', fontsize=9)

sp4a = fig4.add_subplot(gs4[0, 1])
stat_panel(sp4a, stat_lines4a, 'Brake Zones')

# Raw brake pressure trace best lap — all 3 overlaid
ax4b = fig4.add_subplot(gs4[1, 0])
stat_lines4b = []
for drv in data:
    bl  = data[drv]['lap']
    bp  = bl['Brake Press'].fillna(0)
    ax4b.plot(bl['Dist'], bp, color=COLORS[drv],
              linewidth=0.9, alpha=0.85, label=drv)
    ax4b.fill_between(bl['Dist'], 0, bp,
                      color=COLORS[drv], alpha=0.10)
    stat_lines4b += [
        (f'{drv} peak',        f'{bp.max():.2f} bar',          COLORS[drv]),
        (f'{drv} mean active', f'{bp[bp>0.1].mean():.2f} bar', COLORS[drv]),
    ]

ax4b.set_xlabel('Distance from lap start (m)')
ax4b.set_ylabel('Brake Pressure (bar)')
ax4b.legend(fontsize=7.5, framealpha=0.3)
ax4b.grid(True, alpha=0.3)
ax4b.set_title('Raw brake pressure trace — spike height = braking severity  |  width = duration',
               loc='left', fontsize=9)
ax4b.set_xlim(0, max(data[d]['lap']['Dist'].iloc[-1] for d in data) + 20)

sp4b = fig4.add_subplot(gs4[1, 1])
stat_panel(sp4b, stat_lines4b, 'Brake Press\nTrace')
fig4.tight_layout(rect=[0, 0, 1, 0.95])

plt.show()