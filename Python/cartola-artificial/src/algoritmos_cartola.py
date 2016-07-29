#!/usr/bin/env python
#!-*- coding: utf-8 -*-

import algoritmos_cartola as algoritmo
import conversor_json_ed as conversor
import csv
import json
import leitor_json as leitor
import logging
import matematica_cartola as mat_cartola
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sys
import utilitarios_cartola as util
import view
import pdb

# Log Debug
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# Log Info
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
# Log Critical
#logging.basicConfig(level=logging.CRITICAL, format=' %(asctime)s - %(levelname)s - %(message)s')



def convoca_aleatoriamente_por_posicao (cartoletas_posicao, conteudo_csv, num_jogadores, posicao, info):
	jogadores_convocados = []
	cartoletas_por_jogador = cartoletas_posicao

	jogadores_por_posicao = util.obtem_jogadores_por_posicao(conteudo_csv, posicao, info)

	indices_jogadores_sorteados = []

	while num_jogadores > 0:

		idx_jogador_sorteado = random.randint(0, len(jogadores_por_posicao) - 1)
		jogador_sorteado = jogadores_por_posicao[idx_jogador_sorteado]
		preco_jogador_sorteado = float(jogador_sorteado[info["preco"]])

		tentativas = 0
		while (preco_jogador_sorteado > cartoletas_por_jogador) or (idx_jogador_sorteado in indices_jogadores_sorteados):
			idx_jogador_sorteado = random.randint(0, len(jogadores_por_posicao) - 1)
			jogador_sorteado = jogadores_por_posicao[idx_jogador_sorteado]
			preco_jogador_sorteado = jogador_sorteado[info["preco"]]
			tentativas += 1
			if tentativas == 100:
				break

		if tentativas != 100:
			indices_jogadores_sorteados.append(idx_jogador_sorteado)
			jogadores_convocados.append(jogador_sorteado)
			num_jogadores -= 1
		else:
			falha = []
			return falha

	return jogadores_convocados



def get_pior_jogador_posicao (jogadores_posicao, info):
	if len(jogadores_posicao) >= 1 and jogadores_posicao[0] != 0:
		medias_jogadores = {}
		for jogador in jogadores_posicao:
			medias_jogadores[jogador[info["media"]]] = jogador
		chave_pior_jogador = min(medias_jogadores)
		pior_jogador = medias_jogadores[chave_pior_jogador]
		return pior_jogador
	else:
		return None


def convoca_por_posicao (cartoletas_posicao, conteudo_csv, num_jogadores, posicao, info):

	jogadores_convocados = []
	cartoletas_por_jogador = float(cartoletas_posicao)

	jogadores_por_posicao = util.obtem_jogadores_por_posicao(conteudo_csv, posicao, info)
	# print jogadores_por_posicao
	dicionario_jogadores = {}
	for j in jogadores_por_posicao:
		dicionario_jogadores[j[2]] = j

	lista_jogadores_ordenados = sorted(dicionario_jogadores, reverse=True)
	# print lista_jogadores_ordenados
	for j in lista_jogadores_ordenados:
		jogador = dicionario_jogadores[j]
		if jogador[1] < cartoletas_por_jogador:
			# print dicionario_jogadores[j]
			jogadores_convocados.append(dicionario_jogadores[j])
			num_jogadores -= 1
			if num_jogadores == 0:
				break
	return jogadores_convocados

