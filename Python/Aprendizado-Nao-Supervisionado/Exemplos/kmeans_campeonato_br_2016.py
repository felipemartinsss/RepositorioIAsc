#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:11:25 2017

@author: felipemartinsss
"""

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

# Pontuacao dos times no Campeonato Brasileiro de 2016.
inputs = [[80],[71],[71],[62],[59],[57],[55],[53],[53],[52],
          [52],[51],[50],[47],[46],[45],[43],[37],[31],[28]]
          
colors = [
          "#FF0000", 
          "#00FF00",
          "#0000FF",
          "#00FFFF",
          "#FFFF00",
          "#FF00FF",
          "#800000",
          "#008000",
          "#000080",
          "#800080",
          "#808000",
          "#800080",
          "#008080",
          "#F00000",
          "#0F0000",
          "#00F000",
          "#000F00",
          "#0000F0",
          "#00000F",
          "#FFF000",
          "#000FFF"
          ]

# Executa o k-means com k = 5 sobre a pontuação dos times no campeonato.
kmeans = KMeans(n_clusters = 5, random_state = 0).fit(inputs)
print "KMeans - Scikit-Learn"
print "Labels"
print kmeans.labels_
print "Cluster centers:"
print kmeans.cluster_centers_

plt.axis([0, 100, 2010, 2020])
plt.title("k-means sobre pontuacao do campeonato brasileiro de 2016")
plt.ylabel("Ano")
plt.xlabel("Pontuacao do Time")

# Apresenta em modo gráfico a distribuição dos times pelos clusters.
for i in range(0, len(inputs)):
    color_idx = int(kmeans.labels_[i])
    plt.scatter(inputs[i], [2016], color=colors[color_idx])
    
plt.show()


