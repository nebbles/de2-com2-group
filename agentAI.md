## Agent AI in game

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

The above solution can be seen as a 'short-sighted' solution. This is because the Ghost only uses the general direction to help it decipher how it should deal with what is directly in front of it. We can make this more advanced by allowing the Ghost AI to be 'long-sighted' which is that the Ghost plans its entire route ahead of time and updates this route with every iteration to make it more accurate or to correct its route.

### Pacman AI

The principle for the Pacman AI is to get all the biscuits without being caught. In order to do this, a similar system to the Ghost AI can be used, whereby the Pacman will calculate the distance to all remaining biscuits and choose to target the closest one. It can then use either one of the two methods mentioned in the GhostAI file about trying to get to its target tile.

**The exception** to this is with regards to the position of the Ghost that is trying to capture it. The Pacman needs to be intelligent enough to know that it does not want to run into the Ghost. Equally though, we don't want a *fearful* Pacman where all it is worried about is whether it is getting closer to the Ghost.  

As such a 'danger zone' would need to be implemented. This 'danger zone' would come into play when the Ghost enters the Pacman's personal space. At this point the Pacman would actively adjust its biscuit-seeking bahaviour so as to not put itself in any further danger.

A further step can be taken whereby a Ghost in the 'critical zone' for a Pacman results in a complete behaviour change for the Pacman. This would mean that the Ghost is so close that evasive behaviour is required of the Pacman to try and escape being eaten. In this mode, whether time or distance-(to-Ghost) based, the Pacman would need to focus entirely on increasing its distance from the Ghost.