def gera_populacao_inicial (tamanho, cartoletas, conteudo_csv, formacao, info):
	populacao = []
	while len(populacao) < tamanho:
		if len(populacao) <= 0.25 * tamanho:
			time_convocado = algoritmo_balanceado ("Balanceado", cartoletas, conteudo_csv, formacao, info)
		elif len(populacao) <= 0.50 * tamanho:
			time_convocado = algoritmo_balanceado_V2 ("Balanceado V2", cartoletas, conteudo_csv, formacao, info)
		elif len(populacao) <= 0.75 * tamanho:
			time_convocado = algoritmo_aleatorio ("Aleatorio", cartoletas, conteudo_csv, formacao, info)	
		elif len(populacao) <= tamanho:
			time_convocado = algoritmo_estrela_solitaria("Estrela Solitaria", cartoletas, conteudo_csv, formacao, info)
		#elif len(populacao) <= tamanho:
		#	time_convocado = algoritmo_selecao_brasileira("Selecao da Rodada", cartoletas, conteudo_csv, formacao)
		populacao.append(time_convocado)
	return populacao

def cruzamento (time_A, time_B, cartoletas, info):

	if time_A != time_B:
		# pdb.set_trace()
		logging.debug ("Time A: {0}".format(time_A))
		logging.debug ("Time B: {0}".format(time_B))

		qtde_posicoes_time = len(time_A) # num. setores
		#logging.debug("Posicoes Time A: {0}".format(qtde_posicoes_time))

		idx_posicao = random.randint(0, qtde_posicoes_time - 1) # indice de um setor (goleiro/zaga/meias/etc)

		qtde_jogadores_posicao = len(time_A[idx_posicao]) # numero de jogadores do setor

		idx_jogador = random.randint(0, qtde_jogadores_posicao - 1) # um jogador no setor.

		while idx_posicao < qtde_posicoes_time: # para cada um dos setores do time		
			posicoes_no_time_A = time_A[idx_posicao]
			qtde_jogadores_posicao = len(posicoes_no_time_A) # numero de jogadores do setor
			logging.debug ("qtde_jogadores_posicao = {0}".format(qtde_jogadores_posicao))
			logging.debug ("Posicoes no time A: {0}".format(posicoes_no_time_A))
			logging.debug ("idx_posicao = {0}".format(idx_posicao))
			posicoes_no_time_B = time_B[idx_posicao]
			logging.debug ("Posicoes no time B: {0}".format(posicoes_no_time_B))
			while idx_jogador < qtde_jogadores_posicao: # para cada um dos jogadores do setor
				jogador = posicoes_no_time_A[idx_jogador]
				if jogador not in posicoes_no_time_B:
					preco_jogador = jogador[info["preco"]]
					preco_time_B = mat_cartola.get_valor_indice_acumulado_time(time_B, info, "preco")
					jogador_anterior_B = posicoes_no_time_B[idx_jogador]
					preco_jogador_anterior_B = jogador_anterior_B[info["preco"]]
					if preco_time_B - preco_jogador_anterior_B + preco_jogador < cartoletas:
						media_jogador = jogador[info["media"]]
						media_jogador_anterior = jogador_anterior_B[info["media"]]
						if media_jogador > media_jogador_anterior:
							posicoes_no_time_B[idx_jogador] = jogador
							time_B[idx_posicao] = posicoes_no_time_B
				idx_jogador += 1
			time_B[idx_posicao] = posicoes_no_time_B
			idx_posicao += 1
			idx_jogador = 0
		
	return time_B

