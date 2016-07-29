#!/usr/bin/env python
#!-*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

def get_aproveitamento_clubes (json_partidas):
	dict_aproveitamento_clubes = {}
	if json_partidas != None:
		for partida in json_partidas:
			# Le dados do clube de casa/mandante
			logging.debug("clube_casa_id: {0}".format(partida["clube_casa_id"]))
			logging.debug("aproveitamento_mandante: {0}".format(list(partida["aproveitamento_mandante"])))
			dict_aproveitamento_clubes[int(partida["clube_casa_id"])] = list(partida["aproveitamento_mandante"])

			# Le dados do clube visitante
			logging.debug("clube_visitante_id: {0}".format(partida["clube_visitante_id"]))
			logging.debug("aproveitamento_visitante: {0}".format(list(partida["aproveitamento_visitante"])))
			dict_aproveitamento_clubes[int(partida["clube_visitante_id"])] = list(partida["aproveitamento_visitante"])
	return dict_aproveitamento_clubes