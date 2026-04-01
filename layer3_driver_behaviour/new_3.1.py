import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── CONFIG ──────────────────────────────────────────────────────────────────
CSV_PATH       = r'C:\Users\sahit\OneDrive\Documents\assignments_ARCVD\Driver 4  Qualifying 1.csv'
BEST_LAP_START = 607.53
BEST_LAP_END   = 678.718
DT             = 0.05

# ── LOAD & CLEAN ────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH, skiprows=6, header=0, low_memory=False)
df = df[df['Time'] != 's'].dropna(subset=['Time']).reset_index(drop=True)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

bl = df[(df['Time'] >= BEST_LAP_START) & (df['Time'] <= BEST_LAP_END)].copy()
bl['Lap_Time'] = bl['Time'] - BEST_LAP_START
bl = bl.reset_index(drop=True)

# ── FIX DISTANCE ────────────────────────────────────────────────────────────
dist_offset = bl['Distance on GPS Speed'].iloc[0]
bl['Dist']  = bl['Distance on GPS Speed'] - dist_offset
dist        = bl['Dist']
lap_length  = dist.iloc[-1]
lap_time    = len(bl) * DT

# ── CHANNELS ────────────────────────────────────────────────────────────────
thr   = bl['Throttle Pos']
brk   = bl['Brake Pos']
bp    = bl['Brake Press'].fillna(0)
steer = bl['Steering Pos']
spd   = bl['Speed']
gspd  = bl['GPS Speed']
lam   = bl['Lambda']
gx    = bl['Lateral Acc']
gy    = bl['Inline Acc']

# ── PRECOMPUTE ALL STATS ────────────────────────────────────────────────────
full_thr_mask  = thr >= 99
zero_thr_mask  = thr <= 1
on_brake_mask  = brk > 5
trail_mask     = (thr > 5) & (brk > 5)
gate_mask      = thr > 80

t_full   = full_thr_mask.sum() * DT
t_zero   = zero_thr_mask.sum() * DT
t_brake  = on_brake_mask.sum() * DT
t_trail  = trail_mask.sum() * DT
t_gate   = gate_mask.sum() * DT

d_thr    = np.gradient(thr.values, DT)
d_steer  = np.gradient(steer.values, DT)
combined = np.sqrt(gx**2 + gy**2)
gs_safe  = gspd.replace(0, np.nan)
slip     = (spd - gs_safe) / gs_safe * 100
lam_g    = lam[gate_mask]

# braking events
threshold = bp.max() * 0.15
in_ev = False; events = []; pv = 0; pd_ = 0
for dv, bpv in zip(dist, bp):
    if bpv > threshold and not in_ev:
        in_ev = True; pv = bpv; pd_ = dv
    elif bpv > threshold and in_ev:
        if bpv > pv: pv = bpv; pd_ = dv
    elif bpv <= threshold and in_ev:
        in_ev = False; events.append((pd_, pv))

# trail braking zone count
zones = []
in_z = False
for d, tb in zip(dist, trail_mask):
    if tb and not in_z: in_z = True; zs = d
    elif not tb and in_z: in_z = False; zones.append(zs)

# ── STYLE ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f0f0f', 'axes.facecolor':  '#1a1a1a',
    'axes.edgecolor':   '#333333', 'axes.labelcolor': '#cccccc',
    'axes.titlecolor':  '#ffffff', 'xtick.color':     '#888888',
    'ytick.color':      '#888888', 'text.color':      '#cccccc',
    'grid.color':       '#2a2a2a', 'grid.linewidth':  0.5,
    'font.family':      'monospace','axes.titlesize':  10,
    'axes.labelsize':   9,          'xtick.labelsize': 8,
    'ytick.labelsize':  8,
})

STAT_BOX = dict(boxstyle='round', facecolor='#111111',
                edgecolor='#444444', alpha=0.9)

def stat_panel(ax, lines, title=''):
    """Draw a clean stats panel on a blank axis."""
    ax.set_facecolor('#111111')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
    if title:
        ax.text(0.5, 0.97, title, transform=ax.transAxes,
                fontsize=8, color='#EF9F27', fontweight='bold',
                ha='center', va='top')
    y = 0.88
    for label, value, color in lines:
        ax.text(0.05, y, label, transform=ax.transAxes,
                fontsize=7.5, color='#888888', va='top')
        ax.text(0.95, y, value, transform=ax.transAxes,
                fontsize=7.5, color=color, va='top', ha='right',
                fontweight='bold')
        y -= 0.11

