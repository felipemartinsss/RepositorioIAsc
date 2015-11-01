package br.com.iasc.beans;

import java.util.List;
import java.util.Map;

public class Estado
{
  private String alias;
  private List<String> nomesVariaveis;
  private List<Boolean> valoresVariaveis;
  private Map<String, String> acaoEstado;
  
  public Estado() {}
  
  public Estado(String alias, List<String> nomesVariaveis, List<Boolean> valoresVariaveis)
  {
    this.alias = alias;
    this.nomesVariaveis = nomesVariaveis;
    this.valoresVariaveis = valoresVariaveis;
  }
  
  public String getAlias()
  {
    return this.alias;
  }
  
  public List<Boolean> getValoresVariaveis()
  {
    return this.valoresVariaveis;
  }
  
  public void setAcaoEstado(Map<String, String> acaoEstado)
  {
    this.acaoEstado = acaoEstado;
  }
  
  public Map<String, String> getAcaoEstado()
  {
    return this.acaoEstado;
  }
  
  public String toString()
  {
    StringBuffer descricaoEstado = new StringBuffer();
    descricaoEstado.append(this.alias + " : [");
    for (int i = 0; i < this.nomesVariaveis.size(); i++) {
      descricaoEstado.append(" " + (String)this.nomesVariaveis.get(i) + " = " + this.valoresVariaveis.get(i) + " ");
    }
    descricaoEstado.append("]");
    return descricaoEstado.toString();
  }
  
  public boolean equals(Object obj)
  {
    if ((obj instanceof Estado))
    {
      Estado outroEstado = (Estado)obj;
      return getAlias().equals(outroEstado.getAlias());
    }
    return false;
  }
  
  public int hashCode()
  {
    return this.alias.hashCode() * this.valoresVariaveis.hashCode();
  }
}
