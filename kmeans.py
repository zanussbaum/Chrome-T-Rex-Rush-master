import numpy
from individual import Individual
from random import sample, choice

class KMeans:
    """KMeans Algorithm for instance Individuals

    Methods:
        random_centroids(): initialize centroids to k random Individuals
        stopping_condition(): boolean that denotes if the stopping condition has been met
        write_labels(): writes the labels for the centroids to individuals 
        new_centroids(): calculates new centroids
        run(): runs the algorithm
    """
    def __init__(self, dataset, k, max_iterations=100):
        self.dataset = dataset
        self.k = k
        self.iterations = 0
        self.max_iterations = max_iterations
        self.labels = {}
        self.centroids = self.random_centroids()
        self.prev_centroids = None


    def random_centroids(self):
        """Initialize centroids to random centers

        Pick k random centers to calculate centroids

        Returns:
            list: random centroids
        """
        centroids = sample(self.dataset,self.k)

        return centroids

    def stopping_condition(self):
        """Stopping condition for the kmeans algorithm

        KMeans stops if it has reached the max 

        Returns:
            boolean: true if the condition has been met
        """
        if self.iterations > self.max_iterations:
            return True
        return self.centroids == self.prev_centroids

    def write_labels(self):
        """Maps individuals to centroids by creating labels

        Creates a mapping of centroids to a list of individuals
        """
        labels = {}
        #error here, maybe empty centroid? 
        for c in self.centroids:
            labels.update({c:[]})

        self.labels = labels

        for ind in self.dataset:
            difference = [(centroid, abs(ind-centroid)) for centroid in self.centroids]
            centroid = min(difference, key=lambda t: t[1])
            if ind not in self.labels.keys():
                labels = self.labels.get(centroid[0])
                labels.append(ind)
                self.labels.update({centroid[0]:labels})
            
    def new_centroids(self):
        """Calculates the new centroids from the given labels

        If a centroid has no points that have it as its label, it
            reassigns the centroid to a random individual in the dataset
        """

        centroids = []

        for cent in self.labels.keys():
            vals = self.labels.get(cent)
            n = len(vals)

            if n != 0:
                new_arr = numpy.sum([a.strategy for a in vals], axis=0)
                new_arr = numpy.true_divide(new_arr, n)
                new_ind = Individual(arr=new_arr)

            #if centroid has no other labels, randomly reinitialize a new centroid
            else:
                new_ind = choice(self.dataset)

            
            centroids.append(new_ind)

        self.centroids = centroids


    def run(self):
        """Run kmeans algorithm

        Returns:
            list, dictionary, list: list of centroids, dictinary of lables, list of closest points to centroids
        """
        # print("original centroids %s" %(self.centroids))
        while not self.stopping_condition():
            # print("iteration %d" %(self.iterations))
            self.iterations += 1
            self.prev_centroids = self.centroids

            self.write_labels()

            self.new_centroids()

        closest_centroids = []

        for centroid in self.centroids:
            diff = [(ind, abs(ind-centroid)) for ind in self.dataset]
            min_ind = min(diff, key=lambda t:t[1])
            # print("the closest centroid for centroid %s in the list is %s" %(centroid, min_ind))
            closest_centroids.append(min_ind[0])

        return self.centroids, self.labels, closest_centroids


if __name__ == '__main__':
    pop = 20

    ind = [None] * pop

    for i in range(len(ind)):
        ind[i] = Individual()
        print("individual %d is %s" %(i, ind[i]))

    kmeans = KMeans(ind, 3)
    centroids, labels, min_ind =  kmeans.run()


    # for c in centroids:
    #     print("centroid: %s" %c)
    
    # print(labels)

    # for c in centroids:
    #     diff = [(i, abs(i-c)) for i in ind]
    #     min_ind = min(diff, key=lambda t:t[1])
    #     print("the closest centroid for centroid %s in the list is %s" %(c, min_ind))

