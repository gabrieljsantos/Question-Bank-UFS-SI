(0,5 ponto) Considere uma aplicação Java que realiza o processamento de pagamentos de uma universidade através do seguinte cenário estrutural:

```java
public class Usuario {
    public static double taxaAdministrativa = 10.0;

    public void aplicarDesconto() {
        taxaAdministrativa -= 2.0;
    }
}

public class Aluno extends Usuario {
    @Override
    public void aplicarDesconto() {
        taxaAdministrativa -= 5.0;
    }
}

```

No método `main`, realiza-se a seguinte sequência de instruções:

```java
Usuario[] grupo = new Usuario[2];
grupo[0] = new Usuario();
grupo[1] = new Aluno();

for (Usuario u : grupo) {
    u.aplicarDesconto();
}

System.out.println(Usuario.taxaAdministrativa);

```

Analise as asserções sobre o comportamento do código:

I. O array `grupo` armazena referências heterogêneas de objetos devido ao conceito de polimorfismo.

II. Durante a execução do laço `for-each`, o método `aplicarDesconto()` invocado no índice `grupo[1]` será o da classe `Usuario`, visto que o array foi tipado primitivamente como `Usuario[]`.

III. O valor final impresso no console correspondente à `taxaAdministrativa` será `3.0`.

É correto o que se afirma em:

a) I, apenas.

b) I e II, apenas.

c) II e III, apenas.

d) I, II e III.

e) I e III, apenas.