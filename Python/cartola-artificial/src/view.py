#!/usr/bin/env python
#!-*- coding: utf-8 -*-


import logging
import matematica_cartola
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')



def imprime_time (time_convocado, info):
	posicoes = {}
	posicoes[0] = "None"
	posicoes[1] = "Goleiro"
	posicoes[2] = "Lateral"
	posicoes[3] = "Zagueiro"
	posicoes[4] = "Meio-Campo"
	posicoes[5] = "Atacante"
	posicoes[6] = "Tecnico"

	print ("Apelido / Time / Preço / Media")
	for posicao in time_convocado:
		if posicao != 0:
			for jogador in posicao:
				if jogador != 0:
					posicao = posicoes[jogador[info["posicao"]]]
					apelido = jogador[info["apelido"]]
					clube = jogador[info["clube"]]
					preco = jogador[info["preco"]]
					media_cartola = jogador[info["media_cartola"]]
					print ("{0} / {1} / {2} / {3} / {4}".format(posicao, apelido, clube, preco, media_cartola))
