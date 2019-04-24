"""
    TO DO STILL:
    def similarity(self, other):
        --> These will be done in the main runner
        run two instances that are as different as possible 
        then compare with others to get an approximation of their fitness
Something to be aware of is right now duck and jump are super different when calcing difference
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
        similarity(other):
            compare two individuals and quantify how similar the are

    Attributes:
        strategy: integer encoding of when an action will be taken
        fitness: a value based on how well an individual would do in the game 
        size: size of strategy array 
    """
    def __init__(self, size=8, arr=None):
        """Creating a random initial individual

        Parameters
            arr: copied strategy passed in 

        scenarios that can occur are:
            0 - small cactus
            1 - big cactus 
            2 - double cactus
            3 - high ptera
            4 - low ptera
            TODO: Validate that this is exhaustive

        """
        self.size = size
        self.fitness = 0
        if arr is None:
            self.strategy = numpy.array([random.randint(-50, 50) for x in range(self.size)])
            for s in range(len(self.strategy)):
                if self.strategy[s] == 0:
                    self.strategy[s] = 1
        else:
            self.strategy = arr
    def __str__(self):
        """Overwritten string representation
        """

        string = "["

        for i in self.strategy:
            string += " " + str(i)
        
        string += "]"

        string += " " + str(self.fitness)

        return string          

    def _copy(self):
        """Private method that returns a copy of the individual

        Returns:
            Copy of individual with same stategy
        """
        b = numpy.zeros(self.size, dtype=numpy.int64)

        numpy.copyto(b, self.strategy)

        return Individual(size=self.size, arr=b)

    def mutate(self):
        """Mutates a single point of the strategy within the interval of -5 and +5


        Returns:
            copy: a mutated individual 
        """
        to_mutate = self._copy()

        point = random.randint(0, self.size-1)

        to_mutate.strategy[point] = random.randint(-50, 50)

        return to_mutate

    def crossover(self, other):
        """crosses over two individuals

        Parameters:
            other: another individual to cross with 

        Returns:
            this_crossover, other_crossover: two new crossed individuals 
        """
        other_crossover = other._copy() # Need to fix scoping
        this_crossover = self._copy()

        point = random.randint(1, self.size)

        temp = numpy.zeros(self.size - point, dtype=numpy.int64)
        numpy.copyto(temp,this_crossover.strategy[point:])

        this_crossover.strategy[point:] = other_crossover.strategy[point:]
        other_crossover.strategy[point:] = temp

        return this_crossover, other_crossover

    def fitness_approx(self, other):
        """Take in a second individual and call private similarity function to
        generate an approximate fitness

        :param other: Referential Individual
        :return:
        """
        return other.fitness * self.similarity(other)

    def similarity(self, other):
        """
        Private: gives the average similarity in percentage between two individuals
        :param other: the other individual to be compared to
        :return:
        """
        sim = 0
        for index in range(self.size):
            sim += (abs(self.strategy[index]/other.strategy[index] if other.strategy[index] else 0))
        sim /= self.size
        if sim > 1:  # Over 100% doesn't mean better
            return 2 - sim
        else:
            return sim


if __name__ == "__main__":
    one = Individual()
    two = Individual()

    f,t = one.crossover(two)