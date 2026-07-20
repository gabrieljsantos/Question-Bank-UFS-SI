(0,5 ponto) Considere o seguinte modelo de classes que simula o processamento de relatórios em um sistema corporativo:

```java
public abstract class Relatorio {
    protected String titulo;

    public Relatorio(String titulo) {
        this.titulo = titulo;
    }

    public abstract void emitirCorpo();

    public void imprimir() {
        System.out.print("[" + this.titulo + "]");
        emitirCorpo();
    }
}

public class RelatorioFinanceiro extends Relatorio {
    public RelatorioFinanceiro(String t1) {
        super(t1);
    }

    @Override
    public void emitirCorpo() {
        System.out.print("Dados Financeiros");
    }
}

```

Considere que o desenvolvedor executou a seguinte instrução no método principal (`main`):

```java
Relatorio ref = new RelatorioFinanceiro("Anual");
ref.imprimir();

```

A respeito do comportamento do código e das propriedades das classes abstratas, analise as seguintes asserções:

I. A linha de código `Relatorio ref = new RelatorioFinanceiro("Anual");` é válida e exemplifica o uso do polimorfismo de inclusão, onde uma referência da superclasse abstrata aponta para um objeto da subclasse concreta.

II. O método `imprimir()` na classe abstrata `Relatorio` demonstra que classes marcadas como `abstract` podem conter lógica concreta e perfeitamente operacional em seus métodos não abstratos.

III. Caso a assinatura do método `emitirCorpo()` na classe `RelatorioFinanceiro` fosse alterada para `public void emitirCorpo(int ano)`, o código continuaria compilando normalmente como uma sobrescrita válida.

É correto o que se afirma em:

a) I, apenas.

b) II e III, apenas.

c) II, apenas.

d) I, II e III.

e) I e II, apenas.