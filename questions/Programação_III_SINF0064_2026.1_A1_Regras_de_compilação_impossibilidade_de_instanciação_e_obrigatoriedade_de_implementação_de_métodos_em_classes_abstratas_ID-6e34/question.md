(0,5 ponto) No desenvolvimento de sistemas orientados a objetos em Java, as classes abstratas desempenham um papel crucial na arquitetura de software, servindo como uma ferramenta para modelar conceitos genéricos que representam uma forma abstrata, não devendo possuir uma existência concreta. Considere o seguinte cenário de modelagem de um sistema de automação bancária:

```java
public abstract class Conta {
    protected double saldo;

    public Conta(double saldoInicial) {
        this.saldo = saldoInicial;
    }

    public abstract void computarTaxa();

    public void depositar(double valor) {
        this.saldo += valor;
    }
}

public class ContaCorrente extends Conta {
    public ContaCorrente(double saldoInicial) {
        super(saldoInicial);
    }

    @Override
    public void computarTaxa() {
        this.saldo -= 4.50;
    }
}

```

A respeito do comportamento das classes abstratas e do código apresentado, analise as asserções a seguir:

I. A instrução `Conta c = new Conta(100.0);` gerará um erro em tempo de compilação, pois o modificador `abstract` impede que a classe seja instanciada diretamente.

II. A classe `ContaCorrente` é obrigada a fornecer uma implementação concreta para o método `computarTaxa()`, a menos que ela também seja declarada com o modificador `abstract`.

III. Métodos concretos (com corpo), como o método `depositar(double valor)`, não podem residir dentro de uma classe abstrata em Java, invalidando a compilação do código apresentado.

É correto o que se afirma em:

a) I e II, apenas.

b) II e III, apenas.

c) I, apenas.

d) III, apenas.

e) I, II e III.