package br.com.iasc.algorithms;

import java.util.List;
import java.util.Stack;

import org.json.JSONException;

import br.com.iasc.beans.Estado;
import br.com.iasc.beans.Problema;
import br.com.iasc.json.ParserDeProblemas;

/**
 * Implemetação do algoritmo de busca conhecido como Busca em Profundidade. O
 * algoritmo usa a pilha estadosParaExploracao para definir quais estados serão
 * visitados.
 * 
 * @author felipemartinsss
 *
 */
public class BuscaEmProfundidade extends Busca {
	private Stack<Estado> estadosParaExploracao;

	/**
	 * Construtor. Entrada: Um parser de problema para carregar dados do JSON e
	 * a instância atual do problema a ser resolvido.
	 * 
	 * @param pp
	 * @param problema
	 */
	public BuscaEmProfundidade(ParserDeProblemas pp, Problema problema) {
		super(pp, problema);
		this.estadosParaExploracao = new Stack<Estado>();
		System.out.println("Algoritmo " + getClass().getName());
	}

	/**
	 * Método que realiza a busca em profundidade.
	 */
	public List<String> buscarSolucao() throws JSONException {
		String aliasEstadoInicial = this.problema.getAliasEstadoInicial();
		Estado estadoAtual = this.pp.getEstadoPorAlias(this.problema,
				aliasEstadoInicial);

		this.acaoQueOrigina.put(estadoAtual, null);
		this.predecessores.put(estadoAtual, null);
		this.mapaEstadosDescobertos.put(estadoAtual, Boolean.valueOf(true));
		this.profundidadeEstado.put(estadoAtual, Integer.valueOf(0));
		this.estadosParaExploracao.push(estadoAtual);

		Estado ultimoEstado = null;
		while (!this.estadosParaExploracao.isEmpty()) {
			estadoAtual = (Estado) this.estadosParaExploracao.pop();
			if (this.problema.getEstadosMeta().contains(estadoAtual.getAlias())) {
				System.out.println("Solução encontrada!");
				ultimoEstado = estadoAtual;
				break;
			}
			this.problema = this.pp.carregaEstadosSucessores(this.problema,
					estadoAtual.getAlias());
			for (String acao : estadoAtual.getAcaoEstado().keySet()) {
				String aliasSucessor = (String) estadoAtual.getAcaoEstado()
						.get(acao);
				Estado sucessor = this.pp.getEstadoPorAlias(this.problema,
						aliasSucessor);
				if (this.mapaEstadosDescobertos.get(sucessor) == null) {
					this.mapaEstadosDescobertos.put(sucessor, true);
					this.estadosParaExploracao.push(sucessor);
					this.predecessores.put(sucessor, estadoAtual);
					this.profundidadeEstado.put(sucessor,
							this.profundidadeEstado.get(estadoAtual) + 1);
					this.acaoQueOrigina.put(sucessor, acao);
				}
			}
		}
		return getSolucao(ultimoEstado);
	}

	/**
	 * Método principal para a realização de testes.
	 * 
	 * @param args
	 * @throws JSONException
	 */
	public static void main(String[] args) throws JSONException {
		ParserDeProblemas pp = new ParserDeProblemas(
				"mundo-do-aspirador-de-po-original.json");
		Problema problema = pp.getProblemaBasico();
		BuscaEmProfundidade bl = new BuscaEmProfundidade(pp, problema);
		List<String> solucao = bl.buscarSolucao();
		System.out.println(solucao);
	}
}
