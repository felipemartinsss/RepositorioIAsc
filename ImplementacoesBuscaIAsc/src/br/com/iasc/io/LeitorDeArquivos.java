package br.com.iasc.io;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * Classe usada para ler arquivos.
 * 
 * @author felipemartinsss
 *
 */
public class LeitorDeArquivos {
	/**
	 * Método que devolve o conteúdo em texto de um arquivo. Entrada: O caminho
	 * que indica o arquivo a ser carregado. Saída: O texto contido no arquivo.
	 * 
	 * @param nomeArquivo
	 * @return
	 * @throws FileNotFoundException
	 */
	public static String getConteudoArquivo(String nomeArquivo)
			throws FileNotFoundException {
		Scanner leitor = new Scanner(new File("problemas/" + nomeArquivo));
		StringBuffer conteudoArquivo = new StringBuffer();
		while (leitor.hasNextLine()) {
			conteudoArquivo.append(leitor.nextLine());
		}
		leitor.close();
		System.out.println("Arquivo lido: " + conteudoArquivo.toString());
		return conteudoArquivo.toString();
	}
}