def make_fig(title):
    fig = plt.figure(figsize=(17, 6))
    fig.suptitle(f'Driver 3 · Qualifying · Best Lap L8 · {lap_length:.0f}m · {lap_time:.1f}s\n{title}',
                 color='white', fontsize=12)
    return fig

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 1 — DRIVER INPUTS TRACE
# ═══════════════════════════════════════════════════════════════════════════
fig1 = plt.figure(figsize=(17, 12))
fig1.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 1: Driver Inputs Trace',
              color='white', fontsize=12)
fig1.canvas.manager.set_window_title('Plot 1 — Driver Inputs')

gs1 = gridspec.GridSpec(4, 2, figure=fig1, width_ratios=[5, 1],
                         hspace=0.35, wspace=0.05,
                         top=0.92, bottom=0.06, left=0.06, right=0.97)

# Speed
ax = fig1.add_subplot(gs1[0, 0])
ax.plot(dist, spd, color='#378ADD', linewidth=0.9)
ax.fill_between(dist, 0, spd, color='#378ADD', alpha=0.15)
mi = spd.idxmax()
ax.annotate(f'{spd.max():.0f}', xy=(dist.iloc[mi], spd.max()),
            xytext=(dist.iloc[mi]+60, spd.max()-18),
            fontsize=7, color='#EF9F27',
            arrowprops=dict(arrowstyle='->', color='#EF9F27', lw=0.7))
ax.set_ylabel('Speed (km/h)'); ax.set_ylim(0, 215)
ax.grid(True, axis='y', alpha=0.3)
ax.set_title('Speed', loc='left', fontsize=9)

sx = fig1.add_subplot(gs1[0, 1])
stat_panel(sx, [
    ('Top speed',  f'{spd.max():.0f} km/h',   '#EF9F27'),
    ('Min speed',  f'{spd[spd>10].min():.0f} km/h', '#378ADD'),
    ('Avg speed',  f'{spd.mean():.0f} km/h',  '#cccccc'),
], 'Speed')

# Throttle
ax = fig1.add_subplot(gs1[1, 0], sharex=fig1.axes[0])
ax.plot(dist, thr, color='#1D9E75', linewidth=0.9)
ax.fill_between(dist, 0, thr, where=full_thr_mask,
                color='#1D9E75', alpha=0.55, label='≥99%')
ax.fill_between(dist, 0, 100, where=zero_thr_mask,
                color='#E24B4A', alpha=0.20, label='≤1%')
ax.set_ylabel('Throttle (%)'); ax.set_ylim(-5, 115)
ax.grid(True, axis='y', alpha=0.3)
ax.legend(fontsize=7, framealpha=0.3, loc='upper right')
ax.set_title('Throttle  —  green fill = full power  |  red fill = zero throttle', loc='left', fontsize=9)

tx = fig1.add_subplot(gs1[1, 1])
stat_panel(tx, [
    ('Full (≥99%)', f'{t_full:.1f}s  {t_full/lap_time*100:.0f}%', '#1D9E75'),
    ('Zero (≤1%)',  f'{t_zero:.1f}s  {t_zero/lap_time*100:.0f}%', '#E24B4A'),
    ('Max',         f'{thr.max():.0f}%',                           '#cccccc'),
], 'Throttle')

# Brake
ax = fig1.add_subplot(gs1[2, 0], sharex=fig1.axes[0])
ax.plot(dist, brk, color='#E24B4A', linewidth=0.9)
ax.fill_between(dist, 0, brk, where=on_brake_mask,
                color='#E24B4A', alpha=0.50)
ax.set_ylabel('Brake (%)'); ax.set_ylim(-5, 115)
ax.grid(True, axis='y', alpha=0.3)
ax.set_title('Brake  —  red fill = brake active (>5%)', loc='left', fontsize=9)

