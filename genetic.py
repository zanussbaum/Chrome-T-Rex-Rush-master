from individual import Individual


def det_testers(individuals):
    max_diff = 100
    species1 = None
    species2 = None
    for ind1 in individuals:
        for ind2 in individuals:
            if ind1 != ind2:
                sim = ind1.similarity(ind2)
                if sim < max_diff:
                    max_diff = sim
                    species1 = ind1
                    species2 = ind2
    return species1, species2

def run_game(species):
    # So basically copy the main and change user to automated based on strategy
    # Play the game according to the strategy and assign fitness on death

def main():
    population = 20
    individuals = [population]
    for spec in range(population):
        individuals[spec] = Individual()
    species1, species2 = det_testers(individuals)
    run_game(species1)
    run_game(species2)
    for ind in individuals:
        if ind != species1 and ind != species2:
            ind.fitness = (ind.fitness_approx(species1) + ind.fitness_approx(species2))/2
    #Crossover and Mutation

if __name__ == "__main__":
    main()
