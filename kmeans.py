import numpy as np
import matplotlib.pyplot as plt
from individual import Individual
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

color_list = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 
    'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

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
        centroids = np.random.choice(self.dataset,self.k)

        return centroids


    def stopping_condition(self):
        """Stopping condition for the kmeans algorithm

        KMeans stops if it has reached the max 

        Returns:
            boolean: true if the condition has been met
        """
        if self.iterations > self.max_iterations:
            return True
        return np.array_equal(self.centroids,self.prev_centroids)

    def write_labels(self):
        """Maps individuals to centroids by creating labels

        Creates a mapping of centroids to a list of individuals
        """

        labels = {}
        for c in self.centroids:
            labels.update({(c):[]})

        self.labels = labels 


        for ind in self.dataset:
            difference = [(centroid, abs(ind-centroid)) for centroid in self.centroids]
            centroid = min(difference, key=lambda t: t[1])
            if ind not in self.labels.keys():
                labels = self.labels.get((centroid[0]))
                labels.append(ind)
                self.labels.update({centroid[0]:labels})
            
    def new_centroids(self):
        """Calculates the new centroids from the given labels

        If a centroid has no points that have it as its label, it
            reassigns the centroid to a random individual in the dataset
        """

        centroids = set()

        for cent in self.labels.keys():
            vals = self.labels.get(cent)
            n = len(vals)

            if n != 0:
                new_arr = np.sum([a.strategy for a in vals], axis=0)
                new_arr = np.true_divide(new_arr, n)
                new_ind = Individual(arr=new_arr)

            else: 
                new_ind = cent
            
            centroids.add(new_ind)

        self.centroids = centroids


    def run(self):
        """Run kmeans algorithm

        Returns:
            list, dictionary, list: list of centroids, dictinary of lables, list of closest points to centroids
        """
        while not self.stopping_condition():
            self.iterations += 1
            self.prev_centroids = self.centroids

            self.write_labels()

            self.new_centroids()

        closest_centroids = []

        for centroid in self.centroids:
            diff = [(ind, abs(ind-centroid)) for ind in self.dataset]
            min_ind = min(diff, key=lambda t:t[1])
            closest_centroids.append(min_ind[0])

        for i, label in enumerate(self.labels.keys()):
            plt.scatter(label.strategy[0],label.strategy[1],c='black')
            values = self.labels.get(label)
            strategies = [v.strategy for v in values]
            x_values = [x[0] for x in strategies]
            y_values = [y[1] for y in strategies]
            plt.scatter(x_values, y_values,c=color_list[i])

 
        plt.show(block=False)
        plt.pause(3)
        plt.close()

        return self.centroids, self.labels, closest_centroids


if __name__ == '__main__':
    size = 100

    population = [None] * size

    for i in range(size):
        population[i] = Individual()
        print(population[i])


    X = np.array([ind.strategy for ind in population])

    print("these are the indiviual strategies {}".format(X))
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    pca = PCA(n_components=2)


    x = pca.fit_transform(X_scaled)



    pca_pop = [Individual(arr=arr) for arr in x]


    print("these are the strategies after PCA {}".format(x))
    
    kmeans = KMeans(pca_pop, 10)
    centroids, labels, min_ind =  kmeans.run()
    
    l_centroids = [l.strategy for l in centroids]

    revert = scaler.inverse_transform(pca.inverse_transform(l_centroids))

    print("inverted centroids are {}".format(revert))
    print("labels and centroids: {}".format(labels))

    print("there are {} centroids. \n{}".format(len(centroids), centroids))
    

    for i, label in enumerate(labels.keys()):
        plt.scatter(label.strategy[0],label.strategy[1],c='black')
        values = labels.get(label)
        strategies = [v.strategy for v in values]
        x_values = [x[0] for x in strategies]
        y_values = [y[1] for y in strategies]
        plt.scatter(x_values, y_values, c=color_list[i])


    for _,label in labels.items():
        index = np.where(x == label.strategy)
        print(index)


    plt.show()
    # for c in labels:
    #     print(len(labels.get(c)))


