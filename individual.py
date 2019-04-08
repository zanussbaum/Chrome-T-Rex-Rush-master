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
        create random array/string encoding

    def crossover(self, other):
        crossover with other
        maybe want to have a copy function to not changing individual object?

    def mutate(self):
        mutate a point on array

    def fitness(self):
        how are we going to measure this? 

    def similarity(self, other):
        i remember talking about this, but wasn't totally clear on this part

    def run(self, scenario):
        scenario could be an int corrseponding to the event?

        return array[scenario]?
"""