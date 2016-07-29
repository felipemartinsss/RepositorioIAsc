#!/usr/bin/env python
#!-*- coding: utf-8 -*-


import sys
import json
from selenium import webdriver

def get_json_partidas():
	sys.setdefaultencoding("latin-1")
	browser = webdriver.Firefox()
	url_partidas = "https://api.cartolafc.globo.com/partidas"
	browser.get (url_partidas)
	json_partidas_body = json.loads(browser.find_element_by_tag_name('body').text)
	browser.close()
	partidas = json_partidas_body["partidas"]
	return partidas
	
