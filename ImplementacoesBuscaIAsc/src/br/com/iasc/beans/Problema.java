package br.com.iasc.beans;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Classe para armazenar as variáveis importante de um problema de 
 * Busca.
 * @author felipemartinsss
 *
 */
public class Problema
{
  private String nome;
  private List<String> variaveis;
  private List<String> acoes;
  private Set<Estado> estados;
  private String aliasEstadoInicial;
  private List<String> estadosMeta;
  private Map<String, String> acaoEstado;
  
  public String getNome()
  {
    return this.nome;
  }
  
  public void setNome(String nome)
  {
    this.nome = nome;
  }
  
  public List<String> getVariaveis()
  {
    return this.variaveis;
  }
  
  public void setVariaveis(List<String> variaveis)
  {
    this.variaveis = variaveis;
  }
  
  public List<String> getAcoes()
  {
    return this.acoes;
  }
  
  public void setAcoes(List<String> acoes)
  {
    this.acoes = acoes;
  }
  
  public String getAliasEstadoInicial()
  {
    return this.aliasEstadoInicial;
  }
  
  public void setAliasEstadoInicial(String aliasEstadoInicial)
  {
    this.aliasEstadoInicial = aliasEstadoInicial;
  }
  
  public Set<Estado> getEstados()
  {
    return this.estados;
  }
  
  public void setEstados(Set<Estado> estados)
  {
    this.estados = estados;
  }
  
  public Map<String, String> getAcaoEstado()
  {
    return this.acaoEstado;
  }
  
  public void setAcaoEstado(Map<String, String> acaoEstado)
  {
    this.acaoEstado = acaoEstado;
  }
  
  public List<String> getEstadosMeta()
  {
    return this.estadosMeta;
  }
  
  public void setEstadosMeta(List<String> estadosMeta)
  {
    this.estadosMeta = estadosMeta;
  }
  
  public String toString()
  {
    StringBuffer descricaoProblema = new StringBuffer();
    descricaoProblema.append("Nome: " + this.nome + "\n");
    descricaoProblema.append("Variaveis: " + this.variaveis.toString() + "\n");
    descricaoProblema.append("Acoes: " + this.acoes.toString() + "\n");
    descricaoProblema.append("Estado Inicial: " + this.aliasEstadoInicial + "\n");
    descricaoProblema.append("Estados: \n");
    for (Estado estado : this.estados) {
      descricaoProblema.append(estado + "\n");
    }
    descricaoProblema.append("Transicoes: \n");
    for (String acao : this.acaoEstado.keySet()) {
      descricaoProblema.append(acao + " => " + (String)this.acaoEstado.get(acao) + "\n");
    }
    descricaoProblema.append("Estados Meta: " + this.estadosMeta + "\n");
    return descricaoProblema.toString();
  }
}