def mutacao_genetica (filho_AB, cartoletas, conteudo_csv, limiar_mutacao, info):

	# Mutacao Genetica
	# pdb.set_trace()
	idx_posicao_mutacao = random.randint(0, len(filho_AB) - 1)
	setor_antigo = filho_AB[idx_posicao_mutacao]
	idx_jogador_mutacao = random.randint(0, len(setor_antigo) - 1)
	jogador_antigo = setor_antigo[idx_jogador_mutacao]
	while jogador_antigo == 0:
		idx_posicao_mutacao = random.randint(0, len(filho_AB) - 1)
		setor_antigo = filho_AB[idx_posicao_mutacao]
		idx_jogador_mutacao = random.randint(0, len(setor_antigo) - 1)
		jogador_antigo = setor_antigo[idx_jogador_mutacao]

	logging.debug("Cartoletas: {0}".format(cartoletas))
	custo_filho_AB = mat_cartola.get_valor_indice_acumulado_time(filho_AB, info, "preco")
	logging.debug("Custo filho_AB: {0}".format(custo_filho_AB))
	custo_filho_AB -= jogador_antigo[1]
	logging.debug("Custo filho_AB - Custo Jogador Antigo: {0}".format(custo_filho_AB))
	cartoletas_mutacao = cartoletas - custo_filho_AB
	logging.debug("Cartoletas para mutaçao: {0}".format(cartoletas_mutacao))

	if cartoletas_mutacao > 0:
		posicao = jogador_antigo[4]
		jogador_novo = jogador_antigo
		while jogador_antigo == jogador_novo or jogador_novo in setor_antigo:
			jogador_novo = convoca_aleatoriamente_por_posicao (cartoletas_mutacao, conteudo_csv, 1, posicao, info)
			if len(jogador_novo) > 1:
				jogador_novo = jogador_novo[0]
				if jogador_novo in setor_antigo:
					continue
			else:
				jogador_novo = jogador_antigo
				break

		setor_novo = setor_antigo
		setor_novo[idx_jogador_mutacao] = jogador_novo
		filho_AB[idx_posicao_mutacao] = setor_novo
	return filho_AB

def algoritmo_genetico (nome, cartoletas, conteudo_csv, formacao, limite_inferior, info):
	populacao = []
	nova_populacao = []
	probabilidade_continuidade = {}
	soma_medias = 0.0
	limiar_mutacao = 0.01
	tamanho_populacao = 4000 # PRD
	# tamanho_populacao = 2000 # QA
	# tamanho_populacao = 1000
	mutacoes_ocorridas = 0
	geracoes = 20 # PRD
	#geracoes = 10 # QA
	geracoes = 10
	geracao_atual = 1
	cartoletas_por_jogador = cartoletas / (12.0)
	time_campeao = []

	logging.debug ("Calculando geraçao 0 para formacao {0}".format(formacao))
	populacao = gera_populacao_inicial(tamanho_populacao, cartoletas, conteudo_csv, formacao, info)

	medias_times_populacao = [0] * tamanho_populacao
	logging.debug(medias_times_populacao)

	while geracao_atual <= geracoes and max(medias_times_populacao) <= limite_inferior:
		logging.info("Calculando geraçao {0} para formacao {1}".format(geracao_atual, formacao))
		logging.debug("		max(medias_times_populacao) = {0}".format(max(medias_times_populacao)))

		soma_medias = 0.0
		medias_times_populacao = [0] * len(populacao)
		probabilidade_continuidade = [0] * len(populacao)
		pontuacao_por_time = {}

		for id_time_convocado in range(0, len(populacao)):
			time_convocado = populacao[id_time_convocado]
			medias_times_populacao[id_time_convocado] = mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "media")
			soma_medias += medias_times_populacao[id_time_convocado]
			pontuacao_por_time[medias_times_populacao[id_time_convocado]] = id_time_convocado

		logging.debug(medias_times_populacao)

		for id_time_convocado in range(0, len(populacao)):
			probabilidade_continuidade[id_time_convocado] = medias_times_populacao[id_time_convocado] / soma_medias

		probabilidade_continuidade_cumulativa = {}

		probabilidade_continuidade_cumulativa[0] = probabilidade_continuidade[0]
		for id_time_convocado in range(1, len(populacao)):
			probabilidade_continuidade_cumulativa[id_time_convocado] = probabilidade_continuidade_cumulativa[id_time_convocado - 1] + probabilidade_continuidade[id_time_convocado]

		
		nova_populacao = []

		# Seleçao Natural
		while len(nova_populacao) < len(populacao):
			num_sorteio_time_A = mat_cartola.get_id_time_probabilidade_cumulativa (probabilidade_continuidade_cumulativa)
			num_sorteio_time_B = num_sorteio_time_A
		
			while num_sorteio_time_A == num_sorteio_time_B:
				num_sorteio_time_B = mat_cartola.get_id_time_probabilidade_cumulativa (probabilidade_continuidade_cumulativa)

			logging.debug("Cruzamento entre times dos indices {0} e {1}.".format(num_sorteio_time_A, num_sorteio_time_B))
			time_A = populacao[num_sorteio_time_A]
			time_B = populacao[num_sorteio_time_B]
			filho_AB = cruzamento(time_A, time_B, cartoletas, info)

			probabilidade_mutacao = random.random()
			if probabilidade_mutacao < limiar_mutacao:
				filho_AB = mutacao_genetica (filho_AB, cartoletas, conteudo_csv, limiar_mutacao, info)
				mutacoes_ocorridas += 1

			nova_populacao.append(filho_AB)

		populacao = nova_populacao
		geracao_atual += 1
		logging.debug ("Medias geracao: {0}".format(medias_times_populacao))
		idx_time_campeao = pontuacao_por_time[max(medias_times_populacao)]
		logging.debug("idx_time_campeao = {0}".format(idx_time_campeao))
		time_campeao = populacao[idx_time_campeao]
		

	soma_medias = 0.0
	medias_times_populacao = [0] * len(populacao)
	probabilidade_continuidade = [0] * len(populacao)
	pontuacao_por_time = {}

	for id_time_convocado in range(0, len(populacao)):
		time_convocado = populacao[id_time_convocado]
		medias_times_populacao[id_time_convocado] = mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "media")
		soma_medias += medias_times_populacao[id_time_convocado]
		pontuacao_por_time[medias_times_populacao[id_time_convocado]] = id_time_convocado

	logging.debug("Ultima geracao: {0}".format(geracao_atual))
	logging.debug("Mutacoes ocorridas: {0}".format(mutacoes_ocorridas))
	# logging.info("Medias geracao: {0}".format(medias_times_populacao))
	logging.info(max(medias_times_populacao))

	# logging.debug ("Medias geracao: {0}".format(medias_times_populacao))
	idx_time_campeao = pontuacao_por_time[max(medias_times_populacao)]
	logging.debug("idx_time_campeao = {0}".format(idx_time_campeao))
	time_campeao = nova_populacao[idx_time_campeao]
	logging.debug("Time campeao do AG para formacao {0} possui media {1}: {2}".format(formacao, mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "media"), time_campeao))
	return time_campeao



