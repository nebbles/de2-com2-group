### Pacman AI

The principle for the Pacman AI is to get all the biscuits without being caught. In order to do this, a similar system to the Ghost AI can be used, whereby the Pacman will calculate the distance to all remaining biscuits and choose to target the closest one. It can then use either one of the two methods mentioned in the GhostAI file about trying to get to its target tile.

**The exception** to this is with regards to the position of the Ghost that is trying to capture it. The Pacman needs to be intelligent enough to know that it does not want to run into the Ghost. Equally though, we don't want a *fearful* Pacman where all it is worried about is whether it is getting closer to the Ghost.  

As such a 'danger zone' would need to be implemented. This 'danger zone' would come into play when the Ghost enters the Pacman's personal space. At this point the Pacman would actively adjust its biscuit-seeking bahaviour so as to not put itself in any further danger.

A further step can be taken whereby a Ghost in the 'critical zone' for a Pacman results in a complete behaviour change for the Pacman. This would mean that the Ghost is so close that evasive behaviour is required of the Pacman to try and escape being eaten. In this mode, whether time or distance-(to-Ghost) based, the Pacman would need to focus entirely on increasing its distance from the Ghost.
