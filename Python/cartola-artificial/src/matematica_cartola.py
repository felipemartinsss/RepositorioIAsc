#!/usr/bin/env python
#!-*- coding: utf-8 -*-

import random
import utilitarios_cartola as util

def get_porcentual_aproveitamento (dict_aproveitamento_time, id_time):
	porcentual_aproveitamento = 0.0
	if dict_aproveitamento_time != None:
		aproveitamento_time = dict_aproveitamento_time[id_time]
		pontos_disputados = float(len(aproveitamento_time) * 3)
		vitorias = aproveitamento_time.count("v")
		empates = aproveitamento_time.count("e")
		derrotas = aproveitamento_time.count("d")
		pontos_ganhos = float(3 * vitorias + empates)
		porcentual_aproveitamento = pontos_ganhos / pontos_disputados
	return porcentual_aproveitamento

# Use "media", "preco" ou "media_cartola" como (indice) para saber os valores acumulados por jogador no 
# time completo.
def get_valor_indice_acumulado_time (time_convocado, info, indice):
	valor_acumulado = 0.0
	for posicao in time_convocado:
		for jogador in posicao:
			if jogador != 0:
				valor_acumulado += float(jogador[info[indice]])
	return valor_acumulado

def get_probabilidade_vitoria_time (times_provaveis, id_clube, id_clube_adversario, info):
	time = times_provaveis[id_clube]
	time_adversario = times_provaveis[id_clube_adversario]
	media_time = get_valor_indice_acumulado_time(time, info, "media")
	media_time_adversario = get_valor_indice_acumulado_time(time_adversario, info, "media")
	soma_medias = media_time + media_time_adversario
	probabilidade_vitoria_elenco = media_time / soma_medias
	return probabilidade_vitoria_elenco

def get_probabilidade_vitoria_elencos (json_clubes, conteudo_csv, info):
	dict_probabilidades_vitoria_elenco = {}
	times_provaveis = util.get_times_provaveis(json_clubes, conteudo_csv, info)
	for id_time in times_provaveis:
		time = times_provaveis[id_time]
		#print "Time provavel {0}: ".format(id_time)
		#print "Custo: {0}".format(get_custo_time(time))
		#print "Media: {0}".format(get_media_time(time))
		jogadores_time = util.obtem_jogadores_por_time (conteudo_csv, id_time, info)
		#print jogadores_time
		jogador_qualquer = jogadores_time[0]
		probabilidade_vitoria_elenco = get_probabilidade_vitoria_time(times_provaveis, jogador_qualquer[6], jogador_qualquer[7], info)
		dict_probabilidades_vitoria_elenco[id_time] = probabilidade_vitoria_elenco
		#print "Probabilidade de Vitoria por Elenco: {0}".format(probabilidade_vitoria_elenco)
	return dict_probabilidades_vitoria_elenco

def get_id_time_probabilidade_cumulativa (probabilidade_continuidade_cumulativa):
	probabilidade_sorteada = random.random()
	# print probabilidade_sorteada
	for i in range(0, len(probabilidade_continuidade_cumulativa)):
		if probabilidade_sorteada <= probabilidade_continuidade_cumulativa[i]:
			return i