bx = fig1.add_subplot(gs1[2, 1])
stat_panel(bx, [
    ('On brake',   f'{t_brake:.1f}s  {t_brake/lap_time*100:.0f}%', '#E24B4A'),
    ('Max pos',    f'{brk.max():.1f}%',                             '#EF9F27'),
    ('Mean active',f'{brk[brk>5].mean():.1f}%',                    '#cccccc'),
], 'Brake')

# Steering
ax = fig1.add_subplot(gs1[3, 0], sharex=fig1.axes[0])
ax.plot(dist, steer, color='#EF9F27', linewidth=0.9)
ax.fill_between(dist, 0, steer, where=steer > 0,
                color='#EF9F27', alpha=0.35, label='Right')
ax.fill_between(dist, 0, steer, where=steer < 0,
                color='#378ADD', alpha=0.35, label='Left')
ax.axhline(0, color='#555555', linewidth=0.6)
ax.set_ylabel('Steering (deg)'); ax.grid(True, axis='y', alpha=0.3)
ax.legend(fontsize=7, framealpha=0.3, loc='upper right')
ax.set_title('Steering  —  orange=right  blue=left', loc='left', fontsize=9)
ax.set_xlabel('Distance from lap start (m)')
ax.set_xlim(0, lap_length + 20)
ax.set_xticks(np.arange(0, lap_length + 1, 200))

stx = fig1.add_subplot(gs1[3, 1])
stat_panel(stx, [
    ('Max right',  f'{steer.max():.0f} deg', '#EF9F27'),
    ('Max left',   f'{steer.min():.0f} deg', '#378ADD'),
    ('Mean |steer|',f'{steer.abs().mean():.1f} deg','#cccccc'),
], 'Steering')

fig1.tight_layout(rect=[0, 0, 1, 0.95])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 2 — TRAIL BRAKING GATE
# ═══════════════════════════════════════════════════════════════════════════
fig2 = plt.figure(figsize=(17, 8))
fig2.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 2: Trail Braking Gate',
              color='white', fontsize=12)
fig2.canvas.manager.set_window_title('Plot 2 — Trail Braking')

gs2 = gridspec.GridSpec(2, 2, figure=fig2, width_ratios=[5, 1],
                         hspace=0.3, wspace=0.05,
                         top=0.90, bottom=0.08, left=0.06, right=0.97)

ax2a = fig2.add_subplot(gs2[0, 0])
ax2a.plot(dist, thr, color='#1D9E75', linewidth=0.9, label='Throttle %')
ax2a.plot(dist, brk, color='#E24B4A', linewidth=0.9, label='Brake %')
ax2a.fill_between(dist, 0, 100, where=trail_mask,
                  color='#7F77DD', alpha=0.35, label='Both active')
ax2a.set_ylabel('Position (%)'); ax2a.set_ylim(-5, 115)
ax2a.legend(fontsize=7.5, framealpha=0.3, loc='upper right')
ax2a.grid(True, axis='y', alpha=0.3)
ax2a.set_title('Throttle & Brake — purple = both >5% simultaneously (trail braking)', loc='left', fontsize=9)

s2a = fig2.add_subplot(gs2[0, 1])
stat_panel(s2a, [
    ('Trail time',  f'{t_trail:.1f}s',                     '#7F77DD'),
    ('% of lap',    f'{t_trail/lap_time*100:.0f}%',        '#7F77DD'),
    ('Zones',       f'{len(zones)}',                        '#cccccc'),
], 'Trail Brake')

ax2b = fig2.add_subplot(gs2[1, 0], sharex=ax2a)
gate_sig = trail_mask.astype(int)
ax2b.fill_between(dist, 0, gate_sig, color='#7F77DD',
                  alpha=0.75, step='pre', label='Gate ON')
ax2b.set_ylabel('Gate\n(1=active)'); ax2b.set_ylim(-0.1, 1.3)
ax2b.set_yticks([0, 1])
ax2b.grid(True, axis='y', alpha=0.3)
ax2b.set_title('Binary gate — every purple bar = trail braking happening at that distance', loc='left', fontsize=9)
ax2b.set_xlabel('Distance from lap start (m)')
ax2b.set_xlim(0, lap_length + 20)
ax2b.set_xticks(np.arange(0, lap_length + 1, 200))

