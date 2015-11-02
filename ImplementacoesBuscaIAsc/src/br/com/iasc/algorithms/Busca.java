package br.com.iasc.algorithms;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONException;

import br.com.iasc.beans.Estado;
import br.com.iasc.beans.Problema;
import br.com.iasc.json.ParserDeProblemas;

/**
 * Classe abstrata para representar uma implementação de algoritmos de busca.
 * Possui todos os atributos e métodos básicos e comuns 
 * às diferentes implementações de algoritmos.
 * @author felipemartinsss
 *
 */
public abstract class Busca {
	protected ParserDeProblemas pp;
	protected Problema problema;
	protected List<String> solucao;
	protected Map<Estado, Boolean> mapaEstadosDescobertos;
	protected Map<Estado, Estado> predecessores;
	protected Map<Estado, String> acaoQueOrigina;
	protected Map<Estado, Integer> profundidadeEstado;

	/**
	 * Construtor.
	 * Entrada: Recebe um parser de problemas para reconhecer o arquivo JSON e 
	 * uma instância do Problema parcialmente carregado em memória.
	 * @param pp
	 * @param problema
	 */
	public Busca(ParserDeProblemas pp, Problema problema) {
		this.pp = pp;
		this.problema = problema;
		this.solucao = new ArrayList<String>();
		this.mapaEstadosDescobertos = new HashMap<Estado, Boolean>();
		this.predecessores = new HashMap<Estado, Estado>();
		this.acaoQueOrigina = new HashMap<Estado, String>();
		this.profundidadeEstado = new HashMap<Estado, Integer>();
	}

	/**
	 * Método que devolve uma sequência de ações até alcançar um estado meta.
	 * Entrada: dado um último estado, esse método encontra a partir da 
	 * estrutura de predecessores, quais estados foram acessado antes 
	 * desse e que ações foram usadas.
	 * @param ultimoEstado
	 * @return
	 */
	public final List<String> getSolucao(Estado ultimoEstado) {
		Estado estado = ultimoEstado;
		if ((estado != null)
				&& (this.problema.getEstadosMeta().contains(estado.getAlias()))) {
			Estado predecessor = estado;
			do {
				String acao = (String) this.acaoQueOrigina.get(predecessor);
				if (acao != null) {
					this.solucao.add(acao);
				}
			} while ((predecessor = (Estado) this.predecessores
					.get(predecessor)) != null);
			Collections.reverse(this.solucao);
		} else {
			System.out.println("Solucao nao encontrada.");
		}
		return this.solucao;
	}

	/**
	 * Método abstrato que deve ser implementado por qualquer 
	 * classe filha de Busca.
	 * @return
	 * @throws JSONException
	 */
	public abstract List<String> buscarSolucao() throws JSONException;
}
