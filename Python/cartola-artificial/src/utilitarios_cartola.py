#!/usr/bin/env python
#!-*- coding: utf-8 -*-

def obtem_jogadores_por_posicao (conteudo_csv, posicao_id, info):
	jogadores_por_posicao = [j for j in conteudo_csv if j[info["posicao"]] == posicao_id]
	return jogadores_por_posicao

def obtem_jogadores_por_time (conteudo_csv, id_clube, info):
	jogadores_por_time = [j for j in conteudo_csv if j[info["clube_id"]] == id_clube]
	return jogadores_por_time

def getDicionarioIdClubePos (json_clubes):
	dicionarioIdClubePos = {}
	for json_clube in json_clubes:
		id_clube = json_clubes[json_clube]["id"]
		nome_clube = json_clubes[json_clube]["nome"]
		posicao_clube = json_clubes[json_clube]["posicao"]
		dicionarioIdClubePos[id_clube] = (nome_clube, posicao_clube)
	return dicionarioIdClubePos

def getDicionarioIdPosicaoNome (json_posicoes):
	dicionarioIdPosicoes = {}
	for json_posicao in json_posicoes:
		id_posicao = json_posicoes[json_posicao]["id"]
		nome_posicao = json_posicoes[json_posicao]["nome"]
		dicionarioIdPosicoes[id_posicao] = nome_posicao
	return dicionarioIdPosicoes

# Imprime todos os times?
def get_times_provaveis (json_clubes, conteudo_csv, info):
	dicionarioIdClubePos = getDicionarioIdClubePos(json_clubes)
	times_provaveis = {}
	for id_clube in dicionarioIdClubePos.keys():
		if id_clube not in times_provaveis:
			jogadores_time = obtem_jogadores_por_time(conteudo_csv, id_clube, info)
			if (len (jogadores_time) > 1):
				jogador_qualquer = jogadores_time[0]
				times_provaveis[id_clube] = get_time_provavel_jogador(jogador_qualquer, conteudo_csv, info)
				time = times_provaveis[id_clube]
	return times_provaveis

def get_time_provavel_jogador (jogador_1, conteudo_csv, info):
	jogadores_mesmo_time = []
	indices_posicoes = {}
	goleiro = []
	laterais = []
	zagueiros = []
	meias = []
	atacantes = []
	tecnico = []
	posicoes = [None, goleiro, laterais, zagueiros, meias, atacantes, tecnico]

	for i in range (1, len(posicoes)):
		indices_posicoes[i] = posicoes[i]
	for jogador_2 in conteudo_csv[1:]:
		if jogador_1[3] == jogador_2[3]:
			posicao = indices_posicoes[jogador_1[info["posicao"]]] # posicao_id
			posicao.append(jogador_2)	
	for i in range (1, len(posicoes)):
		jogadores_mesmo_time.append(indices_posicoes[i])
	return jogadores_mesmo_time

def get_num_jogadores_pos(formacao):
	jogadores_por_setor = formacao.split("-")
	num_jogadores_pos = {}
	num_jogadores_pos[1] = 1
	if jogadores_por_setor[0] == '3':
		num_jogadores_pos[2] = 0
		num_jogadores_pos[3] = int(jogadores_por_setor[0])

	else:
		num_jogadores_pos[2] = 2
		num_jogadores_pos[3] = int(jogadores_por_setor[0]) - 2

	num_jogadores_pos[4] = int(jogadores_por_setor[1])
	num_jogadores_pos[5] = int(jogadores_por_setor[2])
	num_jogadores_pos[6] = 1
	return num_jogadores_pos