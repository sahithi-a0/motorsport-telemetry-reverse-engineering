# Layer 5 — Is the Car Surviving?

This layer was the most challenging one for me. I had no background 
in engine health monitoring before this. I had to research what each 
channel actually means, what the warning thresholds are, and why they 
matter — before I could even start reading the data properly.

But I'm glad I didn't skip it. Because what came out of this layer 
connected directly back to everything Layer 3 already showed about 
the drivers.

---

## Plot 1 — Thermal Load Progression (Water Temp + Oil Temp)

The first thing I learned doing this layer is that a rising temperature 
line is completely normal — engines get hot. What you're actually 
watching for is a line that keeps climbing late in the race without 
stabilising, or one that crosses a warning threshold and stays there.

**Water temperature**

Starting temperatures are broadly similar across all three. Driver 3 
at 89.8°C, Driver 4 at 89.1°C, Driver 5 at 79.4°C. That 10 degree 
gap for Driver 5 at the start probably just means more time between 
sessions before the race.

What surprised me was the order of peaks. Driver 3 is the last to 
cross 100°C — doesn't get there until 342 seconds in — but ends up 
with the highest sustained temperature at 104.6°C. Driver 4 crosses 
100°C first at 263 seconds but then levels off. Driver 3 never does. 
The line just keeps climbing through the whole race.

From what I understood researching this — that difference between 
stabilising and not stabilising matters a lot. Driver 4's cooling 
system found its balance. Driver 3's never did.

Driver 5 had the lowest peak water temperature of the three and the 
fastest lap times. That combination — least heat, most performance — 
was something I hadn't expected to find.

**Oil temperature**

Oil temperature was the channel I found most interesting to research. 
I learned that oil has lower thermal mass than coolant so it reacts 
faster, and that above certain temperatures the oil starts thinning 
in ways that affect how well it protects the engine bearings. The 
warning threshold I used on this plot is 118°C.

The number that stood out most to me — Driver 5 doesn't cross 110°C 
until 1,633 seconds into the race. Driver 3 crosses it at 543 seconds. 
That's over 1,000 seconds difference between the two drivers in the 
same car on the same circuit. I wasn't expecting that gap to be so large.

Driver 3's oil peaks at 119.8°C — which is 1.8°C above the 118°C 
threshold I found in my research. I'm not in a position to say 
definitively that damage occurred. But it's the number in this entire 
dataset that made me most uncomfortable.

---

## Plot 2 — Oil Pressure vs RPM

I built this plot in two parts — a scatter of pressure against RPM 
from the best lap, and a smoothed pressure trace across the full race. 
I learned that in a healthy engine, oil pressure should rise with RPM 
because the pump is driven off the crankshaft. So the slope of the 
trend line tells you how the system is responding under load.

All three drivers stay above the 2.0 bar warning level during active 
running, which from my research is the number that matters most for 
bearing protection.

What I found more interesting was the full race degradation. Driver 3 
starts at a mean of 4.78 bar and finishes at 2.10 bar — a drop of 
2.68 bar across the race. And when I looked at when the drop 
accelerates, it's around 1,000 seconds — which is almost exactly 
when the oil temperature crosses 110°C in Plot 1.

I'm not experienced enough to say with certainty what causes what here. 
But the timing of those two things lining up felt significant. Hotter 
oil is thinner oil, and thinner oil holds pressure less well. That 
much made sense to me from the research.

Driver 5 drops just 0.16 bar across the entire race. Most stable of 
the three, which lines up with what the temperature data already showed.

---

## Plot 3 — Battery Voltage

This was the channel I understood least going in. I learned that 
voltage matters for data quality — when it drops, sensors can start 
reading incorrectly. So in a way, this plot is as much about trusting 
the other channels as it is about the car's electrical health.

Driver 3 and Driver 5 both hold stable throughout — never near the 
11.5V instability threshold I found in my research.

Driver 4 is different. Late in the race, voltage drops to 10.70V and 
stays below 11.5V for nearly 20 seconds. I went back and checked — 
this happens after Driver 4's best lap, so the lap data I used 
throughout this analysis is still valid. But it raised a flag about 
the car's electrical system.

From what I read, the most likely causes are alternator failure or a 
loose connector. I can't confirm which from the data alone — that 
would need a physical inspection. But I flagged it because it's not 
something I'd want to carry into the next session.

---

## Plot 4 — Brake Pressure vs Entry Speed (Braking Fingerprint)

I came across this type of plot while researching how engineers 
compare braking technique, and I wanted to try building it. The idea 
is to plot peak brake pressure against the speed the car was travelling 
when braking started — one point per braking zone. The shape of the 
cloud tells you something about how each driver approaches corners.

Driver 3's cloud has the highest correlation at 0.919 — pressure 
closely tracks entry speed. Faster in, harder on the brakes. Clean 
and consistent.

Driver 4 has the most zones at 13 and the highest peak pressure at 
36.45 bar. Arrives fast, brakes hard, but breaks some zones into 
multiple applications rather than one clean event.

Driver 5 has the lowest correlation at 0.783. At first I thought 
that meant less consistent braking. But when I looked at which zones 
had high pressure at moderate entry speeds, I realised those were 
the corners where Driver 5 was using the brakes to load the front 
axle and rotate the car — not just to slow down. The lower 
correlation is actually a signature of using braking for more than 
one purpose. I found that the most interesting thing in this plot.

---

## Synthesis — Is the Car Surviving?

**Driver 5's car** is fine. Oil temperature peaks at 113.2°C, well 
below the threshold. Pressure drops just 0.16 bar across the race. 
Voltage stays healthy throughout. This car goes straight back out.

**Driver 4's car** has one thing that needs attention — the voltage 
collapse late in the race. That needs to be investigated before the 
next session. Everything else is within limits.

**Driver 3's car** is the one I'd be most concerned about. Oil 
temperature above the viscosity threshold, steepest pressure drop, 
highest water temperature. None of those alone confirms a problem. 
Together they describe a car that was under more thermal stress than 
the others throughout the race.

And the part that I keep coming back to — the heat isn't from 
pushing hard through corners. It's from wheelspin, over-revving, 
and poor traction at corner exit. The same things the driving data 
already showed in Layer 3.

Fix the technique — and you stop cooking the engine.

The car problem and the driver problem are the same problem.
