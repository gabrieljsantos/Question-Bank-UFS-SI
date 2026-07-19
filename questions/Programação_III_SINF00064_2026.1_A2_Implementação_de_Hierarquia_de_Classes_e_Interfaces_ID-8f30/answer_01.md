## Parte 1: Arquitetura de Classes (OO)

Aqui está o código das interfaces e classes que compõem a lógica de negócios:

```java
// 1. Contratavel (Interface)
public interface Contratavel {
    public double calcularValorTotal();
}

```

```java
// 2. Plano (Classe Abstrata)
public abstract class Plano implements Contratavel {
    protected String nomeCliente;

    public Plano(String nomeCliente) {
        this.nomeCliente = nomeCliente;
    }
}

```

```java
// 3. PlanoMensal (Classe Concreta)
public class PlanoMensal extends Plano {
    private double valorBase;

    public PlanoMensal(String nomeCliente, double valorBase) {
        super(nomeCliente);
        this.valorBase = valorBase;
    }

    @Override
    public double calcularValorTotal() {
        return this.valorBase;
    }
}

```

```java
// 4. PlanoDiario (Classe Concreta)
public class PlanoDiario extends Plano {
    private double valorDiaria;
    private int quantidadeDias;

    public PlanoDiario(String nomeCliente, double valorDiaria, int quantidadeDias) {
        super(nomeCliente);
        this.valorDiaria = valorDiaria;
        this.quantidadeDias = quantidadeDias;
    }

    @Override
    public double calcularValorTotal() {
        return this.valorDiaria * this.quantidadeDias;
    }
}

```

---

## Parte 2: Tratamento de Eventos

Este é o código que deve ser inserido **estritamente dentro** do método `actionPerformed` do botão `btnCalcular`.

Ele faz a captura dos dados da tela (conforme a interface gráfica apresentada que foca no "Plano Diário"), realiza as conversões necessárias, instancia o objeto correto e atualiza o rótulo de resultado:

```java
@Override
public void actionPerformed(ActionEvent e) {
    // 1. Captura os dados textuais dos componentes da tela
    String nome = txtCliente.getText();
    String strValorDiaria = txtValorDiaria.getText();
    String strDias = txtDias.getText();

    try {
        // 2. Converte os valores para os tipos corretos
        double valorDiaria = Double.parseDouble(strValorDiaria);
        int dias = Integer.parseInt(strDias);

        // 3. Instancia o PlanoDiario utilizando o polimorfismo da interface
        Contratavel plano = new PlanoDiario(nome, valorDiaria, dias);

        // 4. Calcula o total e atualiza o JLabel na tela
        double total = plano.calcularValorTotal();
        lblResultado.setText("Total: R$ " + total);

    } catch (NumberFormatException ex) {
        // Trata possíveis erros caso o usuário digite letras onde deveriam ser números
        lblResultado.setText("Erro: Valores inválidos!");
    }
}

```