def algoritmo_estrela_solitaria(nome, cartoletas, conteudo_csv, formacao, info):
	time_convocado = []
	jogadores_por_setor = formacao.split("-")
	posicoes = [1, 2, 3, 4, 5, 6]
	num_jogadores_pos = util.get_num_jogadores_pos(formacao)
	custo_jogadores_pos = {}

	logging.debug ("Length posicoes: {0}".format(len(posicoes)))
	posicao_sorteada_estrela = random.randint(1, len(posicoes) - 1)

	while num_jogadores_pos[posicao_sorteada_estrela] == 0:
		posicao_sorteada_estrela = random.randint(1, len(posicoes) - 1)

	jogador_convocado = convoca_por_posicao (cartoletas, conteudo_csv, 1, posicao_sorteada_estrela, info)[0]
	num_jogadores_pos[posicao_sorteada_estrela] -= 1

	cartoletas_estrela = jogador_convocado[info["preco"]]
	cartoletas_restantes = cartoletas - cartoletas_estrela
	logging.debug("Jogador convocado: {0}".format(jogador_convocado))
	logging.debug("Cartoletas restantes: {0}".format(cartoletas_restantes))

	cartoletas_por_jogador = cartoletas_restantes / 11.0

	for p in posicoes:
		custo_jogadores_pos[p] = num_jogadores_pos[p] * cartoletas_por_jogador
		if num_jogadores_pos[p] != 0:
			jogadores_convocados_pos = convoca_por_posicao(custo_jogadores_pos[p] / num_jogadores_pos[p], conteudo_csv, num_jogadores_pos[p], p, info)
			time_convocado.append(jogadores_convocados_pos)
		else:
			time_convocado.append([0])
		

	setor_jogador_estrela = time_convocado[posicao_sorteada_estrela - 1]
	logging.debug("Setor do jogador estrela: {0}".format(setor_jogador_estrela))
	if len(setor_jogador_estrela) == 1 and setor_jogador_estrela[0] == 0:
		setor_jogador_estrela[0] = jogador_convocado
	else:
		setor_jogador_estrela.append(jogador_convocado)
	time_convocado[posicao_sorteada_estrela - 1] = setor_jogador_estrela
	
	logging.debug("Time_convocado por Estrela Solitaria: {0}".format(time_convocado))

	logging.debug("Custo do time {0}".format(mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "preco")))
	logging.debug("Media do time {0}".format(mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "media")))

	return time_convocado

