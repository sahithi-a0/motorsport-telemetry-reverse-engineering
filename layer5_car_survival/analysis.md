
# Layer 5 — Is the Car Surviving?

## Plot 1 — Thermal Load Progression (Water Temp + Oil Temp)

Both temperature channels are plotted against session time across the full race. The dashed warning lines are the thresholds where temperature stops being something you monitor and becomes something you act on. A steadily climbing line is completely normal — engines get hot. What you're worried about is a line that's still accelerating late in the race, or one that crosses the threshold and doesn't come back.

**Water temperature**

Starting temperatures are broadly similar. Driver 3 at 89.8°C, Driver 4 at 89.1°C, Driver 5 at 79.4°C. That 10 degree gap for Driver 5 at the start likely just means more time between sessions or a longer gap before the formation lap.

Driver 4 crosses 100°C first at 263 seconds in. Driver 5 at 273 seconds. Driver 3 doesn't get there until 342 seconds — last of the three — yet ends up with the highest sustained temperature at 104.6°C. Driver 4 peaks at 103.2°C, Driver 5 at 102.3°C.

The rate of rise matters more than the peak. Driver 3 climbs throughout the race and never really stabilises — heat keeps accumulating right to the end. Driver 4 heats up fast early then levels off, their cooling system found an equilibrium. Driver 3's never did. Extend that session another ten laps and Driver 3's coolant is heading somewhere you really don't want it to go. At that point you're on the radio.

Driver 5 tells the efficiency story plainly — lowest peak water temperature in the field, fastest lap times in the field. Least waste heat per unit of performance. Driver 3 sits at the opposite end. The engine is working hard and the stopwatch isn't reflecting it.

**Oil temperature**

Oil temperature reacts faster than water because it has lower thermal mass. It's also the channel that directly affects whether the bearings are being looked after. The warning threshold on this plot is 118°C — once you're regularly above that, the oil starts thinning in ways that cause damage.

Driver 3 reaches 110°C at 543 seconds. Driver 4 reaches it at 600 seconds — later than Driver 3 despite being a faster driver. Driver 5 doesn't cross 110°C until 1,633 seconds. Over 1,000 seconds later than Driver 3. That single number captures the difference between these two drivers better than almost anything else in the dataset.

Driver 4 rises 41.4°C across the race — the steepest oil temperature climb of anyone here. Driver 5 rises 38.3°C. Driver 3 rises 30.4°C but starts hotter, which is why their peak of 119.8°C is the highest. That's 1.8°C above the viscosity warning threshold. The oil has crossed the line where measurable degradation begins. Combined with the pressure data in Plot 2, Driver 3's car is the one I'd be inspecting first after this race.

---

## Plot 2 — Oil Pressure vs RPM

Two panels. The upper one scatters oil pressure against RPM from the best lap with a fitted trend line. The lower one shows smoothed oil pressure across the full race. Together they answer — what's the system doing under peak load, and is it holding up over distance?

**Best lap scatter**

In a healthy system, oil pressure rises with RPM because the pump is mechanically driven off the crankshaft. The slope of the trend line measures that relationship. Driver 4 shows the steepest slope at 0.532 bar per 1,000 rpm. Driver 3 at 0.410, Driver 5 at 0.383. All three stay comfortably above the 2.0 bar warning threshold during active running, which is the number that matters most.

The scatter cloud shape carries its own information. Driver 3's cloud spreads wider in the lower RPM range — the slow corner zones. On a circuit with 18-metre hairpins generating over 5g laterally, oil surge at low speed is a real concern, and that wider scatter is exactly what it looks like in the data.

**Full session pressure degradation**

Driver 3 starts the race at a mean of 4.78 bar and finishes at 2.10 bar — a drop of 2.68 bar. The decline is gradual early then accelerates around 1,000 seconds in, which is exactly when oil temperature crosses 110°C and viscosity starts going. That's the loop you don't want. Hotter oil, thinner oil, lower pressure, less cooling at the bearing surfaces, even hotter oil. Once it starts, it feeds itself.

Driver 4 drops just 0.08 bar across the full race. Remarkably stable. The caveat is the starting pressure of 2.45 bar is already low — finishing at 2.37 bar leaves almost no margin before the 2.0 bar warning level. It's stable, but there's no buffer left.

Driver 5 drops 0.16 bar. Most stable profile of the three, which lines up with everything the temperature data already said. Cooler oil holds viscosity, stable viscosity maintains pressure, stable pressure protects the engine. It all connects.

---

## Plot 3 — Battery Voltage

Battery voltage isn't a performance channel. It doesn't tell you about lap time. What it tells you is whether the data from every other channel can actually be trusted. When voltage drops, sensors start reading things they shouldn't — and what looks like a technique problem in the data might just be a battery that's struggling.

**Full race trace**

Driver 3 holds between 12.00V and 12.30V throughout. Never near the 11.5V instability threshold. Electrically clean all race. Doesn't explain the brake position anomalies from Layer 3, but at least voltage isn't behind them.

Driver 5's trace is the cleanest — minimum 11.90V, zero time below either warning threshold. Exactly what a healthy system looks like.

