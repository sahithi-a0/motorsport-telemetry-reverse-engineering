## ANALYSIS
## LAYER-3- Each Driver’s Driving Style

# Plot 1 — Driver Inputs Trace (Speed, Throttle, Brake, Steering)
The inputs trace is where the lap stops being a number and starts being a story. Four channels — speed, throttle, brake, steering — plotted against lap distance. Everything the driver does physically shows up here. Reading it well means understanding what each channel is actually measuring versus what it's responding to. Throttle position is something the driver controls directly. Speed is what happens as a result.
Looking at the speed channel first. Driver 5 leads on every metric — top speed of 198 km/h, minimum corner speed of 61 km/h, and an average lap speed of 114 km/h. Driver 4 runs 194 km/h top speed with a 54 km/h minimum, averaging 112 km/h. Driver 3 tops out at 193 km/h with a 59 km/h minimum and 110 km/h average. That 4 km/h difference in average speed between Driver 5 and Driver 3, sustained over 2,154 metres, directly accounts for the 2.7 second gap between their best qualifying times of 1:08.5 and 1:11.2. The average speed number is the clearest single indicator of overall pace.
The throttle channel throws up something that looks counter-intuitive at first. Driver 4 is on full throttle for 28.8 seconds — 41% of the lap. Driver 3 for 27.1 seconds — 38%. Driver 5, the fastest of the three, is at fully saturated throttle for only 2.1 seconds. That's 3% of the lap. The instinct is to assume the fastest driver should be on the power the most, but that's not what's happening here. Driver 5 is modulating continuously — partial throttle blended with lateral load through the corners, managing combined slip rather than waiting for a clean straight to apply full power. It's a more demanding technique to execute but a more efficient one in terms of lap time.
The brake channel needs a flag before any conclusions are drawn. Driver 3 shows brake position above 5% for 67.9 seconds out of a 71.2 second lap — that's 95% of the lap with the brake pedal partially depressed. Physically, that doesn't hold up for this circuit. What it almost certainly indicates is a sensor zero offset — a small mechanical preload sitting in the pedal position sensor that keeps the reading artificially elevated at rest. This is a data quality issue and it needs to be noted. It doesn't invalidate the brake pressure analysis in Plot 6, which reads hydraulic pressure at the caliper independently, but it does mean Driver 3's brake position numbers cannot be taken at face value. Driver 4's 26.0 seconds and Driver 5's 23.4 seconds on brake are both physically plausible for this layout.
On steering, Driver 3 reaches 90 degrees right and 80 degrees left. Driver 5 shows 103 degrees right and 97 degrees left — the most symmetric of the three, which suggests the most balanced line through left and right hand corners. Driver 4 records an anomalous 176 degree value on the right. That's physically impossible for a conventional rack-and-pinion system. It confirms a sensor scaling or calibration issue on Driver 4's steering channel, which needs to be resolved before that data can be used for technique analysis.
________________________________________



