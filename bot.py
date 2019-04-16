"""
This will be the created bot stub which our genetic program will 'design'
It has functions to respond to the on screen events
It will be constantly calling event functions based on screen (update every 0.1 sec??)
    --> Possible second variable parameter for mutation or crossover
Once a certain threshold is reached (differs from event to event), it will trigger its action
These functions are going to be our actual crossover as such hopefully maintaining good responses

TODO:

Coding side:

Write the stubs for every permutation of events and write the main runner
Parallelize runners
Seed original parameters
Generate Population
Write the genetic runner
Possibly slim the codebase to only important

Theoretical Side:
Paper on how to speed up
    --> Possible idea is to use heuristic value for fitness, for example local maxima until considered good
    --> Approach in paper is using similarity of two bots to measure fitness
        ==> Similar bots will be similarily fit
How to determine pixels (objects)
    pixel grabbing is too slow
    --> New idea:
        Iterate over all objects on screen and their location and based on their distance to dino react,
        instead of "seeing" objects
Possible good practice would be to split up code base

Pass all objects to a function to check what object is closest 
and then trigger event in individuals 

"""