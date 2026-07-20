(0,5 ponto) Considere o seguinte trecho de código em Java, que gerencia o controle de acessos de uma aplicação acadêmica:

```java
public class RastreadorAcesso {
    public static int totalAcessos = 0;
    private String usuario;

    public RastreadorAcesso(String usuario) {
        this.usuario = usuario;
        totalAcessos++;
    }

    public static int obterTotal() {
        // Linha X
        return totalAcessos;
    }
}

```

Em relação ao comportamento das variáveis e métodos estáticos no paradigma de orientação a objetos em Java, analise as afirmações a seguir:

I. O modificador `static` indica que a variável `totalAcessos` pertence à classe `RastreadorAcesso`, e não a uma instância específica, sendo compartilhada por todos os objetos criados a partir dela.

II. Caso o desenvolvedor insira a instrução `System.out.println(this.usuario);` na Linha X, o código compilará perfeitamente, uma vez que métodos estáticos possuem acesso direto a atributos de instância por estarem na mesma classe.

III. Se três objetos da classe `RastreadorAcesso` forem instanciados sequencialmente, o valor retornado pela chamada de `RastreadorAcesso.obterTotal()` será igual a 3.

É correto o que se afirma em:

a) I, II e III.

b) II, apenas.

c) II e III, apenas.

d) I, apenas.

e) I e III, apenas.