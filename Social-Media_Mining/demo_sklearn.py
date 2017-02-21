#!/usr/bin/python3.5
# -*-coding:utf-8-*-


from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Load the data
iris = datasets.load_iris()
X = iris.data

petal_length = X[:,2]
petal_width = X[:,3]
# print petal_length,type(petal_length)
# print petal_width, type(petal_width)
true_labels = iris.target
# print(true_labels)

# Apply KMeans clustering
estimator = KMeans(n_clusters=3)
estimator.fit(X)
predicted_labels = estimator.labels_

# Color Scheme definition: red, yellow and blue
color_scheme = ['r', 'y', 'b']

# Markers definition: circle, "x" and "plus"
marker_list = ['o', 'x', '+']

# Assign colors/markers to the predicted labels
colors_predicted_labels = [color_scheme[lab] for lab in predicted_labels]
markers_predicted = [marker_list[lab] for lab in predicted_labels]

colors_true_labels = [color_scheme[lab] for lab in true_labels]
markers_true = [marker_list[lab] for lab in true_labels]


# Plot and save the two scatter plots
for x, y, c, m in zip(petal_length, petal_width, colors_predicted_labels, markers_predicted):
    plt.scatter(x, y, c=c, marker=m)
    plt.savefig('iris_predicted_labels.png')

for x, y, c, m in zip(petal_length, petal_width, colors_true_labels, markers_true):
    plt.scatter(x, y, c=c, marker=m)
    plt.savefig('iris_true_labels.png')

