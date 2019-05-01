import numpy
from individual import Individual
from random import sample

class KMeans:
    """Rewritten KMeans for Individuals 
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
        """
        centroids = sample(self.dataset,self.k)

        return centroids

    def stopping_condition(self):
        """Stopping condition for the kmeans algorithm
        """
        if self.iterations > self.max_iterations:
            return True
        return self.centroids == self.prev_centroids

    def write_labels(self):
        """Denote a centroid for a each individual 
        """
        labels = {}
        for c in self.centroids:
            labels.update({c:[]})

        self.labels = labels

        for ind in self.dataset:
            difference = [(centroid, abs(ind-centroid)) for centroid in self.centroids]
            centroid = min(difference, key=lambda t: t[1])
            if ind not in self.labels.keys():
                labels = self.labels.get(centroid[0])
                if labels is None:
                    temp = 1
                labels.append(ind)
                self.labels.update({centroid[0]:labels})
            
    def new_centroids(self):
        """Need to figure out how to calculate mean here 
            and then use that to find the new centroids 
        """

        centroids = []

        for cent in self.labels.keys():
            vals = self.labels.get(cent)
            n = len(vals)
            
            if n != 0:
                new_arr = numpy.sum([a.strategy for a in vals], axis=0)
                new_arr = numpy.true_divide(new_arr, n)

                new_ind = Individual(arr=new_arr)
                centroids.append(new_ind)

        self.centroids = centroids


    def run(self):
        """Run kmeans
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