# Plot 2 — Trail Braking Gate
Trail braking is the technique of holding brake pressure into corner entry while simultaneously beginning to steer. Done correctly, it progressively loads the front axle, increases front grip, and allows a later apex. It's a transient technique — it operates in the transition phase between braking and cornering — not something that should be active for large portions of a lap.
In qualifying, Driver 3 registers trail braking for 45.4 seconds across 33 zones — 64% of the lap. That number is again a direct consequence of the brake sensor offset identified in Plot 1. When the pedal position sensor reads above 5% at rest and the throttle is also above 5%, the logical gate that detects trail braking activates continuously. The genuine trail braking events for Driver 3 are the longer, sustained zones visible on the distance trace — not the short scattered flicker events.
Driver 4 trail brakes for 5.1 seconds — 7% of the lap — despite having the most braking zones detected across the session. Driver 5 registers 3.5 seconds — 5%, across 16 zones. Both of those numbers point toward a point-and-squirt technique: brake hard and straight, get the rotation done, then commit to the throttle. It prioritises traction at corner exit over minimum speed at the apex. On a circuit with this many tight hairpins, that's a defensible approach.
In the race, Driver 4's trail braking count jumps sharply — from 5.1 seconds across 37 zones in qualifying to 34.1 seconds across 69 zones. That near-doubling of zones detected tells you the braking inputs became significantly more varied under race conditions, likely from traffic management or tyre degradation changing what corner entry required. Driver 5 stays at 2.5 seconds — 3% — consistent and disciplined across both sessions.
________________________________________
# Plot 3 — Throttle Derivative
The throttle derivative isn't telling you what the throttle is doing — it's telling you how fast it's changing. That distinction matters. A high positive rate is an aggressive snap open. A high negative rate is a sudden lift. Together they give you the aggression signature of each driver's throttle technique.
In qualifying, Driver 5 records the highest closing rate at -1,060 %/s — the most decisive lift of the three. When Driver 5 comes off the throttle, it happens almost instantaneously. Full commitment to the braking event, no hesitation. Their maximum opening rate is 630 %/s. Driver 3's opening rate is the slowest at 394 %/s, with a closing rate of -928 %/s. Driver 4 sits in between at 505 %/s opening and -990 %/s closing.
The mean opening rate tells you more about lap time than the peak values. Driver 5's mean of 47 %/s is the lowest of the three — lower than Driver 3's 71 %/s and Driver 4's 54 %/s. A lower mean opening rate means Driver 5 builds throttle more gradually on average. That's entirely consistent with the partial throttle technique seen in Plot 1 — managing combined slip at corner exit rather than snapping to full power and risking wheelspin. The faster application rates from Driver 3 and Driver 4 suggest a more binary on-off throttle style.
In the race, Driver 3's maximum opening rate jumps to 733 %/s — significantly more aggressive than their qualifying technique. The mean drops to 54 %/s though, which means those aggressive spikes are concentrated at specific corners rather than a change in general style. It could be tyre degradation forcing more binary inputs, or overtaking attempts demanding faster corner exit acceleration. Driver 4 and Driver 5 both remain broadly similar between qualifying and race — more repeatable technique, less reactive to conditions.
________________________________________
# Plot 4 — GG Diagram
The GG diagram is the performance envelope. Lateral acceleration plotted against longitudinal acceleration for every data point in the lap. A driver fully exploiting the tyre's combined grip limit produces a circular or diamond-shaped cloud that fills the theoretical boundary. A driver leaving grip unused shows a cloud that doesn't reach it.
Driver 3 in qualifying shows a lateral peak of 5.890g and maximum braking deceleration of 5.410g. The 98th percentile grip envelope sits at 5.314g — high, consistent with a formula-style car generating meaningful aerodynamic downforce at speed. Mean combined G across the lap is 2.277g, meaning Driver 3 uses an average of 43% of peak grip capacity throughout the lap.
Driver 4's grip envelope in qualifying is 2.562g — significantly lower than Driver 3's 5.314g, with both drivers in the same car. That is the most concerning data point in the entire Layer 3 analysis. Either the accelerometer channels on Driver 4's car carry a scaling error — plausible given the brake and steering sensor issues already identified — or Driver 4 is genuinely not loading the car through the corners. A mean combined G of 1.124g against Driver 3's 2.277g is too large a gap to be attributed to driving style alone. The sensor calibration needs to be checked before any conclusions are drawn from Driver 4's GG data.
Driver 5 sits at 2.809g envelope and 1.206g mean — similar in magnitude to Driver 4, which raises the same calibration question. But Driver 5 is the fastest driver in the session. If those G values are genuine, then Driver 5 is generating the fastest lap time with the least peak grip loading — which is physically possible through very smooth corner transitions and minimal combined slip events. It would actually reinforce everything the throttle and slip ratio data already suggests about their technique.
In the race, all three drivers show reduced envelopes against qualifying. Expected — tyre degradation, fuel load changes, the tyres simply not operating at the same peak level. Driver 3 drops from 5.314g to 5.185g. Driver 4 and Driver 5 both hold near their qualifying values. The consistency of those low G readings across both sessions for Driver 4 and Driver 5 makes the sensor calibration question harder to dismiss.
________________________________________
# Plot 5 — Steering Derivative
The steering derivative shows whether corner entry is smooth or aggressive. A smooth driver produces a sustained, moderate turn-in rate with gradual unwinding. An aggressive driver shows sharp spikes at turn-in and fast unwinding at the apex — what engineers call a low steering smoothness index.
Driver 3 in qualifying shows a maximum steering rate of 631 deg/s to the right and -1,200 deg/s to the left. The left side rate is nearly double the right. That level of asymmetry is significant — Driver 3 is substantially more aggressive turning into left-hand corners than right-hand corners. On a circuit where the primary braking zones feed into left-hand hairpins, there may be a deliberate rotation strategy behind it, but it also raises the possibility of a tendency toward transient oversteer on left-hand entry. Something worth watching in the video if it's available.
Driver 4 shows 592 deg/s right and -562 deg/s left — the most symmetric of the three. Balanced, neutral inputs into both directions. Driver 5 reads 649 deg/s right and -532 deg/s left, with a mean absolute rate of 52 deg/s. The time above 200 deg/s — the aggressive input threshold — is broadly similar across all three drivers at 3.2 to 4.2 seconds per lap. So the number of aggressive steering events is comparable. What differs is how extreme those events are when they happen.
In the race, Driver 3's steering asymmetry reverses completely. Maximum rate to the right jumps to 1,310 deg/s while the left drops to -643 deg/s — a full inversion of the qualifying pattern. Race traffic could explain it, different corner priorities under defensive driving. Another possibility is tyre degradation affecting one side of the car more than the other, changing the balance and requiring more aggressive input on the side that was previously smooth to achieve the same rotation.
________________________________________
# Plot 6 — Brake Pressure Delta
The brake pressure channel is the most reliable braking metric in this dataset. It measures actual hydraulic force at the caliper — independent of the pedal position sensor issues that affected Plots 1 and 2. These numbers can be trusted.
Driver 5 produces the highest peak brake pressure at 39.70 bar. That's harder than Driver 3 at 36.09 bar and Driver 4 at 34.91 bar. Consistent with Driver 5 braking later and arriving at corner entry with more speed. Their mean active brake pressure of 12.44 bar is also the highest — not just a harder peak, but sustained threshold braking held through the full deceleration phase rather than a quick spike and release.
Driver 3's mean active pressure tells a different story at 4.30 bar — significantly lower than Driver 5's 12.44 bar despite a similar peak. That pattern describes a driver who hits the brakes hard at the initial application and then quickly releases pressure, rather than holding threshold through the middle of the braking zone. The car decelerates efficiently at the start of braking and then less so. It's a common technique issue — the instinct to release the pedal once the initial load is in, rather than trusting the threshold and holding it.
Driver 4 shows 10 braking zones detected in qualifying against Driver 5's 8. More events in the same lap length means Driver 4 is splitting what the other drivers treat as a single braking event into multiple applications — building, partially releasing, reapplying. It's a legitimate technique for managing front-end balance on corner entry, but it's less efficient than clean threshold braking held through the zone.
In the race, Driver 4's peak rises to 36.45 bar and the number of braking zones increases to 13 — consistent with the increased trail braking activity in Plot 2, more complex application patterns under race conditions. Driver 5's peak drops considerably to 26.61 bar from their 39.70 bar qualifying peak. Whether that's tyre management, a deliberate strategy to reduce brake stress over the full race distance, or a braking point change that allows a lower peak while maintaining corner entry speed — that would need the stint data to confirm.
________________________________________

