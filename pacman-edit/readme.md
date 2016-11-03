### Configuration

```bash
-g DirectionalGhost -p ApproximateQAgent -a extractor=SimpleExtractor -x 100 -n 110 -l mediumClassic
```
Run the ***pacman.py*** script with the above configuration for correct game initiation.

#### Explanation of configuration

`-g DirectionalGhost` defines the ghost agent (*DirectionalGhost*) being used.  
`-p ApproximateQAgent` defines the pacman agent (*ApproximateQAgent*) being used.  
`-a extractor=SimpleExtractor` defines agent arguments.  
`-x 100` defines the number of training sessions (*100 sessions*) the pacman learns for.  
`-n 110` defines the number of games (*110 games, 100 if which are training*) the pacman.py script runs for.  
`-l mediumClassic` defines the map (*mediumClassic*) being used for the games. 

### Author
The solutions to the problems originally posted at the Pacman project site were developed by Ramón Argüello ([@monchote](https://github.com/monchote)) back in 2011.

### Resources

[Lecture 11: Reinforcement Learning II](https://youtu.be/yNeSFbE1jdY?t=25m41s)  
[UC Berkeley CS188 Intro to AI - Project 3: Reinforcement Learning](http://ai.berkeley.edu/reinforcement.html)  
[Q-learning on Wikipedia](https://en.wikipedia.org/wiki/Q-learning)  