Driver 4 is a completely different situation. The session mean of 12.23V looks fine until you see what's hiding underneath it. Late in the race, voltage drops below 11.5V and stays there for nearly 20 seconds. Not a brief spike — a sustained collapse down to 10.70V, which is 0.80V below the threshold where things start going wrong.

The timing matters. Driver 4's best lap is completed well before the voltage drop, so the best lap data is valid. But the steering and brake anomalies from the earlier layers happened before this event too, which means they can't be blamed on it. Driver 4 had pre-existing sensor calibration problems and then the charging system failed on top of them. Two separate problems on the same car.

Most likely cause is alternator failure or a connector working loose under the lateral loads this circuit generates. Five and a half g through an 18-metre hairpin is hard on connections. Driver 4's charging circuit needs a proper inspection before this car goes out again.

**Best lap voltage zoom**

All three drivers show small voltage dips through the best lap at high-draw moments — injector pulses at high RPM, data logger writes, brake light activation. Driver 4 and Driver 5 show drops of around 0.2V, Driver 3 around 0.1V. All three best laps were completed well above 11.5V. The best lap data throughout this entire analysis is electrically sound.

---

## Plot 4 — Brake Pressure vs Entry Speed (Braking Fingerprint)

Each point on this scatter is one braking zone — peak hydraulic pressure plotted against the speed the car was doing when braking started. The shape of the cloud is the braking fingerprint. No two drivers leave the same one.

**Driver 3**

Eight braking zones. Speed-to-pressure correlation of 0.919 — the highest of the three. Brake pressure is almost perfectly proportional to arrival speed. Faster into the corner, harder on the brakes. It's disciplined and repeatable — textbook threshold braking. The hardest event comes at 141 km/h entry and 32.24 bar. Clean technique, very consistent. Mean active pressure of 4.21 bar is the lowest of the three, which tells you the high-pressure events are concentrated at the two main braking zones and the rest of the circuit sees much lighter application.

**Driver 4**

Thirteen braking zones — the most of any driver. Where Driver 3 treats a section as one braking event, Driver 4 splits it into multiple applications. The hardest event is 184 km/h entry at 36.45 bar — the highest entry speed and highest peak pressure in this dataset. Driver 4 is arriving at the main hairpin faster and hitting harder than anyone else. Late, committed, aggressive. Pure point-and-squirt.

The correlation of 0.895 is slightly lower than Driver 3's. The drop comes from the secondary zones where similar entry speeds generate quite different pressure levels. The heavy braking zones are committed and consistent. The secondary zones are where the inconsistency lives. Mean active pressure of 5.83 bar reflects the additional secondary applications spread across the lap.

**Driver 5**

Twelve zones, correlation of 0.783 — lowest of the three. Before that sounds like a problem, it isn't. It's a signature.

Maximum entry speed is 136 km/h and peak pressure is 26.61 bar — both lower than Driver 3 and Driver 4. Yet Driver 5 is the fastest. The explanation is that Driver 5 isn't arriving at corners as fast because the braking is happening earlier and more progressively. The car is decelerating and rotating simultaneously. Less emergency, more precision.

Mean active pressure of 8.71 bar is the highest of the three. Driver 5 is holding pressure all the way through the braking zone rather than spiking and releasing. Sustained threshold, corner to corner.

The lower correlation tells the real story. Some of Driver 5's braking zones show high pressure at moderate entry speeds — disproportionately hard if you think about it purely as deceleration. But it's not purely deceleration. That pressure is being used to load the front axle and rotate the car. Braking as a steering tool, not just a speed-reduction tool. When pressure serves two purposes at different corners, the tidy speed-to-pressure relationship breaks down. The 0.783 correlation is evidence of a more complete technique, not a less disciplined one.

---

## Synthesis — Is the Car Surviving?

**Driver 5's car** is fine. Oil temperature peaks at 113.2°C — safely below the viscosity threshold. Oil pressure drops just 0.16 bar across the full race. Battery voltage never goes below 11.90V. The engine is being loaded hard — 38°C oil temperature rise confirms that — but everything stays within safe limits. This car goes straight back out.

**Driver 4's car** has one confirmed problem that needs fixing before the next session — the voltage collapse to 10.70V late in the race. Nearly 20 seconds below the instability threshold is not something you carry forward. The thermal load is aggressive but within limits. The braking loads are high but brakes are consumables. The electrical fault is the priority.

**Driver 3's car** is the one I'd be most concerned about walking away from this race. Highest water temperature at 104.6°C, oil temperature at 119.8°C which is already above the 118°C viscosity warning threshold, and the steepest oil pressure drop in the dataset at 2.68 bar. None of those individually confirms a failure. Together they describe a car that was thermally saturated through most of this race and never found its equilibrium.

And the uncomfortable part is that the heat isn't coming from fast cornering — it's coming from wheelspin, over-revving, and poor traction at corner exit. The same issues the driving data already flagged in Layer 3. Fix the technique and you don't just find lap time — you also stop cooking the engine.

The car problem and the driver problem are the same problem.
