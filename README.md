# Codingame-Assignment

*Platinum Rift 2*

My Codingame nickname is SinemCevik. Student No.20180808026

There is few parts to my strategy:

-For the first 10 turns, I focus on area expansion, the existing pods are divided into 2 per turn (with a minimum of 1 driven pod). 
After turn 10, the number of pod moves is slightly changed.

-For the direction of movement, I use a decision weight, so that the pod will tend to move towards a location with a higher value, 
according to the decision weight of that zone.

-If the direction the pods are going is a dead end, I gave the other pods a tendency to point elsewhere.

-I direct the newly spawned pod to the outer border of the zone that I chosen. This is done so that there is no accumulation 
of pods around the HQ in the mid-late game because of to the decision weight which tends to be the same, considering that the zone 
around the HQ is homogeneous and we own the majority.

-A factor in the decision weight is quite important. I make my pods chase enemy pods that are in the zone and is centered to 
my pods location.

You could follow my comments in code for further understanding. 
