package br.com.iasc.json;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import br.com.iasc.beans.Estado;
import br.com.iasc.beans.Problema;
import br.com.iasc.io.LeitorDeArquivos;

/**
 * Classe usada para realiza o parsing dos arquivos .json que 
 * especificam problemas de Busca.
 * @author felipemartinsss
 *
 */
public class ParserDeProblemas {
	private String conteudoArquivo;

	/**
	 * Construtor.
	 * Entrada: Recebe um nome de arquivo e 
	 * carrega o conteúdo do arquivo cujo 
	 * nome foi fornecido.
	 * @param nomeArquivo
	 */
	public ParserDeProblemas(String nomeArquivo) {
		try {
			this.conteudoArquivo = LeitorDeArquivos
					.getConteudoArquivo(nomeArquivo);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	/**
	 * 
	 * @return
	 * @throws JSONException
	 */
	public Problema getProblemaBasico() throws JSONException {
		JSONObject mundoDoAspiradorDePo = new JSONObject(this.conteudoArquivo);
		JSONObject jsonProblema = mundoDoAspiradorDePo
				.getJSONObject("problema");

		Problema problema = new Problema();

		problema.setNome(jsonProblema.getString("nome"));

		JSONArray jsonVariaveis = jsonProblema.getJSONArray("variaveis");
		List<String> variaveis = new ArrayList <String> ();
		for (int i = 0; i < jsonVariaveis.length(); i++) {
			String nomeVariavel = jsonVariaveis.getString(i);
			variaveis.add(nomeVariavel);
		}
		problema.setVariaveis(variaveis);

		List<String> acoes = new ArrayList <String> ();
		JSONArray jsonAcoes = jsonProblema.getJSONArray("acoes");
		for (int i = 0; i < jsonAcoes.length(); i++) {
			String nomeAcao = jsonAcoes.getString(i);
			acoes.add(nomeAcao);
		}
		problema.setAcoes(acoes);

		String aliasEstadoInicial = jsonProblema.getString("estado-inicial");
		problema.setAliasEstadoInicial(aliasEstadoInicial);

		JSONObject jsonEstados = jsonProblema.getJSONObject("estados");
		JSONArray jsonVariaveisEstadoSel = jsonEstados
				.optJSONArray(aliasEstadoInicial);
		List<Boolean> variaveisDeEstado = new ArrayList <Boolean> ();
		for (int i = 0; i < jsonVariaveisEstadoSel.length(); i++) {
			variaveisDeEstado.add(Boolean.valueOf(jsonVariaveisEstadoSel
					.getBoolean(i)));
		}
		Estado estado = new Estado(aliasEstadoInicial, variaveis,
				variaveisDeEstado);
		Set<Estado> estados = new HashSet <Estado> ();
		estados.add(estado);
		problema.setEstados(estados);

		JSONObject jsonTransicoes = jsonProblema.getJSONObject("transicoes");
		JSONArray jsonTransicoesDoEstado = jsonTransicoes
				.getJSONArray(aliasEstadoInicial);
		Map<String, String> acaoEstado = new HashMap <String, String> ();
		for (int i = 0; i < jsonTransicoesDoEstado.length(); i++) {
			JSONObject jsonTransicao = jsonTransicoesDoEstado.getJSONObject(i);
			String acaoAtual = (String) acoes.get(i);
			String estadoSucessor = jsonTransicao.getString(acaoAtual);
			acaoEstado.put(acaoAtual, estadoSucessor);
		}
		problema.setAcaoEstado(acaoEstado);

		JSONArray jsonEstadosMeta = jsonProblema.getJSONArray("estados-meta");
		List<String> estadosMeta = new ArrayList <String> ();
		for (int i = 0; i < jsonEstadosMeta.length(); i++) {
			String meta = jsonEstadosMeta.getString(i);
			estadosMeta.add(meta);
		}
		problema.setEstadosMeta(estadosMeta);

		return problema;
	}

	public Problema carregaEstadosSucessores(Problema problema,
			String aliasEstadoAtual) throws JSONException {
		List<Estado> estadosSucessores = new ArrayList <Estado> ();
		JSONObject mundoDoAspiradorDePo = new JSONObject(this.conteudoArquivo);
		JSONObject jsonProblema = mundoDoAspiradorDePo
				.getJSONObject("problema");
		JSONObject jsonEstados = jsonProblema.getJSONObject("estados");
		JSONObject jsonTransicoes = jsonProblema.getJSONObject("transicoes");
		JSONArray jsonTransicoesDoEstado = jsonTransicoes
				.getJSONArray(aliasEstadoAtual);
		Estado estado = getEstadoPorAlias(problema, aliasEstadoAtual);
		List<String> acoes = problema.getAcoes();
		Map<String, String> acaoEstado = new HashMap <String, String> ();
		for (int i = 0; i < jsonTransicoesDoEstado.length(); i++) {
			JSONObject jsonTransicao = jsonTransicoesDoEstado.getJSONObject(i);
			String acao = (String) acoes.get(i);
			String aliasEstadoSucessor = jsonTransicao.getString(acao);
			acaoEstado.put(acao, aliasEstadoSucessor);
			JSONArray jsonVariaveisDoEstado = jsonEstados
					.getJSONArray(aliasEstadoSucessor);
			List<Boolean> variaveisDoEstado = new ArrayList <Boolean> ();
			for (int j = 0; j < jsonVariaveisDoEstado.length(); j++) {
				variaveisDoEstado.add(Boolean.valueOf(jsonVariaveisDoEstado
						.getBoolean(j)));
			}
			Estado sucessor = new Estado(aliasEstadoSucessor,
					problema.getVariaveis(), variaveisDoEstado);
			estadosSucessores.add(sucessor);
		}
		estado.setAcaoEstado(acaoEstado);

		problema.getEstados().addAll(estadosSucessores);

		return problema;
	}

	public Problema carregaEstadoSucessor(Problema problema,
			String aliasEstadoAtual, String acao) throws JSONException {
		List<Estado> estadosSucessores = new ArrayList <Estado>();
		JSONObject mundoDoAspiradorDePo = new JSONObject(this.conteudoArquivo);
		JSONObject jsonProblema = mundoDoAspiradorDePo
				.getJSONObject("problema");
		JSONObject jsonEstados = jsonProblema.getJSONObject("estados");
		JSONObject jsonTransicoes = jsonProblema.getJSONObject("transicoes");
		JSONArray jsonTransicoesDoEstado = jsonTransicoes
				.getJSONArray(aliasEstadoAtual);
		List<String> acoes = problema.getAcoes();
		int indiceAcao = acoes.indexOf(acao);
		JSONObject jsonTransicao = jsonTransicoesDoEstado
				.getJSONObject(indiceAcao);
		String aliasEstadoSucessor = jsonTransicao.getString(acao);
		JSONArray jsonVariaveisDoEstado = jsonEstados
				.getJSONArray(aliasEstadoSucessor);
		List<Boolean> variaveisDoEstado = new ArrayList <Boolean> ();
		for (int j = 0; j < jsonVariaveisDoEstado.length(); j++) {
			variaveisDoEstado.add(Boolean.valueOf(jsonVariaveisDoEstado
					.getBoolean(j)));
		}
		Estado sucessor = new Estado(aliasEstadoSucessor,
				problema.getVariaveis(), variaveisDoEstado);
		estadosSucessores.add(sucessor);
		problema.getEstados().addAll(estadosSucessores);
		Estado estadoAtual = getEstadoPorAlias(problema, aliasEstadoAtual);
		estadoAtual.getAcaoEstado().put(acao, sucessor.getAlias());
		return problema;
	}

	public Estado getEstadoPorAlias(Problema problema, String aliasEstado) {
		Estado estadoResultante = null;
		for (Estado estado : problema.getEstados()) {
			if ((estado.getAlias() != null)
					&& (estado.getAlias().equals(aliasEstado))) {
				estadoResultante = estado;
			}
		}
		return estadoResultante;
	}

	/**
	 * Método de testes da classe.
	 * @param args
	 * @throws FileNotFoundException
	 * @throws JSONException
	 */
	public static void main(String[] args) throws FileNotFoundException,
			JSONException {
		ParserDeProblemas pp = new ParserDeProblemas(
				"mundo-do-aspirador-de-po-melhorado.json");
		Problema problema = pp.getProblemaBasico();
		System.out.println(problema.toString());
		problema = pp.carregaEstadosSucessores(problema,
				problema.getAliasEstadoInicial());
		System.out
				.println("Apos carregar estados sucessores do estado inicial...");

		String acao = "mover_para_sala_esquerda";
		String estadoHipotetico = "s2";
		problema = pp.carregaEstadoSucessor(problema, estadoHipotetico, acao);

		System.out.println(problema.toString());
	}
}