s2b = fig2.add_subplot(gs2[1, 1])
stat_panel(s2b, [
    ('Thr threshold', '>5%',  '#1D9E75'),
    ('Brk threshold', '>5%',  '#E24B4A'),
    ('Sample rate',  '20 Hz', '#cccccc'),
], 'Gate Logic')

fig2.tight_layout(rect=[0, 0, 1, 0.94])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 3 — THROTTLE DERIVATIVE
# ═══════════════════════════════════════════════════════════════════════════
fig3 = plt.figure(figsize=(17, 8))
fig3.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 3: Throttle Derivative',
              color='white', fontsize=12)
fig3.canvas.manager.set_window_title('Plot 3 — Throttle Derivative')

gs3 = gridspec.GridSpec(2, 2, figure=fig3, width_ratios=[5, 1],
                         hspace=0.3, wspace=0.05,
                         top=0.90, bottom=0.08, left=0.06, right=0.97)

ax3a = fig3.add_subplot(gs3[0, 0])
ax3a.plot(dist, thr, color='#1D9E75', linewidth=0.9)
ax3a.fill_between(dist, 0, thr, color='#1D9E75', alpha=0.15)
ax3a.set_ylabel('Throttle (%)'); ax3a.set_ylim(-5, 115)
ax3a.grid(True, axis='y', alpha=0.3)
ax3a.set_title('Raw throttle position', loc='left', fontsize=9)

s3a = fig3.add_subplot(gs3[0, 1])
stat_panel(s3a, [
    ('Max pos',  f'{thr.max():.0f}%',         '#1D9E75'),
    ('Full thr', f'{t_full:.1f}s',             '#1D9E75'),
    ('Zero thr', f'{t_zero:.1f}s',             '#E24B4A'),
], 'Throttle')

ax3b = fig3.add_subplot(gs3[1, 0], sharex=ax3a)
ax3b.fill_between(dist, 0, d_thr, where=d_thr >= 0,
                  color='#1D9E75', alpha=0.70, label='Opening (+)')
ax3b.fill_between(dist, 0, d_thr, where=d_thr < 0,
                  color='#E24B4A', alpha=0.70, label='Closing (−)')
ax3b.axhline(0, color='#555555', linewidth=0.7)
ax3b.set_ylabel('dThrottle/dt (%/s)')
ax3b.grid(True, axis='y', alpha=0.3)
ax3b.legend(fontsize=7.5, framealpha=0.3, loc='upper right')
ax3b.set_title('Rate of change — tall green = snap open  |  tall red = sudden lift', loc='left', fontsize=9)
ax3b.set_xlabel('Distance from lap start (m)')
ax3b.set_xlim(0, lap_length + 20)
ax3b.set_xticks(np.arange(0, lap_length + 1, 200))

s3b = fig3.add_subplot(gs3[1, 1])
stat_panel(s3b, [
    ('Max open',   f'{np.max(d_thr):.0f} %/s',              '#1D9E75'),
    ('Max close',  f'{np.min(d_thr):.0f} %/s',              '#E24B4A'),
    ('Mean open',  f'{np.mean(d_thr[d_thr>0]):.0f} %/s',   '#cccccc'),
    ('Mean close', f'{np.mean(d_thr[d_thr<0]):.0f} %/s',   '#cccccc'),
], 'dThrottle/dt')

fig3.tight_layout(rect=[0, 0, 1, 0.94])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 4 — GG DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════
fig4 = plt.figure(figsize=(12, 9))
fig4.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 4: GG Diagram',
              color='white', fontsize=12)
fig4.canvas.manager.set_window_title('Plot 4 — GG Diagram')

gs4 = gridspec.GridSpec(1, 2, figure=fig4, width_ratios=[3, 1],
                         wspace=0.05, top=0.90, bottom=0.08,
                         left=0.07, right=0.97)

ax4 = fig4.add_subplot(gs4[0, 0])
sc = ax4.scatter(gx, gy, c=spd, cmap='RdYlGn_r', s=5, alpha=0.7, zorder=3)
cbar = plt.colorbar(sc, ax=ax4, pad=0.02, fraction=0.03)
cbar.set_label('Speed (km/h)', color='#cccccc', fontsize=8)
cbar.ax.yaxis.set_tick_params(color='#cccccc', labelsize=7)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#cccccc')

