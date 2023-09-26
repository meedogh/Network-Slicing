

from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import pickle
import matplotlib.pyplot as plt

path =  "C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/action_each_single_request_reward_method4_add_init_10_11_12_no_protrization_less_failure_less_reward_2_test/states_of_memory/states_of_memory_path0.pkl"
# X = np.array().reshape(len(x1), 2)
deque =[ ]
with open(path, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

X_ =  np.array(deque)
print(X_.shape)
X =  np.array(deque).reshape(X_.shape[1],4)

print(X.shape)
distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 10)

for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)

    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X.shape[0])
    inertias.append(kmeanModel.inertia_)

    mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                   'euclidean'), axis=1)) / X.shape[0]
    mapping2[k] = kmeanModel.inertia_


plt.plot(K, distortions, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.savefig("number of clusters.svg", format="svg")

plt.show()