#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:13:39 2017

@author: felipemartinsss
"""

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Carrega imagem do municipio de São Paulo em um gráfico
import matplotlib.image as mpimg
image = mpimg.imread("img/mapa-municipio-sao-paulo-regioes.png")
plt.imshow(image)

# Pontos indicando cada 1 milhão de pessoas no gráfico.
population = [[90,225],[90,325],[75,90],[125,140],
              [125, 90],[75, 150],[175,150],[125,180],
              [200,125],[225,150],[237, 125],[250,150],]

# Cores a serem utilizadas pelo Matplotlib para apresentar os dados.
colors = [
          "#FF0000", 
          "#00FF00",
          "#0000FF",
          "#FF00FF",
          "#FFFF00",
          "#00FFFF",
          "#800000",
          "#008000",
          "#000080",
          "#800080",
          "#808000",
          "#800080",
          ]
          
color_names = {"#FF0000": "vermelho", "#00FF00": "verde", "#0000FF": "azul"}


plt.title("Distribuicao da Populacao de Sao Paulo por regioes (ficticio)")
plt.xlabel("Longitude ficticia")
plt.ylabel("Latitude ficticia")


for i in range(0, len(population)):
    plt.scatter(population[i][0], population[i][1], color="green")
    
X = np.array(population)

# Executa k-means sobre os pontos onde as pessoas estão concentradas,
# simulacao com k = 3.
kmeans = KMeans(n_clusters = 3, random_state = 0).fit(X)
print "KMeans - Scikit-Learn"
print "Labels"
print kmeans.labels_
print "Cluster centers:"
print kmeans.cluster_centers_

for i in range(0, len(kmeans.cluster_centers_)):
    color_idx = i
    plt.scatter(kmeans.cluster_centers_[i][0], kmeans.cluster_centers_[i][1], color=colors[color_idx], marker="+", s=100)
plt.show()

# Tenta prever a qual cluster pertence determinada pessoa dada sua localização.
osasco_person = [[40, 120]]
cluster_id = kmeans.predict(osasco_person)
print "Morador de Osasco deve ir para hospital: %s" % cluster_id
print "Cor: %s" % color_names[colors[int(cluster_id)]]