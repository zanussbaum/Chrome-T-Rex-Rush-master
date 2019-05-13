import random
import numpy


def fit_function(difference):
    return 0.24 * numpy.exp((-(difference - 59)**2) / 1152)


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

        """
        self.size = size
        self.fitness = 0
        self.death_scenario = -1
        self.jumped_too_early = None
        if arr is None:
            self.strategy = numpy.random.uniform(low=1.0, high=556.0,size=self.size)
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

        return string

    def __repr__(self):
        """Overwritten representation of object
        """
        return self.__str__()

    def __eq__(self, other):
        """Overwritten equality 
        """
        return numpy.array_equal(self.strategy, other.strategy)

    def __ne__(self,other):
        return not self.__eq__(other)

    def __key(self):
        """
        """
        return tuple(self.strategy)

    def __hash__(self):
        """
        """
        return hash(self.__key())
      
    def __sub__(self, other):
        """Overwritten subtraction method
        """
        return numpy.linalg.norm(numpy.subtract(numpy.absolute(self.strategy),numpy.absolute(other.strategy)))
                 
    def __copy(self):
        """Private method that returns a copy of the individual

        Returns:
            Copy of individual with same strategy
        """
        b = numpy.zeros(self.size, dtype=numpy.float64)

        numpy.copyto(b, self.strategy)

        return Individual(size=self.size, arr=b)

    def mutate(self):
        """Mutates a single point of the strategy within the interval of 1 and 556

        Returns:
            copy: a mutated individual 
        """
        to_mutate = self.__copy()

        point = random.randint(0, self.size-1)

        to_mutate.strategy[point] = random.randint(1, 556)

        return to_mutate

    def crossover(self, other):
        """crosses over two individuals

        Parameters:
            other: another individual to cross with 

        Returns:
            this_crossover, other_crossover: two new crossed individuals 
        """
        other_crossover = other.__copy()
        this_crossover = self.__copy()

        point = random.randint(0, self.size)
        if point + 1 > self.size:
            other_point = self.size
        else:
            other_point = random.randint(point + 1, self.size)

        temp = numpy.zeros(other_point - point, dtype=numpy.float64)
        numpy.copyto(temp, this_crossover.strategy[point:other_point])

        this_crossover.strategy[point:other_point] = other_crossover.strategy[point:other_point]
        other_crossover.strategy[point:other_point] = temp

        return this_crossover, other_crossover

    def fitness_approx(self, other):
        """Take in a second individual and call private similarity function to
        generate an approximate fitness

        :param other: Referential Individual
        :return:
        """
        if other.death_scenario != -1:
            dif = other.strategy[other.death_scenario] - self.strategy[other.death_scenario]
            sim_val = fit_function(abs(dif))
            if other.jumped_too_early:
                if dif > 0:
                    return other.fitness * (1 + sim_val)
                else:
                    return other.fitness * (1 - sim_val)
            else:
                if dif < 0:
                    return other.fitness * (1 + sim_val)
                else:
                    return other.fitness * (1 - sim_val)
        return other.fitness * self.similarity(other)

    def similarity(self, other):
        """
        Private: gives the average similarity in percentage between two individuals
        :param other: the other individual to be compared to
        :return:
        """
        difference = other - self
        norm = numpy.linalg.norm(other.strategy)

        return difference/norm


if __name__ == "__main__":
    one = Individual()
    two = Individual()
    f, t = one.crossover(two)