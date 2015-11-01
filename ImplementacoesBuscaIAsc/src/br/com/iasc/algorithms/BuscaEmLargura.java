package br.com.iasc.algorithms;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.json.JSONException;

import br.com.iasc.beans.Estado;
import br.com.iasc.beans.Problema;
import br.com.iasc.json.ParserDeProblemas;

public class BuscaEmLargura extends Busca {
	private LinkedList<Estado> estadosParaExploracao;

	public BuscaEmLargura(ParserDeProblemas pp, Problema problema) {
		super(pp, problema);
		this.estadosParaExploracao = new LinkedList <Estado> ();
		System.out.println("Algoritmo " + getClass().getName());
	}

	public List<String> buscarSolucao() throws JSONException {
		Estado ultimoEstado = null;
		System.out.println("Estado inicial: "
				+ this.problema.getAliasEstadoInicial());

		String aliasEstadoAtual = this.problema.getAliasEstadoInicial();
		this.problema = this.pp.carregaEstadosSucessores(this.problema,
				aliasEstadoAtual);
		Estado estadoAtual = this.pp.getEstadoPorAlias(this.problema,
				aliasEstadoAtual);

		this.mapaEstadosDescobertos.put(estadoAtual, Boolean.valueOf(true));
		this.estadosParaExploracao.add(estadoAtual);
		this.predecessores.put(estadoAtual, null);
		this.acaoQueOrigina.put(estadoAtual, null);
		this.profundidadeEstado.put(estadoAtual, Integer.valueOf(0));

		Estado primeiro = null;
		while (!this.estadosParaExploracao.isEmpty()) {
			primeiro = (Estado) this.estadosParaExploracao.peek();
			if (this.problema.getEstadosMeta().contains(primeiro.getAlias())) {
				System.out.println("Solução encontrada.");
				ultimoEstado = primeiro;
				break;
			}
			this.problema = this.pp.carregaEstadosSucessores(this.problema,
					primeiro.getAlias());
			Map<String, String> acaoEstado = primeiro.getAcaoEstado();
			for (String acao : acaoEstado.keySet()) {
				Estado sucessor = this.pp.getEstadoPorAlias(this.problema,
						(String) acaoEstado.get(acao));
				if (this.mapaEstadosDescobertos.get(sucessor) == null) {
					this.mapaEstadosDescobertos.put(sucessor,
							Boolean.valueOf(true));
					this.estadosParaExploracao.offer(sucessor);
					this.predecessores.put(sucessor, primeiro);
					this.acaoQueOrigina.put(sucessor, acao);
					this.profundidadeEstado.put(sucessor,
							this.profundidadeEstado.get(primeiro) + 1);
				}
			}
			this.estadosParaExploracao.poll();
		}
		return getSolucao(ultimoEstado);
	}

	public static void main(String[] args) throws JSONException {
		ParserDeProblemas pp = new ParserDeProblemas(
				"mundo-do-aspirador-de-po-original.json");
		Problema problema = pp.getProblemaBasico();
		BuscaEmLargura bl = new BuscaEmLargura(pp, problema);
		List<String> solucao = bl.buscarSolucao();
		System.out.println(solucao);
	}
}