# Plot 7 — Wheel Slip Ratio
The slip ratio is a derived channel — vehicle speed minus GPS speed, divided by GPS speed, expressed as a percentage. Positive values are wheelspin, driven wheels rotating faster than actual ground velocity. Negative values are lockup, wheels rotating slower than the car is travelling during braking.
In qualifying, Driver 4 produces the highest peak wheelspin at 10.17% but the shortest duration above the 3% threshold at 11.2 seconds. Driver 3 peaks lower at 9.28% but sustains it the longest — 14.8 seconds above threshold. Driver 5 is the most efficient across both metrics: lowest peak at 8.32% and 12.0 seconds above threshold.
What makes Driver 5's numbers meaningful isn't just the lower peak — it's the combination of lower peak, shorter duration, and faster recovery. Sustained wheelspin above 3% is energy going into tyre heat and wear rather than forward velocity. Driver 3's 14.8 seconds of significant wheelspin in a 71.2 second lap means roughly 21% of the lap the driven wheels aren't operating at peak traction efficiency.
On the lockup side, all three drivers show brief spikes in the heaviest braking zones — normal behaviour. None are carrying sustained lockup events. Driver 5 peaks at -5.04% for 1.0 second, Driver 3 at -4.76% for 0.7 seconds, Driver 4 at -4.66% for 1.2 seconds. Short, sharp, and recovered quickly.
The location of Driver 3's peak wheelspin is the detail that stands out. That 9.28% peak occurs at a throttle position of only 26% — mid-corner, not on the straight under full acceleration. The car is breaking traction under partial throttle while still carrying lateral load. That's a combined slip condition, and it's a specific problem with a specific set of solutions — either a differential calibration change to reduce locking under partial throttle, or a throttle map adjustment that reduces torque delivery during the mid-corner phase. It's not something the driver can fully manage on their own without a mechanical change underneath them.











