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

# Log Debug
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# Log Info
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
# Log Critical
#logging.basicConfig(level=logging.CRITICAL, format=' %(asctime)s - %(levelname)s - %(message)s')

info = {}
info["apelido"] = 0
info["preco"] = 1
info["media"] = 2
info["clube"] = 3
info["posicao"] = 4
info["em_casa"] = 5
info["clube_id"] = 6
info["clube_adversario_id"] = 7
info["variacao_preco"] = 8
info["pontos_ultima"] = 9
info["percentual_participacao"] = 10
info["media_cartola"] = 11

def gerar_arquivo_csv (json_atletas, json_clubes, json_posicoes):
	conteudo_csv = []
	cabecalho_csv = ["apelido", "preco", "media", "clube", "posicao", "em_casa", "clube_id", "clube_adversario_id",       "variacao_preco", "pontos_ultima", "percentual_participacao", "media_real"]
	conteudo_csv.append(cabecalho_csv)

	dicionarioIdClubePos = util.getDicionarioIdClubePos(json_clubes)

	rodada_atual = -1

	for json_atleta in json_atletas:
		rodada = json_atleta["rodada_id"]
		if rodada_atual == -1:
			rodada_atual = rodada
		jogos_disputados = json_atleta["jogos_num"]
		status_id = json_atleta["status_id"] 

		if status_id == 7 and jogos_disputados >= 0.66 * rodada:
			# fator_casa = 1.5
			apelido = json_atleta["apelido"]
			preco_num = float(json_atleta["preco_num"])
			media_num = float(json_atleta["media_num"])
			clube_id = json_atleta["clube_id"]
			posicao_id = json_atleta["posicao_id"]
			json_partida = json_atleta["partida"]
			time_de_casa = json_partida["clube_casa_id"]
			time_visitante = json_partida["clube_visitante_id"]
			variacao_preco = float(json_atleta["variacao_num"])
			pontos_ultima = json_atleta["pontos_num"]
			porcentual_partic = float(jogos_disputados / rodada)
			media_real = float(json_atleta["media_num"])

			# clube_adversario_id = -1
			if clube_id == time_de_casa:
				# media_num *= fator_casa
				clube_adversario_id = time_visitante
			else:
				clube_adversario_id = time_de_casa


			jogador_csv = [apelido, preco_num, media_num, dicionarioIdClubePos[clube_id][0], posicao_id, clube_id == time_de_casa, clube_id, clube_adversario_id, variacao_preco, pontos_ultima, porcentual_partic, media_real]
			conteudo_csv.append(jogador_csv)

	arquivo = "jogadores_rodada_{0}.csv".format(rodada_atual)
	with open(arquivo, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(conteudo_csv)

	print ("Arquivo {0} gravado com sucesso".format(arquivo))
	return conteudo_csv

def update_conteudo_csv (cartoletas, conteudo_csv, dict_probabilidades_vitoria_elenco, dict_aproveitamento_clubes):
	alg = "Selecao da Rodada"
	formacoes = ["4-4-2", "4-3-3", "4-5-1", "3-5-2", "3-4-3", "5-3-2", "5-4-1"]
	time_convocado_selecao = algoritmo.get_melhor_formacao_algoritmo(alg, cartoletas, conteudo_csv, formacoes, info, None)
	custo_selecao = mat_cartola.get_valor_indice_acumulado_time(time_convocado_selecao, info, "preco")
	print "Custo da Selecao da Rodada usando Medias do Cartola FC: {0}".format(custo_selecao)

	for i in range(1, len(conteudo_csv)):
		jogador = conteudo_csv[i]
		id_time = jogador[info["clube_id"]]
		media_jogador = jogador[info["media"]] 
		jogadores_time = util.obtem_jogadores_por_time (conteudo_csv, id_time, info)
		time_atual = []
		time_atual.append(jogadores_time)
		import pdb

		probabilidade_vitoria_elenco = dict_probabilidades_vitoria_elenco[id_time]
		aproveitamento_time = mat_cartola.get_porcentual_aproveitamento(dict_aproveitamento_clubes, id_time)
		variacao_preco = jogador[info["variacao_preco"]]
		preco = jogador[info["preco"]]
		percentual_participacao = info["percentual_participacao"]


		# rodada 14: 00.00 C$: 113.74
		importancia_cartoleta = ((cartoletas - custo_selecao) / custo_selecao) * (variacao_preco / preco)	
		jogador[info["media"]] = media_jogador * percentual_participacao * probabilidade_vitoria_elenco * aproveitamento_time
		jogador[info["media"]] = jogador[info["media"]] + importancia_cartoleta * jogador[info["media"]]

		# rodada 13: 45.85 C$: ~110
		# importancia_cartoleta = ((cartoletas - custo_selecao) / custo_selecao) * (variacao_preco / preco)	
		# jogador[info["media"]] = media_jogador * percentual_participacao * probabilidade_vitoria_elenco * aproveitamento_time
		# jogador[info["media"]] = jogador[info["media"]] + importancia_cartoleta * jogador[info["media"]]

		# recorde do programa - rodada 12: 53.79 C$: ~102.
		#jogador[info["media"]] = media_jogador * probabilidade_vitoria_elenco - variacao_preco

		conteudo_csv[i] = jogador	
	return conteudo_csv

reload(sys)
# sys.setdefaultencoding("latin-1")
sys.setdefaultencoding("UTF-8")
browser = webdriver.Firefox()

url_mercado = "https://api.cartolafc.globo.com/atletas/mercado"
browser.get (url_mercado)
json_body = json.loads(browser.find_element_by_tag_name('body').text)
json_atletas = json_body["atletas"]
json_clubes = json_body["clubes"]
json_posicoes = json_body["posicoes"]
conteudo_csv = gerar_arquivo_csv (json_atletas, json_clubes, json_posicoes)
random.seed()
json_partidas = leitor.get_json_partidas()
print ("Quantas cartoletas (C$) voce possui?")
cartoletas = float(input())
print "##########################################################################################"
formacoes = ["4-4-2", "4-3-3", "4-5-1", "3-5-2", "3-4-3", "5-3-2", "5-4-1"]
dict_aproveitamento_clubes = conversor.get_aproveitamento_clubes (json_partidas)
logging.debug (dict_aproveitamento_clubes)
dict_probabilidades_vitoria_elenco = mat_cartola.get_probabilidade_vitoria_elencos(json_clubes, conteudo_csv, info)
conteudo_csv = update_conteudo_csv(cartoletas, conteudo_csv, dict_probabilidades_vitoria_elenco, dict_aproveitamento_clubes)
algoritmos = ["Balanceado", "Balanceado V2", "Aleatorio", "Estrela Solitaria", "Genetico"]
# algoritmos = ["Balanceado"]
# algoritmos = ["Balanceado V2"]
# algoritmos = ["Aleatorio"]
# algoritmos = ["Estrela Solitaria"]
# algoritmos = ["Genetico"]

times_campeoes = {}
medias_campeoes = {}

for alg in algoritmos:
	if alg != "Genetico":
		times_campeoes[alg] = algoritmo.get_melhor_formacao_algoritmo(alg, cartoletas, conteudo_csv, formacoes, info, None)
	else:
		if len(medias_campeoes) != 0:
			limiar_algoritmo_genetico = max(medias_campeoes)
		else:
			limiar_algoritmo_genetico = 200.00

		print ("Limiar para algoritmo genetico: {0}".format(limiar_algoritmo_genetico))
		times_campeoes[alg] = algoritmo.get_melhor_formacao_algoritmo(alg, cartoletas, conteudo_csv, formacoes, info, limiar_algoritmo_genetico)
	
	media_time_campeao_alg = mat_cartola.get_valor_indice_acumulado_time(times_campeoes[alg], info, "media")
	medias_campeoes[media_time_campeao_alg] = alg

idx_vencedor_geral = max(medias_campeoes)
algoritmo_vencedor_geral = medias_campeoes[idx_vencedor_geral]
print "Vencedor Geral: {0}".format(algoritmo_vencedor_geral)
time_vencedor_geral = times_campeoes[algoritmo_vencedor_geral]
view.imprime_time(time_vencedor_geral, info)
custo_vencedor_geral = mat_cartola.get_valor_indice_acumulado_time(time_vencedor_geral, info, "preco")
print "Media: {0}; Custo: {1}".format(idx_vencedor_geral, custo_vencedor_geral)
browser.close()