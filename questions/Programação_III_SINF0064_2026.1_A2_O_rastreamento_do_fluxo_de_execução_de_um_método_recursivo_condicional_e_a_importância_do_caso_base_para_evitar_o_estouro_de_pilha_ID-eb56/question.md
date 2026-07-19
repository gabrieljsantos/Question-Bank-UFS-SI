(0,6 pontos) Considere o código abaixo, que apresenta uma classe contendo um método recursivo:

```java
public class AnaliseRecursiva {
    public static int processar(int n) {
        if (n <= 1) {
            return 1;
        } else if (n % 2 == 0) {
            return n + processar(n - 1);
        } else {
            return processar(n - 1) - n;
        }
    }

    public static void main(String[] args) {
        int resultado = processar(5);
        System.out.println("Resultado: " + resultado);
    }
}

```

A respeito do comportamento do método `processar` e do conceito de recursividade, avalie as asserções a seguir e a relação proposta entre elas:

**I.** A execução do método main imprimirá no console o valor Resultado: -3.

**II.** O método processar implementa uma recursão que possui um caso base bem definido para n <= 1, garantindo que a pilha de execução (call stack) não sofra um estouro (StackOverflowError) para qualquer valor inteiro positivo de n.

A respeito dessas asserções, assinale a opção correta.

* **A)** As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.
* **B)** As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.
* **C)** A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.
* **D)** A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.
* **E)** Ambas as asserções são proposições falsas.

