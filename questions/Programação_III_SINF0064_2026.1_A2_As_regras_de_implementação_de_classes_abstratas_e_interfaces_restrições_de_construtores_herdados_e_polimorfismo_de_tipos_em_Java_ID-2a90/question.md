(1,0 ponto) Considere o cenário de desenvolvimento de uma API para processamento financeiro estruturada com o seguinte código Java:

```java
public interface Tributavel {
    double calcularImposto();
}

```

```java
public abstract class Conta {
    protected double saldo;
    
    public Conta(double saldo) {
        this.saldo = saldo;
    }
    
    public abstract void atualizar();
}

```

```java
public class ContaInvestimento extends Conta implements Tributavel {
    public ContaInvestimento(double saldo) {
        super(saldo);
    }
    
    @Override
    public void atualizar() {
        this.saldo *= 1.05;
    }
    
    @Override
    public double calcularImposto() {
        return this.saldo * 0.02;
    }
}

```

Avalie as seguintes afirmações sobre a estrutura apresentada:

**I.** A classe `ContaInvestimento` é obrigada a fornecer a implementação concreta de `atualizar()` e `calcularImposto()`, caso contrário, causará erro de compilação.
**II.** O construtor de `ContaInvestimento` faz uma chamada a `super(saldo)`. Se o construtor explícito da classe abstrata `Conta` fosse removido, a linha `super(saldo)` geraria um erro de compilação se mantida.
**III.** Graças ao princípio da herança múltipla de classes e interfaces, uma linha contendo `Tributavel t = new ContaInvestimento(1000);` permite chamar diretamente o método `t.atualizar()` sem a necessidade de conversão.

É correto o que se afirma em:

* **A)** II, apenas.
* **B)** I e II, apenas.
* **C)** I e III, apenas.
* **D)** I e II, apenas. *(Nota: Opção repetida conforme a impressão original da imagem)*
* **E)** I, II e III.