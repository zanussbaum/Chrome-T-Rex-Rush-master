"""
    TO DO STILL:
    def fitness(self):
        fitness approximation through similarity 

    def similarity(self, other):
        run two instances that are as different as possible 
        then compare with others to get an approximation of their fitness
"""
import random
import numpy
class Individual:
    """Individual class with a strategy for each scenario 

    Methods:
        _copy():
            private method to copy individual
        mutate():
            makes single point mutation 
        crossover(other):
            crossover strategies with another individual 

    Attributes:
        strategy: integer encoding of when an action will be taken
        fitness: a value based on how well an individual would do in the game 
        size: size of strategy array 
    """
    def __init__(self, size=5,arr=None):
        """Creating a random initial individual

        Parameters
            arr: copied strategy passed in 

        scenarios that can occur are:
            0 - small cactus
            1 - big cactus 
            2 - double cactus
            3 - high ptera
            4 - low ptera

        """
        self.size = size
        if arr is None:
            self.strategy = numpy.array([random.randint(-5,5) for x in range(self.size)])
        else:
            self.strategy = arr

    def _copy(self):
        """Private method that returns a copy of the individual

        Returns:
            Copy of individual with same startegy  
        """
        b = numpy.zeros(self,size, dtype=numpy.int64)

        numpy.copyto(b, self.strategy)

        return Individual(size=self.size, arr=b)

    def mutate(self):
        """Mutates a single point of the strategy


        Returns:
            copy: a mutated individual 
        """
        to_mutate = self._copy()

        point = random.randint(0,self.size)

        to_mutate.strategy[point] = random.randint(-5,5)

        return to_mutate

    def crossover(self, other):
        """crosses over two individuals

        Parameters:
            other: another individual to cross with 

        Returns:
            this_crossover, other_crossover: two new crossed individuals 
        """
        other_crossover = other._copy()
        this_crossover = self._copy()

        point = random.randint(0,self.size)

        temp = this_crossover.strategy[point:]
        this_crossover.strategy[point:] = other_crossover[point:]
        other_crossover.strategy[point:] = temp

        return this_crossover, other_crossover