g_env = np.percentile(np.sqrt(gx**2 + gy**2), 98)
theta = np.linspace(0, 2*np.pi, 300)
ax4.plot(g_env*np.cos(theta), g_env*np.sin(theta),
         color='#7F77DD', linewidth=1.2, linestyle='--',
         alpha=0.7, label=f'Grip envelope {g_env:.2f}g')
ax4.axhline(0, color='#444444', linewidth=0.7)
ax4.axvline(0, color='#444444', linewidth=0.7)
ax4.text( g_env*0.55,  g_env*0.65, 'Accel\n+Right', fontsize=8, color='#666666', ha='center')
ax4.text(-g_env*0.55,  g_env*0.65, 'Accel\n+Left',  fontsize=8, color='#666666', ha='center')
ax4.text( g_env*0.55, -g_env*0.65, 'Brake\n+Right', fontsize=8, color='#666666', ha='center')
ax4.text(-g_env*0.55, -g_env*0.65, 'Brake\n+Left',  fontsize=8, color='#666666', ha='center')
ax4.set_xlabel('Lateral G  ← Left | Right →')
ax4.set_ylabel('Inline G   ↓ Brake | Accel ↑')
ax4.set_aspect('equal')
ax4.legend(fontsize=8, framealpha=0.3)
ax4.grid(True, alpha=0.25)
ax4.set_title('Colour = speed  |  wider cloud = more grip used', loc='left', fontsize=9)

s4 = fig4.add_subplot(gs4[0, 1])
stat_panel(s4, [
    ('Max lateral G', f'{gx.abs().max():.2f}g',       '#EF9F27'),
    ('Max braking G', f'{gy.min():.2f}g',              '#E24B4A'),
    ('Max accel G',   f'{gy.max():.2f}g',              '#1D9E75'),
    ('Grip envelope', f'{g_env:.2f}g',                 '#7F77DD'),
    ('Mean combined', f'{combined.mean():.2f}g',       '#cccccc'),
], 'GG Stats')

fig4.tight_layout(rect=[0, 0, 1, 0.94])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 5 — STEERING DERIVATIVE
# ═══════════════════════════════════════════════════════════════════════════
fig5 = plt.figure(figsize=(17, 8))
fig5.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 5: Steering Derivative',
              color='white', fontsize=12)
fig5.canvas.manager.set_window_title('Plot 5 — Steering Derivative')

gs5 = gridspec.GridSpec(2, 2, figure=fig5, width_ratios=[5, 1],
                         hspace=0.3, wspace=0.05,
                         top=0.90, bottom=0.08, left=0.06, right=0.97)

ax5a = fig5.add_subplot(gs5[0, 0])
ax5a.plot(dist, steer, color='#EF9F27', linewidth=0.9)
ax5a.fill_between(dist, 0, steer, where=steer > 0,
                  color='#EF9F27', alpha=0.35, label='Right')
ax5a.fill_between(dist, 0, steer, where=steer < 0,
                  color='#378ADD', alpha=0.35, label='Left')
ax5a.axhline(0, color='#555555', linewidth=0.6)
ax5a.set_ylabel('Steering (deg)')
ax5a.legend(fontsize=7.5, framealpha=0.3, loc='upper right')
ax5a.grid(True, axis='y', alpha=0.3)
ax5a.set_title('Raw steering angle', loc='left', fontsize=9)

s5a = fig5.add_subplot(gs5[0, 1])
stat_panel(s5a, [
    ('Max right',  f'{steer.max():.0f} deg', '#EF9F27'),
    ('Max left',   f'{steer.min():.0f} deg', '#378ADD'),
    ('Mean |ang|', f'{steer.abs().mean():.1f} deg', '#cccccc'),
], 'Steering')

ax5b = fig5.add_subplot(gs5[1, 0], sharex=ax5a)
ax5b.fill_between(dist, 0, d_steer, where=d_steer >= 0,
                  color='#EF9F27', alpha=0.70, label='Right / unwind')
ax5b.fill_between(dist, 0, d_steer, where=d_steer < 0,
                  color='#378ADD', alpha=0.70, label='Left / unwind')
