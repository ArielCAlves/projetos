# Basic Libs
import pandas as pd
import numpy as np

#Plot Libs
import matplotlib.pyplot as plt

# Clustering and Metrics Libs
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist, pdist
from sklearn.metrics import silhouette_score

# Hiding Warnings Libs
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv(f'datasets/dataset_ML.csv')

df['is_superhost'] = df['is_superhost'].replace(False,0).replace(True,1)
df.drop(columns='ad_id',inplace=True)
print(df.head(1))
print()

pca = PCA(n_components=2).fit_transform(df)
k_range = range(1,12)
k_means_var = [KMeans(n_clusters = k).fit(pca) for k in k_range]
centroids = [X.cluster_centers_ for X in k_means_var]
k_euclid = [cdist(pca, cent, 'euclidean') for cent in centroids]
dist = [np.min(ke, axis=1) for ke in k_euclid]
sum_of_squares_intra_cluster = [sum(d**2) for d in dist]
total_sum = sum(pdist(pca) **2) / pca.shape[0]
sum_of_squares_inter_cluster = total_sum - sum_of_squares_intra_cluster


# Plots in the report
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(k_range, soma_quadrados_inter_clusters/soma_total * 100, 'b*-')
# ax.set_ylim((0,100))
# plt.grid(True)
# plt.xlabel('Number of Clusters')
# plt.ylabel('% of Variance Explained')
# print(plt.title('Variance Explained by Value of K'))


model_v1 = KMeans(n_clusters=4)
model_v1.fit(pca)

h = 0.02
x_min, x_max = pca[:,0].min() - 5, pca[:,0].max() - 1
y_min, y_max = pca[:, 1].min() + 1, pca[:,1].max() + 5
xx, yy = np.meshgrid(np.linspace(x_min, x_max), np.linspace(y_min, y_max))
Z = model_v1.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# plt.figure(1)
# plt.clf()
# plt.imshow(Z,
#            interpolation = 'nearest',
#            extent = (xx.min(), xx.max(), yy.min(), yy.max()),
#            cmap = plt.cm.Paired,
#            aspect = 'auto',
#            origin = 'lower')

labels = model_v1.labels_
print(f"Evaluating the model with the chosen number of clusters: {silhouette_score(pca, labels, metric='euclidean')}")
print()

col_names = []
for col in df.columns:
    col_names.append(col)
    
cluster_map = pd.DataFrame(df, columns=col_names)
cluster_map['cluster'] = model_v1.labels_

print(cluster_map.head())
print()

# clusters in descending order by Mean
print(cluster_map[['cluster','price']].groupby('cluster').mean().sort_values(by='price', ascending=False))
print()

# clusters in descending order by Sum
print(cluster_map[['cluster','price']].groupby('cluster').sum().sort_values(by='price', ascending=False))
print()


#Grouping the data by clusters
cluster_map_0 = cluster_map.loc[cluster_map['cluster']==0]
cluster_map_1 = cluster_map.loc[cluster_map['cluster']==1]
cluster_map_2 = cluster_map.loc[cluster_map['cluster']==2]
cluster_map_3 = cluster_map.loc[cluster_map['cluster']==3]

print(f'Number of Properties in the Cluster 0: {cluster_map_0.shape[0]}')
print()
print(f'Number of Properties in the Cluster 1: {cluster_map_1.shape[0]}')
print()
print(f'Number of Properties in the Cluster 2: {cluster_map_2.shape[0]}')
print()
print(f'Number of Properties in the Cluster 3: {cluster_map_3.shape[0]}')
print()