def algoritmo_aleatorio (nome, cartoletas, conteudo_csv, formacao, info):
	cartoletas_por_jogador = cartoletas / (11.0 + 1.0)
	time_convocado = []
	jogadores_por_setor = formacao.split("-")
	# Goleiro, Laterais, Zagueiros, Meias, Atacantes, Tecnico
	posicoes = [1, 2, 3, 4, 5, 6]
	num_jogadores_pos = util.get_num_jogadores_pos(formacao)
	custo_jogadores_pos = {}

	for p in posicoes:
		custo_jogadores_pos[p] = num_jogadores_pos[p] * cartoletas_por_jogador
		if num_jogadores_pos[p] != 0:
			jogadores_convocados_pos = convoca_aleatoriamente_por_posicao (custo_jogadores_pos[p] / num_jogadores_pos[p], conteudo_csv, num_jogadores_pos[p], p, info)
			time_convocado.append(jogadores_convocados_pos)
		else:
			time_convocado.append([0])

	return time_convocado



def algoritmo_balanceado (nome, cartoletas, conteudo_csv, formacao, info):
	cartoletas_por_jogador = cartoletas / (11.0 + 1.0)
	# print ("Voce pode gastar ate {0} por jogador.".format(cartoletas_por_jogador))
	time_convocado = []
	
	# Goleiro, Laterais, Zagueiros, Meias, Atacantes, Tecnico
	posicoes = [1, 2, 3, 4, 5, 6]	
	num_jogadores_pos = util.get_num_jogadores_pos(formacao)
	custo_jogadores_pos = {}
	
	for p in posicoes:
		custo_jogadores_pos[p] = num_jogadores_pos[p] * cartoletas_por_jogador
		if num_jogadores_pos[p] != 0:
			jogadores_convocados_pos = convoca_por_posicao(custo_jogadores_pos[p] / num_jogadores_pos[p], conteudo_csv, num_jogadores_pos[p], p, info)
			time_convocado.append(jogadores_convocados_pos)
		else:
			time_convocado.append([0])
	return time_convocado