ax5b.axhline(0, color='#555555', linewidth=0.7)
ax5b.set_ylabel('dSteering/dt (deg/s)')
ax5b.legend(fontsize=7.5, framealpha=0.3, loc='upper right')
ax5b.grid(True, axis='y', alpha=0.3)
ax5b.set_title('Steering rate — tall spike = aggressive input  |  flat = smooth sustained turn', loc='left', fontsize=9)
ax5b.set_xlabel('Distance from lap start (m)')
ax5b.set_xlim(0, lap_length + 20)
ax5b.set_xticks(np.arange(0, lap_length + 1, 200))

s5b = fig5.add_subplot(gs5[1, 1])
stat_panel(s5b, [
    ('Max rate R',   f'{np.max(d_steer):.0f} deg/s',           '#EF9F27'),
    ('Max rate L',   f'{np.min(d_steer):.0f} deg/s',           '#378ADD'),
    ('Mean |rate|',  f'{np.mean(np.abs(d_steer)):.0f} deg/s',  '#cccccc'),
    ('>200 deg/s',   f'{(np.abs(d_steer)>200).sum()*DT:.1f}s', '#E24B4A'),
], 'dSteering/dt')

fig5.tight_layout(rect=[0, 0, 1, 0.94])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 6 — BRAKE PRESSURE DELTA
# ═══════════════════════════════════════════════════════════════════════════
fig6 = plt.figure(figsize=(17, 8))
fig6.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 6: Brake Pressure Delta',
              color='white', fontsize=12)
fig6.canvas.manager.set_window_title('Plot 6 — Brake Pressure')

gs6 = gridspec.GridSpec(2, 2, figure=fig6, width_ratios=[5, 1],
                         hspace=0.3, wspace=0.05,
                         top=0.90, bottom=0.08, left=0.06, right=0.97)

ax6a = fig6.add_subplot(gs6[0, 0])
ax6a.plot(dist, bp, color='#E24B4A', linewidth=0.9)
ax6a.fill_between(dist, 0, bp, color='#E24B4A', alpha=0.25)
ax6a.set_ylabel('Brake Pressure (bar)')
ax6a.grid(True, axis='y', alpha=0.3)
ax6a.set_title('Raw brake pressure — spike height = how hard brakes are hit', loc='left', fontsize=9)

s6a = fig6.add_subplot(gs6[0, 1])
stat_panel(s6a, [
    ('Max pressure', f'{bp.max():.2f} bar',           '#E24B4A'),
    ('Mean active',  f'{bp[bp>0.1].mean():.2f} bar',  '#EF9F27'),
    ('Zones',        f'{len(events)}',                 '#cccccc'),
], 'Brake Press')

ax6b = fig6.add_subplot(gs6[1, 0], sharex=ax6a)
if events:
    e_dists = [e[0] for e in events]
    e_vals  = [e[1] for e in events]
    max_v   = max(e_vals)
    colors  = ['#E24B4A' if v == max_v else '#EF9F27' for v in e_vals]
    bars = ax6b.bar(e_dists, e_vals, width=30, color=colors, alpha=0.85, zorder=3)
    # annotate each bar
    for ed, ev, ec in zip(e_dists, e_vals, colors):
        ax6b.text(ed, ev + 0.5, f'{ev:.1f}', ha='center',
                  fontsize=7, color=ec)
    # annotate hardest
    max_i = e_vals.index(max_v)
    ax6b.annotate(f'Hardest\n{max_v:.1f} bar',
                  xy=(e_dists[max_i], max_v),
                  xytext=(e_dists[max_i]+100, max_v*0.85),
                  fontsize=7.5, color='#E24B4A',
                  arrowprops=dict(arrowstyle='->', color='#E24B4A', lw=0.8))
ax6b.set_ylabel('Peak Pressure (bar)')
ax6b.grid(True, axis='y', alpha=0.3)
ax6b.set_title(f'Peak brake pressure per zone  |  red = hardest  |  {len(events)} zones total', loc='left', fontsize=9)
ax6b.set_xlabel('Distance from lap start (m)')
ax6b.set_xlim(0, lap_length + 20)
ax6b.set_xticks(np.arange(0, lap_length + 1, 200))