## Driver 4
# Plot 1 — Driver Inputs Trace
Speed
Best lap of 69.8 seconds, 194 km/h top speed, 54 km/h minimum corner speed. Average speed of 112 km/h puts Driver 4 between the other two. The trace looks clean — proper peaks on the straights, sharp drops into corners, nothing alarming mid-corner.
The minimum corner speed of 54 km/h is the problem. That's 7 km/h slower than Driver 5 through the tightest hairpins. On a circuit where more than half the lap is spent cornering, arriving at apices that much slower isn't a rounding error — it's a structural deficit that compounds corner after corner.
Throttle
41% of the lap at full throttle — highest of the three drivers. That sounds committed. What it actually means is Driver 4 exits corners slower and needs more straight to recover the speed. The throttle is working harder because the corners aren't working well enough. One other flag — maximum throttle reads 102%. Sensor calibration offset, consistent with the other channel issues on this car.
Brake
Maximum brake position of 170%, mean active of 52.6%. Both physically impossible. This channel is unusable. All braking conclusions for Driver 4 come from the hydraulic pressure sensor in Plot 6, which is independent and clean.
Steering
176 degrees right — can't happen on a conventional rack. Same calibration problem as the throttle, almost certainly linked to the voltage instability found in the car health data. Mean absolute angle of 31.5 degrees is the lowest of the three, but whether that reflects wider lines or a compressed sensor reading can't be confirmed without recalibration.
________________________________________
# Plot 2 — Trail Braking Gate
5.1 seconds of trail braking across 37 detected zones. Thirty-seven zones in a 70 second lap means one detection every 1.9 seconds — that's not trail braking, that's the brake sensor reading slightly above zero at rest and triggering the gate every time the throttle rises above 5%.
The real trail braking events are the longer sustained signals on the plot. Strip the sensor noise out and you're probably looking at 6 to 8 genuine events at the primary corners. Driver 4 is fundamentally a threshold braker. The raw zone count makes them look like something else, but the data doesn't support that once the sensor issue is accounted for.
________________________________________
# Plot 3 — Throttle Derivative
Opening rate of 505 %/s, closing rate of -990 %/s. The closing rate is decisive — when Driver 4 lifts for a braking zone, they commit instantly and completely.
The derivative trace tells the technique story clearly. Large spikes at corner exits where the throttle snaps open, large negative spikes at the next braking zone where it shuts hard. Very little in between. That's point-and-squirt in data form — wait for a clean traction window, commit to the throttle fully, then close it sharply for the next corner. The throttle is either opening hard or shutting hard. Not much modulation in the middle.
Mean opening rate of 54 %/s versus Driver 5's 47 %/s. Driver 4 gets to full throttle slightly faster, but from a lower corner exit speed — so there's less traction stress at the moment of application. The technique can afford to be more aggressive precisely because the corner has already been mostly dealt with before the throttle opens.
________________________________________
# Plot 4 — GG Diagram
Grip envelope of 2.562g against Driver 3's 5.314g. Same car, same circuit. That gap cannot be real cornering force difference. Either the accelerometer is running at half sensitivity, or the voltage instability is causing sensor drift across multiple channels at once. The quadrant time distribution — how long Driver 4 spends in each combination of lateral and longitudinal load — looks proportionate and believable. The magnitudes don't. Shape of the technique is readable, the actual G numbers can't be used for comparison until the accelerometer calibration is checked.
________________________________________
# Plot 5 — Steering Derivative
Maximum right rate of 592 deg/s, maximum left of 562 deg/s. That's almost perfectly symmetric — a 1.05 to 1 ratio between the two sides. Driver 4 is the most balanced driver in this dataset in terms of directional steering aggression. No preference for one corner type over another, no direction where they're more hesitant or more aggressive. Right input time of 32.1 seconds, left input time of 31.6 seconds — the symmetry holds at the macro level too.
Mean absolute rate of 57 deg/s is the highest of the three, which suggests more active corrections throughout the lap. Whether that's the car moving around or a technique that requires more continuous input to hold the line, the G data isn't reliable enough to answer definitively.
________________________________________
# Plot 6 — Brake Pressure Delta
Ten braking zones, maximum peak of 34.91 bar at the first hairpin, mean active pressure of 12.61 bar — highest of the three drivers.
The ten zones split into four primary events above 20 bar and six secondary events below 15. The secondary zones are where the story is. Three of those six cluster between 1,158 and 1,170 metres — three separate brake applications within 12 metres of each other. That's the chicane. Press, partial release, press again through the direction changes instead of carrying momentum. Each release and reapplication shifts load transfer back and forth across the front axle, unsettles the car, and costs time that a single clean application wouldn't.
The comparison with Driver 5 makes it concrete. Both have almost identical mean active pressures — 12.61 versus 12.44 bar. Both press hard when they brake. Driver 5 does it across 8 clean zones, Driver 4 across 10 fragmented ones. Same effort, less efficient execution.
________________________________________
# Plot 7 — Wheel Slip Ratio
Maximum wheelspin of 10.17% at 22% throttle position, mid-corner. Not on the straight under full power — in the middle of a corner under partial throttle while still carrying lateral load. The tyre is already generating cornering force and the driven wheels are asking it to do too much at the same time. Combined slip, and the tyre loses.
Wheelspin time above 3% is 11.25 seconds. Adjusted for lap length, that's 16.1% of the lap in significant wheelspin against Driver 3's 20.8%. Better than Driver 3 per unit of lap time, not as clean as Driver 5.
The -4.66% lockup at 571 metres with essentially zero brake pressure is a GPS artefact — high lateral G in a tight corner causing momentary measurement error, not a real lockup. Genuine lockup events total 1.15 seconds below the -3% threshold, concentrated at the heavy braking zones where the pressure data confirms hard application. Mean absolute slip of 1.587% — lowest of the three — means outside of those discrete events, Driver 4 is running clean traction across most of the lap.
________________________________________


















