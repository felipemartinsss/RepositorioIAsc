import sys
import csv
from math import sqrt
from math import pow

# Dada uma matriz e um valor, encontra as coordenadas (i,j) 
# que contenham o valor procurado.
def encontraPosicoes (matriz, M, N, valor):
	posicoes = []
	for i in range(0, M):
		for j in range(0, N):
			if matriz[i][j] == valor:
				posicoes.append((i, j))
	return posicoes

# Dada uma matriz e a posicao atual pelas coordenadas (i,j), 
# encontra os estados sucessores com 1 passo de (i,j)
def encontra_estados_sucessores (matriz, M, N, posicao_atual):
	i = posicao_atual[0]
	j = posicao_atual[1]
	estados_sucessores = []
	if i > 0 and matriz[i-1][j] != '2': # Move para cima na matriz.
		estados_sucessores.append ((i-1, j))
	if i+1 < M and matriz[i+1][j] != '2': # Move para baixo na matriz.
		estados_sucessores.append ((i+1, j))
	if j > 0 and matriz[i][j-1] != '2': # Move para esquerda na matriz.
		estados_sucessores.append ((i, j-1))
	if j+1 < N and matriz[i][j+1] != '2': # Move para direita na matriz.
		estados_sucessores.append ((i, j+1))
	if j > 0 and i > 0 and matriz[i-1][j-1] != '2': # Move diagonalmente para esq sup.
		estados_sucessores.append ((i-1, j-1))
	if j > 0 and i+1 < M and matriz[i+1][j-1] != '2': # Move diagonalmente para esq inf.
		estados_sucessores.append ((i+1, j-1))
	if j+1 < N and i > 0 and matriz[i-1][j+1] != '2': # Move diagonalmente para dir sup.
		estados_sucessores.append ((i-1, j+1))
	if j+1 < N and i+1 < M and matriz[i+1][j+1] != '2': # Move diagonalmente para dir inf.
		estados_sucessores.append ((i+1, j+1))
	return estados_sucessores

# Dado um estado considerado final, uma lista de predecessores e um numero de iteracao,
# apresenta em qual iteracao foi encontrada a solucao e como partir do estado inicial 
# e chegar ate o estado final a partir da solucao parcial armazenada em predecessores.
def apresenta_solucao (estado, predecessores, iteracao):
	caminho = []
	caminho.append(estado)
	print "Solucao encontrada na iteracao " + str(iteracao) + ":"
	while predecessores[estado] != None:
		caminho.append(predecessores[estado])
		estado = predecessores[estado]
	caminho = caminho[::-1]
	print caminho

# Dado um estado qualquer e um conjunto de estados finais, 
# calcula a distancia do estado qualquer ate um estado final mais proximo.
def calcula_distancia_meta (estado, estados_finais):
	x = estado[0]
	y = estado[1]
	distancia_minima = 1000000000

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		diff1 = x_estado_final - x
		diff2 = y_estado_final - y
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		if distancia_atual < distancia_minima:
			distancia_minima = distancia_atual
	return distancia_minima

# Dada uma franja (fringe) e uma funcao heuristica, 
# encontra o estado com menor valor nessa franja.
def encontra_estado_mais_promissor (franja, heuristica_estados):
	valor_mais_promissor = 1000000000
	estado_mais_promissor = None
	indice_mais_promissor = 0
	indice = 0
	for estado in franja:
		if heuristica_estados[estado] < valor_mais_promissor:
			estado_mais_promissor = estado
			valor_mais_promissor = heuristica_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

# Dada uma fila com alguns estados, apresenta cada um deles.
def mostra_estados_fila (fila):
	print "==================================="
	print "Estados para analisar"
	for estado in fila:
		print str(estado)
	print "==================================="

# Dada uma franja (fringe) com alguns estados, apresenta o valor heuristico 
# de cada um deles.
def mostra_valores_franja (franja, heuristica):
	print "==================================="
	print "Valores da franja"
	for estado in franja:
		print "V_" + str(estado) + " = " + str(heuristica[estado])
	print "==================================="

# Algoritmo: Busca em Largura (Breadth-First Search)
# Dada uma matriz, um estado inicial e estados finais, define um conjunto de acoes para alcancar um dos estados finais.
def busca_em_largura (matriz, M, N, estado_inicial, estados_finais):
	estados_visitados = []
	estados_expandidos = []
	profundidade_estados = {}
	predecessores = {}
	solucao_encontrada = False
	print "Algoritmo: Busca em Largura"
	estados_visitados.append(estado_inicial)
	profundidade_estados[estado_inicial] = 0
	predecessores[estado_inicial] = None
	iteracao = 1
	while len(estados_visitados) != 0:
		# mostra_estados_fila (estados_visitados) # Mostra a fila do algoritmo em cada iteracao.
		estado = estados_visitados.pop(0)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores (matriz, M, N, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in estados_visitados:
					estados_visitados.append(estados_sucessores[i])
					profundidade_estados[estados_sucessores[i]] = profundidade_estados[estado] + 1
					predecessores[estados_sucessores[i]] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao (estado, predecessores, iteracao)
	else:
		print "Nao foi possivel encontrar uma solucao para o problema."

# Algoritmo: Busca A* (A Estrela / A Star)
def busca_a_estrela (matriz, M, N, estado_inicial, estados_finais):
	distancia_meta = {}
	distancia_percorrida = {}
	heuristica = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False

	print "Algoritmo: A* (A Estrela)"

	# Inicializacao de distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	distancia_meta[estado_inicial] = calcula_distancia_meta (estado_inicial, estados_finais) 
	heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_meta[estado_inicial]
	predecessores[estado_inicial] = None
	print "Heuristica da Distancia no Estado Inicial: " + str(heuristica[estado_inicial])
	franja = []
	franja.append(estado_inicial)
	iteracao = 1
	while len(franja) != 0:
		# mostra_valores_franja (franja, heuristica)
		indice_mais_promissor = encontra_estado_mais_promissor(franja, heuristica)
		estado = franja.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, M, N, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in franja:
				franja.append(sucessor)
				if sucessor not in heuristica.keys():
					distancia_meta[sucessor] = calcula_distancia_meta(sucessor, estados_finais)
					distancia_percorrida[sucessor] = distancia_percorrida[estado] + 1
					heuristica[sucessor] = distancia_meta[sucessor] + distancia_percorrida[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao (estado, predecessores, iteracao)
	else:
		print "Nao foi possivel encontrar uma solucao para o problema."

# Fluxo principal do program em Python.
# Inspirado no problema 'Duende Perdido' da Olimpiada Brasileira de Informatica de 2005 - OBI 2005.
if len(sys.argv) == 2:
	problema = open(sys.argv[1]) # Chame o problem com: python buscas_ia.py data/duende_perdido_1.csv
	leitor_problema = csv.reader (problema)
	entrada = list(leitor_problema)
	M = int(entrada[0][0]) # numero de linhas.
	N = int(entrada[0][1]) # numero de colunas.
	matriz = entrada[1:] # mapa representado como matriz.

	estado_inicial = encontraPosicoes (matriz, M, N, '3')
	estados_finais = encontraPosicoes (matriz, M, N, '0')
	print "Matriz (mapa): "
	print str(matriz)
	print "Estado Inicial: " + str(estado_inicial)
	print "Estado Final: " + str(estados_finais)
	busca_em_largura (matriz, M, N, estado_inicial[0], estados_finais)
	busca_a_estrela (matriz, M, N, estado_inicial[0], estados_finais)
else:
	print "Forneca um arquivo CSV para os algoritmos de busca."