s6b = fig6.add_subplot(gs6[1, 1])
if events:
    sorted_ev = sorted(events, key=lambda x: x[1], reverse=True)
    lines6b = [(f'Z{i+1} @{int(e[0])}m', f'{e[1]:.1f} bar',
                '#E24B4A' if i==0 else '#EF9F27')
               for i, e in enumerate(sorted_ev[:5])]
    stat_panel(s6b, lines6b, 'Top Zones')

fig6.tight_layout(rect=[0, 0, 1, 0.94])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 7 — LAMBDA GATED
# ═══════════════════════════════════════════════════════════════════════════
# fig7 = plt.figure(figsize=(17, 8))
# fig7.suptitle('Driver 3 · Qualifying · Best Lap L8  —  Plot 7: Lambda Gated (Throttle >80%)',
#               color='white', fontsize=12)
# fig7.canvas.manager.set_window_title('Plot 7 — Lambda Gated')

# gs7 = gridspec.GridSpec(2, 2, figure=fig7, width_ratios=[5, 1],
#                          hspace=0.3, wspace=0.05,
#                          top=0.90, bottom=0.08, left=0.06, right=0.97)

# ax7a = fig7.add_subplot(gs7[0, 0])
# ax7a.plot(dist, thr, color='#1D9E75', linewidth=0.8, alpha=0.7)
# ax7a.fill_between(dist, 0, 100, where=gate_mask,
#                   color='#1D9E75', alpha=0.20, label=f'Gate active >80%')
# ax7a.set_ylabel('Throttle (%)'); ax7a.set_ylim(-5, 115)
# ax7a.legend(fontsize=7.5, framealpha=0.3, loc='upper right')
# ax7a.grid(True, axis='y', alpha=0.3)
# ax7a.set_title('Throttle — green zones = gate open — only these zones shown in lambda panel', loc='left', fontsize=9)

# s7a = fig7.add_subplot(gs7[0, 1])
# stat_panel(s7a, [
#     ('Gate time', f'{t_gate:.1f}s',              '#1D9E75'),
#     ('% of lap',  f'{t_gate/lap_time*100:.0f}%', '#1D9E75'),
#     ('Threshold', '>80%',                         '#cccccc'),
# ], 'Gate')

# lam_gated = lam.where(gate_mask, other=np.nan)

# ax7b = fig7.add_subplot(gs7[1, 0], sharex=ax7a)
# ax7b.axhline(1.0, color='#ffffff', linewidth=0.8,
#              linestyle='--', alpha=0.4, label='λ=1.0 stoich')
# ax7b.axhspan(0.80, 1.0,  color='#E24B4A', alpha=0.10, label='Rich <1.0')
# ax7b.axhspan(1.0,  1.10, color='#EF9F27', alpha=0.10, label='Lean >1.0')
# ax7b.plot(dist, lam_gated, color='#FAC775', linewidth=1.3, alpha=0.9)
# ax7b.fill_between(dist, 1.0, lam_gated,
#                   where=lam_gated < 1.0, color='#E24B4A', alpha=0.25)
# ax7b.fill_between(dist, 1.0, lam_gated,
#                   where=lam_gated > 1.0, color='#EF9F27', alpha=0.25)
# ax7b.set_ylabel('Lambda'); ax7b.set_ylim(0.75, 1.15)
# ax7b.legend(fontsize=7.5, framealpha=0.3, ncol=3, loc='upper right')
# ax7b.grid(True, axis='y', alpha=0.3)
# ax7b.set_title('Lambda at full throttle only  |  below 1.0=rich(safe)  above 1.0=lean(risk)', loc='left', fontsize=9)
# ax7b.set_xlabel('Distance from lap start (m)')
# ax7b.set_xlim(0, lap_length + 20)
# ax7b.set_xticks(np.arange(0, lap_length + 1, 200))

# s7b = fig7.add_subplot(gs7[1, 1])
# lam_note = 'No data' if lam_g.isna().all() or lam_g.max() == 0 else f'{lam_g.mean():.3f}'
# stat_panel(s7b, [
#     ('Mean λ',   lam_note,                              '#FAC775'),
#     ('Min λ',    f'{lam_g.min():.3f}' if lam_g.max()>0 else 'N/A', '#E24B4A'),
#     ('Max λ',    f'{lam_g.max():.3f}' if lam_g.max()>0 else 'N/A', '#EF9F27'),
#     ('Status',   'Sensor off' if lam_g.max()==0 else 'Active',       '#888888'),
# ], 'Lambda')