## Driver 5
# Plot 1 — Driver Inputs Trace
Speed
198 km/h top speed. 61 km/h minimum corner speed. 114 km/h average speed. 68.5 second best lap. Every single speed metric is first place. Not faster on the straight and even elsewhere — faster everywhere, at every measuring point, across the whole lap.
Throttle
Full throttle time of 2.1 seconds. Three percent of the lap. The fastest driver on the circuit is barely using a flat throttle. That's the most confusing number in the dataset until you understand what's happening in the other 97%.
Driver 5 spends 45.2 seconds in the partial throttle zone — blending the power in progressively while the car is still turning. Not waiting for a clean straight to open up before applying throttle. Managing the tyre as it transitions from pure cornering load to combined cornering and acceleration load simultaneously. It's a harder technique to execute but it gets the car accelerating sooner. On a circuit this short and this corner-heavy, sooner means everything.
Brake
On-brake time of 23.4 seconds — lowest of the three. Maximum brake position of 83% is the only physically credible maximum reading in the whole dataset. Mean active brake position of 53.9% confirms Driver 5 holds pressure through the braking zone rather than hitting a peak and releasing. Threshold technique visible even before the pressure data is opened.
Steering
103 degrees right, 97 degrees left. Six degree difference between the two sides — essentially nothing. Mean absolute angle of 25.5 degrees is the lowest of the three. Less steering movement at higher corner speeds isn't caution — it's a better line. Driver 5 is flowing through corners on a wider arc, using the full width of the circuit, needing less lock at the apex because the car isn't being rotated aggressively into a tight line. The steering is quieter because the approach is better.
________________________________________
# Plot 2 — Trail Braking Gate
3.5 seconds — 5% of the lap — across 16 zones. Lowest of the three on every measure. This fits perfectly with everything else in Driver 5's data. When you're managing load transfer through continuous partial throttle throughout the corner, you don't need the brake to generate front-end grip. The throttle is already doing that job. The brake becomes a precision tool used at specific corners for specific rotation needs, not something that gets dragged into every corner by default.
When Driver 5 does trail brake, it's a deliberate decision. The low count isn't a gap in technique — it's evidence of knowing when to use it and when not to.
________________________________________
# Plot 3 — Throttle Derivative
Maximum opening rate of 630 %/s — highest of the three. Maximum closing rate of -1,060 %/s — also highest. The fastest inputs in both directions from the driver who barely uses full throttle. That feels like a contradiction until you look at where those peaks actually occur.
The high rates happen at transition moments — specifically when the corner releases onto the straight and Driver 5 commits fully to the power. At that exact moment, the input is sharp and decisive. Same on the lift — when the braking point comes, the throttle shuts instantly. The aggression is concentrated at the transitions, not spread through the corners.
Mean opening rate of 47 %/s — the lowest of the three. High peaks, low mean. Smooth and gradual through the loaded phase of the corner, then sharp and decisive at the moment it opens up. Smooth where it protects traction, aggressive where it gains time. Knowing the difference between those two moments is the whole technique.
________________________________________
# Plot 4 — GG Diagram
Grip envelope of 2.809g — largest of Driver 4 and Driver 5, though the same calibration question applies as it did for Driver 4. The absolute numbers can't be directly compared to Driver 3 without verifying the accelerometer gain settings first.
What is reliable is the shape. Driver 5 spends 21.6 seconds accelerating while turning right — more than any other driver in that quadrant. Accelerating right means exiting the left-hand hairpins onto the main straight. The primary performance zone on this circuit. Driver 5 spends more time in the combined-load cornering phase than anyone else. That's the partial throttle technique visible in the GG diagram — more time in the zone where lateral and longitudinal forces are being managed simultaneously.
Maximum lateral G of 5.070g dominates the profile. More lateral force than braking or acceleration. That's what a driver looks like when corner speed is the priority above everything else.
________________________________________
# Plot 5 — Steering Derivative
Maximum right rate of 649 deg/s, maximum left of 532 deg/s. Slightly more aggressive turning right, which feeds the left-hand hairpins — the fastest and most important section of this circuit. Driver 5 is marginally more aggressive entering the corners where the most time is available to be gained.
Aggressive input time above 200 deg/s is just 3.15 seconds — lowest of the three. Fewest sudden high-rate steering inputs per lap. When a high-rate input does appear, it's intentional. Right input time 30.8 seconds, left input time 31.0 seconds — identical. Completely symmetric across both directions of the circuit. No corner type where Driver 5 is less comfortable, no direction an opponent could exploit. There's no weakness visible anywhere in this steering data.
________________________________________
# Plot 6 — Brake Pressure Delta
Eight zones — fewest of the three. Maximum peak of 39.70 bar — the hardest single braking event in the entire qualifying dataset across all three drivers. Driver 5 arrives at that corner fastest and brakes hardest. Both simultaneously. The only way that works is a later braking point — arriving at higher speed with the same marker would need even more pressure or a longer stopping distance. Driver 5 is braking later, not just harder.
Through the chicane where Driver 4 shows six fragmented applications, Driver 5 shows three — all at lower pressures than Driver 4's equivalent zones. More speed carried in, less deceleration needed. Fewer inputs, cleaner execution.
Mean active pressure of 12.44 bar — almost identical to Driver 4's 12.61. Both press hard when they brake. Driver 5 just does it in fewer, better organised events, holding threshold pressure all the way through the zone rather than peaking and releasing.
________________________________________
# Plot 7 — Wheel Slip Ratio
Maximum wheelspin of 8.32% — lowest in qualifying. The throttle position at that moment reads -6%, essentially zero. Driver 5's highest wheelspin reading isn't even under power — it's a GPS artefact from a tight corner under high lateral load. Genuine wheelspin under power is lower than the headline number suggests.
Maximum lockup of -5.04% under 30.25 bar at the first hairpin. That's real — brief, at the absolute braking limit, recovered in under a second. A momentary lockup at the hardest braking point on the circuit isn't a mistake. It's evidence the driver is right at the edge of what the tyre can hold.
Mean absolute slip of 1.624% — middle of the three. Driver 4's 1.587% is marginally lower, but accounting for Driver 4's GPS artefacts, both are managing traction at a similar level. Both are clearly better than Driver 3.














