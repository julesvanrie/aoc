Basically got it, and quite right from the start.
But I had some small stupid errors (some small quirks that I still don't understand).

## TLDR;
- Dijkstra with two extra dimensions (current direction, and number of straight movements)
- Heaps to run it efficiently
## Basic idea:
- Dijkstra yes
  - Got that working first with my own dummy example (to make sure that my basic Dijkstra worked). Started with a large field with a bump in the middle, or a wall somehwere, and checked the path visually)
  - Implementation relatively straightforward with three arrays:
    - Shortest distance so far
    - Visited yes or no
    - Parent (where did I come from)
    - Turns out we don't even need that last one for this one. We just look for the distance, not for the path
- Then moved to this special one with constraints:
  - Fairly quickly came up with the idea to add an extra dimension to take into accont the direction we're going (so making it into 4 layers of 2D arrays)
  - First I added an extra array to keep track of how many times I moved in the same direction
  - Then thought: sometimes it might be better to back track and come to the same point, if it gives me the option to go longer straight on afterwards.
  - Took a bit of time to figure out that I also needed a 4th dimension. So basically made into 4 layers of 3D arrays now. Last dimension: 0,1,2,3 times in the same direction
  - That did the trick on my test data (well, except for some strange quirks that didn't show up in the test).
- But it was way too slow.
  - Reason was that I wrote a very basic algo to find the next shortest distance (lots of loops). And that was way too slow on the real data.
  - Considered moving to numpy. That would probably be faster to find the min.
  - But that's no fun. And wouldn't work in other langauges.
  - So did a quick search on the reddit.
  - First post "It's basically Dijkstra with 2 extra dimensions". Cool :star-struck: . That's what I thought. Didn't really dive into the code but saw this one used heaps.
  - So had a look at how heaps work, implemented. And it ran in 0.015s.