def algoritmo_balanceado_V2 (nome, cartoletas, conteudo_csv, formacao, info):
	time_convocado = algoritmo_balanceado (nome, cartoletas, conteudo_csv, formacao, info)
	# logging.info ("Time Balanceado: {0}".format(time_convocado))

	custo_time_balanceado = mat_cartola.get_valor_indice_acumulado_time (time_convocado, info, "preco")
	cartoletas_restantes = cartoletas - custo_time_balanceado
	logging.debug ("Cartoletas restantes: {0}".format(cartoletas_restantes))

	posicoes_validas = 0.0
	for posicoes in time_convocado:
		if len(posicoes) >= 1 and posicoes[0] != 0:
			posicoes_validas += 1.0

	logging.debug ("Posicoes validas: {0}".format(posicoes_validas))
	cartoletas_restantes_posicao = int(cartoletas_restantes / posicoes_validas)
	logging.debug ("Cartoletas por setor: {0}".format(cartoletas_restantes_posicao))

	for posicoes in time_convocado:
		pior_jogador_posicao = get_pior_jogador_posicao(posicoes, info)
		logging.debug ("Setor: {0}".format(posicoes))
		logging.debug ("Pior jogador do setor: {0}".format(pior_jogador_posicao))
		if pior_jogador_posicao != None:
			custo_pior_jogador_posicao = pior_jogador_posicao[info["preco"]]
			posicao_jogador = pior_jogador_posicao[info["posicao"]]
			custo_limite_novo_jogador = custo_pior_jogador_posicao + cartoletas_restantes_posicao
			logging.debug ("Custo limite: {0}".format(custo_limite_novo_jogador))
			jogador_novo_posicao = pior_jogador_posicao
			jogador_novo_posicao = convoca_por_posicao(custo_limite_novo_jogador, conteudo_csv, 1, posicao_jogador, info)
			logging.debug ("Novo jogador do setor: {0}".format(jogador_novo_posicao))
			logging.debug ("Jogador Novo: {0}".format(jogador_novo_posicao))
			idx_jogador_antigo = posicoes.index(pior_jogador_posicao)
			logging.debug ("Idx pior jogador: {0}".format(idx_jogador_antigo))

			if posicoes[idx_jogador_antigo] != jogador_novo_posicao[0] and jogador_novo_posicao[0] not in posicoes:
				posicoes[idx_jogador_antigo] = jogador_novo_posicao[0]

	logging.debug ("Time modificado: {0}".format (time_convocado))
	return time_convocado

def algoritmo_selecao_brasileira (nome, cartoletas, conteudo_csv, formacao, info):
	time_convocado = algoritmo_balanceado (nome, 500.0, conteudo_csv, formacao, info)
	return time_convocado

def get_melhor_formacao_algoritmo(nome, cartoletas, conteudo_csv, formacoes, info, limiar_alg_genetico):
	times_montados = {}
	for formacao in formacoes:	
		logging.debug ("Montando time para formacao {0} usando algoritmo {1}.".format(formacao, nome))
		if nome == "Balanceado":
			time_convocado = algoritmo_balanceado(nome, cartoletas, conteudo_csv, formacao, info)
		elif nome == "Aleatorio":
			time_convocado = algoritmo_aleatorio(nome, cartoletas, conteudo_csv, formacao, info)
		elif nome == "Genetico":
			time_convocado = algoritmo_genetico(nome, cartoletas, conteudo_csv, formacao, limiar_alg_genetico, info)
		elif nome == "Estrela Solitaria":
			time_convocado = algoritmo_estrela_solitaria(nome, cartoletas, conteudo_csv, formacao, info)
		elif nome == "Balanceado V2":
			time_convocado = algoritmo_balanceado_V2 (nome, cartoletas, conteudo_csv, formacao, info)
		elif nome == "Selecao da Rodada":
			time_convocado = algoritmo_selecao_brasileira (nome, cartoletas, conteudo_csv, formacao, info)

		media_time = mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "media")
		times_montados[media_time] = time_convocado
		custo_time = mat_cartola.get_valor_indice_acumulado_time(time_convocado, info, "preco")
		logging.debug ("Media: {0}".format(media_time))
		logging.debug ("Custo: {0}".format(custo_time))
		logging.debug ("###################################################################################")

	media_time_campeao = max(times_montados)
	time_campeao = times_montados[media_time_campeao]
	custo_time_campeao = mat_cartola.get_valor_indice_acumulado_time(time_campeao, info, "preco")

	logging.info ("\n")
	logging.info ("Algoritmo: {0}".format(nome))
	logging.info ("Media do time vencedor: {0}".format(media_time_campeao))
	logging.info ("Custo do time vencedor: {0}".format(custo_time_campeao))
	import view
	view.imprime_time(time_campeao, info)
	logging.info ("\n")
	return time_campeao