# fig7.tight_layout(rect=[0, 0, 1, 0.94])

# ═══════════════════════════════════════════════════════════════════════════
# PLOT 7 — WHEEL SLIP RATIO
# ═══════════════════════════════════════════════════════════════════════════
fig8 = plt.figure(figsize=(17, 8))
fig8.suptitle('Driver 4 · Qualifying · Best Lap L8  —  Plot 7: Wheel Slip Ratio',
              color='white', fontsize=12)
fig8.canvas.manager.set_window_title('Plot 8 — Wheel Slip')

gs8 = gridspec.GridSpec(2, 2, figure=fig8, width_ratios=[5, 1],
                         hspace=0.3, wspace=0.05,
                         top=0.90, bottom=0.08, left=0.06, right=0.97)

ax8a = fig8.add_subplot(gs8[0, 0])
ax8a.plot(dist, spd,  color='#378ADD', linewidth=0.9,
          alpha=0.9, label='Vehicle Speed')
ax8a.plot(dist, gspd, color='#E24B4A', linewidth=0.8,
          alpha=0.6, label='GPS Speed')
ax8a.set_ylabel('Speed (km/h)')
ax8a.legend(fontsize=7.5, framealpha=0.3, loc='upper right')
ax8a.grid(True, axis='y', alpha=0.3)
ax8a.set_title('Vehicle vs GPS speed — gap between lines = slip', loc='left', fontsize=9)

s8a = fig8.add_subplot(gs8[0, 1])
stat_panel(s8a, [
    ('Max veh spd', f'{spd.max():.0f} km/h',  '#378ADD'),
    ('Max GPS spd', f'{gspd.max():.0f} km/h', '#E24B4A'),
    ('Max diff',    f'{(spd-gspd).max():.1f} km/h', '#EF9F27'),
], 'Speeds')

ax8b = fig8.add_subplot(gs8[1, 0], sharex=ax8a)
ax8b.fill_between(dist, 0, slip,
                  where=slip >= 0, color='#EF9F27',
                  alpha=0.75, label='Wheelspin (+)')
ax8b.fill_between(dist, 0, slip,
                  where=slip < 0,  color='#378ADD',
                  alpha=0.75, label='Lockup (−)')
ax8b.axhline(0, color='#555555', linewidth=0.7)
ax8b.axhline(3,  color='#EF9F27', linewidth=0.6,
             linestyle=':', alpha=0.5, label='+3% threshold')
ax8b.axhline(-3, color='#378ADD', linewidth=0.6,
             linestyle=':', alpha=0.5, label='-3% threshold')
ax8b.set_ylabel('Slip Ratio (%)')
ax8b.legend(fontsize=7.5, framealpha=0.3, loc='upper right', ncol=2)
ax8b.grid(True, axis='y', alpha=0.3)
ax8b.set_title('Orange=wheelspin  Blue=lockup  |  dotted lines=±3% threshold', loc='left', fontsize=9)
ax8b.set_xlabel('Distance from lap start (m)')
ax8b.set_xlim(0, lap_length + 20)
ax8b.set_xticks(np.arange(0, lap_length + 1, 200))

s8b = fig8.add_subplot(gs8[1, 1])
stat_panel(s8b, [
    ('Max spin',    f'{slip.max():.2f}%',              '#EF9F27'),
    ('Max lockup',  f'{slip.min():.2f}%',              '#378ADD'),
    ('Spin >3%',    f'{(slip>3).sum()*DT:.1f}s',       '#EF9F27'),
    ('Lock <-3%',   f'{(slip<-3).sum()*DT:.1f}s',      '#378ADD'),
    ('Mean |slip|', f'{slip.abs().mean():.2f}%',        '#cccccc'),
], 'Slip Stats')

fig8.tight_layout(rect=[0, 0, 1, 0.94])

# ── SHOW ALL ────────────────────────────────────────────────────────────────
plt.show()