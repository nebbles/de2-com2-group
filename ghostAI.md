### Ghost AI

The idea for ghost AI is to create an efficient algorithm for either chasing the pacman or to ambush the pacman. The first idea, to *chase* the pacman can be implemented using Manhatten Distance (using the *euclidean distance*). The second idea, to *ambush* the pacman is a little trickier, as the algorithm needs to recognise where the pacman might be going.

We could predict where the pacman is heading based on a couple of key pieces of information. 
By using the:
+ Pacman orientation/direction
+ By locating where any energisers are, or even the closest energiser to the pacman
+ By recognising where the majority of the food is left.

We could use the direction of the pacman and use vectors to work out a '*target tile*' that the Ghost wants to get to. As a result it can then implement the manhattan distance etc. to get there.

Another seperate system to getting to the target tile (e.g. the pacman current position) would be to think about the next turning the Ghost needs to take in order to get closer to its target. 

Say the Ghost knows the **delta x** and **delta y** between itself and the pacman then it can prioritise in which axis it needs to make progress. Combine this with the fact the ghost cannot reverse its own direction and then you have a *queue* of different turns the Ghost plans to do to improve its position with relation to the pacman by reducing its delta x and y values.
