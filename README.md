# motorsport-telemetry-reverse-engineering

## What is this project?
I had one thing — telemetry data from 3 drivers.
No car name. No track name. Nothing else.

And I wanted to see how much I could figure out just from that data.

Which car is this? Which track? How is each driver actually driving it?
Who is the fastest and why? Is the engine surviving the race?

All of that — from just the numbers.

---

##Why I built this

This project is me taking everything I learned from the IMA Applied Race
Car Vehicle Dynamics course — combined with my own research and extra
reading — and putting it all into one place.

I wanted to go through a real dataset the way an engineer would.
Not just run plots and move on — but actually ask questions, find answers,
and build understanding layer by layer.

Honestly, I loved it. The idea that a dataset can tell you everything —
the machine, the place, the people, even whether the car is quietly
breaking — that's what got me hooked.

---

## The 5 Layers

The analysis is structured in 5 layers — each one asking a different
question about the same data.

First I identified the car. Then I built the track from GPS alone.
Then I looked at how each driver was actually operating the machine.
Then I compared all three drivers head to head. And finally I checked
whether the car was surviving the whole thing.

Each layer builds on the one before it. You can't understand the driver
without first understanding the car and the track. You can't compare
drivers fairly without understanding each one individually first.

That structure wasn't given to me — it's just how the questions
naturally unfolded.

---

### Layer 1 — What is this machine?
`Speed · RPM · Gear · Speed vs RPM coloured by gear`

Before anything else I wanted to know — what kind of car am I even
looking at?

193 km/h top speed. 5-speed gearbox. Free-revving naturally aspirated
engine living near its rev ceiling for most of the lap. Average GPS to
vehicle speed delta of just 1.5 km/h — decent mechanical grip for its
power output.

From the data alone — a lightweight, Formula 4 class single seater.
A car where the driver makes the difference, not the horsepower.

---

### Layer 2 — Where did it go?
`GPS · Track Map · Elevation Profile · Corner Radius · Heading`

Next question — where is this car going?

I built the full circuit layout from GPS channels alone. No track map
referenced. What came out was a low-speed, technical circuit with a short
main straight and at least six proper braking corners. The car spends more
than half its best lap in second gear.

Turned out to be consistent with Kari Motor Speedway.

---

### Layer 3 — How is the human driving it?
`Throttle · Brake · Steering · Trail Braking · CG Diagram · Wheel Spin`

With the car and track understood, I looked at the driver.

Not just what inputs they made — but how smooth they were, where they
trailed the brake, how aggressively they steered, where the car was
working hardest on the tyres. The GG diagram and throttle derivative
together tell a story that lap time alone never could.

---

### Layer 4 — Comparing all 3 drivers
`Lap Delta · Speed Trace · Throttle & Brake Overlay · GG Diagram · Trail Braking`

This is where it got really interesting.

Driver 5 is the fastest in both qualifying and the race. By nearly
3 seconds in quali. But they have the lowest full throttle time of all
three drivers.

Driver 5 — 2.1 seconds at full throttle. Just 3% of a 68.5 second lap.
Driver 3 — 27.1 seconds (38%).
Driver 4 — 28.8 seconds (41%).

That completely broke my initial thinking. I assumed more throttle meant
more speed. The data proved the opposite.

What Driver 5 is doing is carrying more speed through the corners —
61 km/h minimum corner speed vs 54 km/h for Driver 4. By the time they
reach the straight, the work is already done. They don't need full throttle
because they never lost the speed in the first place.

Driver 3, meanwhile, has 14.8 seconds of wheelspin above 3% in a single
lap — pushing hard on throttle but fighting the car instead of working
with it.

There's a saying in motorsport — the fast way out of a corner is the slow
way in. Driver 5's data is the clearest proof of that I've ever seen.

---

### Layer 5 — Is the car surviving?
`Water Temp · Oil Temp · Oil Press · Head Temp · Exhaust Temp · Lambda · Fuel Level · Battery Voltage · Logger Temp`

The final question — after everything the drivers put the car through,
is it actually okay?

Driver 5's car is fine. Oil temperature peaks at 113.2°C, well clear of
the viscosity threshold. Oil pressure drops 0.16 bar across the full race.
Battery voltage never goes below 11.90V. The engine is being loaded hard
— 38°C oil temperature rise confirms that — but everything stays within
safe limits. This car goes straight back out.

Driver 4's car has one thing that needs fixing before the next session —
the voltage collapse to 10.70V at the end of the race. Nineteen seconds
below the instability threshold is not something you ignore. The thermal
load is aggressive but within limits. The electrical fault is the priority.

Driver 3's car is the one I'd be most concerned about. Highest water
temperature, oil within 0.2°C of the viscosity damage threshold, steepest
oil pressure drop in the dataset. None of those individually is a confirmed
failure. Together they describe a car that was thermally saturated through
most of this race and never found its equilibrium. And the uncomfortable
part is that the heat isn't coming from fast cornering — it's coming from
wheelspin, over-revving, and poor traction at corner exit. The same issues
the driving data already identified in Layer 3.


---

## Tools

- Python · Pandas · NumPy · Matplotlib

---

## About me

I'm an electronics engineering student working toward a career in
motorsport. This project is me putting everything I've learned so far
into one place — and pushing beyond it.

-K.SAHITHI CHANDANA
[ https://www.linkedin.com/in/sahithichandanakonyala]

