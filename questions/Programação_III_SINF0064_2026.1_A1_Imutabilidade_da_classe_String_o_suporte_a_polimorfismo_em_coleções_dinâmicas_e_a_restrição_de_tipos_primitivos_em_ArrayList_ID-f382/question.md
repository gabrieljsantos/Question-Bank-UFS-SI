(0,5 ponto) Considere o seguinte código em Java que manipula o cadastro de componentes acadêmicos de um curso de TI:

```java
import java.util.ArrayList;

public class ComponenteCurricular {
    private String nome;
    protected double cargaHoraria;

    public ComponenteCurricular(String nome, double cargaHoraria) {
        this.nome = nome;
        this.cargaHoraria = cargaHoraria;
    }

    public String getNome() {
        return this.nome;
    }

    public void atualizarNome(String novoNome) {
        this.nome.concat(" - ATUALIZADO");
    }
}

public class Laboratorio extends ComponenteCurricular {
    private int vagas;

    public Laboratorio(String nome, double ch, int vagas) {
        super(nome, ch);
        this.vagas = vagas;
    }
}

```

Analise as seguintes asserções a respeito do comportamento do código e das estruturas do Java:

I. A execução do método `atualizarNome` modificará permanentemente o conteúdo do atributo `nome` da instância, anexando o sufixo " - ATUALIZADO".

II. Se criarmos uma lista utilizando `ArrayList<ComponenteCurricular> lista = new ArrayList<ComponenteCurricular>();`, o polimorfismo permite que instâncias da classe `Laboratorio` sejam adicionadas a essa mesma lista.

III. Caso o programador tente instanciar uma lista genérica utilizando tipos primitivos como `ArrayList<int>`, o código compilará normalmente, pois o Java realiza a conversão automática de forma implícita no escopo das coleções.

É correto o que se afirma em:

a) II, apenas.

b) I e II.

c) II e III, apenas.

d) I, apenas.

e) I e III, apenas.