## CONCLUSION
Driver 3 — Working Hard, Getting Less Back
Driver 3 is the busiest driver in this data. Most steering movement, most throttle snapping, hard braking everywhere. From inside the cockpit this probably feels like a committed, aggressive lap. The data doesn't agree.
The core problem with Driver 3 isn't effort — it's that the effort and the results have come apart. The car is being worked harder than either of the other two at almost every measurable point, and the lap times are the slowest of the three. That gap between input and output is the entire coaching brief.
Take the throttle. Full throttle for 38% of the lap sounds like commitment. But those full-throttle periods start later than Driver 5's partial throttle application. Driver 3 waits until the corner is completely finished before opening the power. Driver 5 is already accelerating before the corner is finished. By the time Driver 3 is flat, Driver 5 has already built the speed and needs less of the straight to carry it forward.
The braking tells a similar story. Hard initial hit, quick release, mean active pressure of only 4.30 bar. Driver 3 commits to the braking point but doesn't hold threshold pressure through the middle of the stop. The car decelerates hardest at the very start of the braking zone and then less efficiently after that. It's not bad braking — it's incomplete braking. The corner entry suffers for it.
Then there's the wheelspin. Fourteen seconds above 3% in a 71 second lap. That's a lot. But the detail that makes it worse is where it happens — at 26% throttle, mid-corner, while the car is still generating lateral load. This isn't bold throttle application on a straight. The car is breaking traction in the loaded phase of the corner, where the tyre is already being asked to produce cornering force and simply can't produce traction on top of it at the same time. The result is heat, tyre wear, lost time, and an engine working harder than necessary — all happening simultaneously and all for the same root cause.
The steering asymmetry — more aggressive into left-hand corners than right — either means the car is harder to rotate one way, the driver has less confidence one way, or both. On a circuit where the main hairpins are left-hand corners, that's a significant weakness in exactly the wrong place.
Driver 3 is not lacking effort or commitment. What's lacking is efficiency — the ability to convert that effort into corner speed rather than heat and wheelspin. Fix the corner exit and almost everything else improves at the same time.
________________________________________
Driver 4 — The Best Braker, But Braking is Only Half the Corner
Driver 4 structures a lap differently to the other two. Each corner is a sequence of separate events — brake, turn, accelerate — each handled cleanly in isolation. Within each individual phase, the technique is actually very good. The weakness is the space between those phases.
The braking is genuinely the strongest part of this dataset. Peak pressure of 34.91 bar at the first hairpin, mean active pressure of 12.61 bar — the most sustained threshold braking of the three. Driver 4 doesn't spike and release. When the brakes go on, they stay on through the zone. That's a real technical quality and it wins the braking phase of every major corner.
But the braking data also reveals the problem. Ten zones in qualifying — the most of any driver — with three of them clustered within 12 metres of each other through the chicane. Apply, partial release, reapply. Apply, partial release, reapply. Each cycle unsettles the front axle and costs time. On a long fast circuit with proper straights, treating every corner as a full stop and restart is a workable approach. On this circuit, where the next corner arrives within 200 to 300 metres of the previous one in the technical sections, there simply isn't enough room to do it that way efficiently.
The throttle derivative confirms the philosophy — open hard, close hard, not much in between. It works in the heavy braking zones. It's too blunt for the flowing sections. The minimum corner speed of 54 km/h — the lowest of the three — is the cost of that approach. The commitment goes into the braking entry and runs out before the apex.
Driver 4 is a neutral, balanced driver — symmetric steering inputs across left and right, proportionate technique in both directions. No obvious weakness an opponent can target. But neutral commitment producing the lowest minimum corner speed on a circuit where cornering is everything is still a problem, regardless of how balanced it looks.
One thing that needs to be said clearly — the sensor issues on Driver 4's car, the impossible steering angles, the over-range throttle and brake values, all trace back to the electrical instability confirmed in the car health analysis. Until that's fixed, some of what's in the data can't be fully trusted, and the corner exit technique can't be properly evaluated. Sort the electrics first, then come back to the fine details.
________________________________________
Driver 5 — A Different Way of Thinking About a Corner
Driver 5 doesn't fit neatly into either of the other two profiles. Not the hardest braker — Driver 4 holds more sustained pressure. Not the most committed on the throttle — Driver 3 and Driver 4 both spend more time at full power. Doesn't use trail braking the most. And yet every single performance number belongs to Driver 5. Fastest lap, highest average speed, highest minimum corner speed, lowest wheelspin, best consistency.
The technique is built on one idea — the tyre contact patch has a limited budget, and the driver who spends that budget most intelligently wins.
While Driver 3 and Driver 4 are waiting for the car to be straight before opening the throttle, Driver 5 is already on partial power through the corner. Not full power — the tyre can't generate maximum cornering force and maximum acceleration simultaneously. But partial power, progressively building, shifting the load from pure lateral toward combined lateral and longitudinal before the corner has fully finished. By the time the car reaches the straight, Driver 5 has already been accelerating for several hundred metres. The straight is shorter because less of it is needed to reach the next braking point.
This is why the 2.1 seconds of full throttle makes complete sense once you understand it. Full throttle is only needed in the brief gap between the corner fully releasing and the next braking zone arriving. On a 2,154 metre lap with a main straight of roughly 400 metres, that gap is genuinely short. Driver 5 was already accelerating through the corner — the straight is just where the partial throttle becomes full throttle for a moment before the brakes go on again.
The brake pressure data — 39.70 bar peak, 12.44 bar mean across 8 clean zones — describes someone who brakes later, harder, and holds it longer than the others. The later braking point is only possible because of the higher corner exit speed from the corner before. Each corner feeds the next. The technique compounds on itself in a way that point-and-squirt simply can't replicate, because point-and-squirt resets to zero at every corner entry.
The brief lockup at -5.04% under 30.25 bar of brake pressure at the first hairpin is worth mentioning. It's not a mistake. A driver who never gets close to a lockup is not braking at the limit. Driver 5 touches the limit, holds it for under a second, and recovers cleanly. That's threshold braking done correctly — finding the absolute edge of adhesion and staying there rather than backing away from it.
Symmetric steering across both directions, no corner type where the confidence visibly drops, lowest wheelspin in the field despite the highest corner speeds. The technique that generates the most speed also generates the least traction loss. Those two things aren't in tension with each other — they're the same technique producing both outcomes simultaneously.
________________________________________
# One Line Each
Driver 3 — more effort than anyone, less return than anyone, and the distance between those two facts is exactly what needs to be fixed.
Driver 4 — wins every braking zone, but braking is where the corner ends, not where the lap time is made.
Driver 5 — not driving harder than the others, just using the tyre better than the others, and on this circuit that turns out to be the only thing that matters.


