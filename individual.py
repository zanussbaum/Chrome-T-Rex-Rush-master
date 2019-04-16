"""
Some thoughts/questions that arose when writing this:
    for the array/encoding of the strategy, do the values 
        represent when an individual will jump? Basically 
        are we fixing their actions under different scenarios 
        and finding the best strategy based on when to perform 
        those actions(jump, duck, etc.)?

    how are we measuring the fitness again? i remember
        you mentioned there was a paper discussing similarity
        and using that to approximate others

    also, this is just my initial ideas. if you don't think
        we need an object for the individual, i'm totally okay
        going that direction.

Individual class 
    Attributes:
        array/string encoding
        current fitness if possible?

    Methods:

    def __init__(self):
        create random array encoding
        array of integers that denotes the distance to which it will take the action
        where each index referes to an event in the game

        positive values mean jump
        negative values mean duck 

    def crossover(self, other):
        crossover with other
        may want to have a copy function so we are not destroying individuals

    def mutate(self):
        mutate a point on array

    def fitness(self):
        fitness approximation through similarity 

    def similarity(self, other):
        run two instances that are as different as possible 
        then compare with others to get an approximation of their fitness
"""