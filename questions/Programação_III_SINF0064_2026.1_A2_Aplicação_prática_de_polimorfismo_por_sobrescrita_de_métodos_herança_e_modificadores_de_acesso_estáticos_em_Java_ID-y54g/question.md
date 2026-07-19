(1,0 ponto) Considere um sistema de gerenciamento de notificações acadêmicas desenvolvido em Java. Para estruturar o envio de mensagens, o desenvolvedor definiu a seguinte interface e estrutura de classes:

```java
public interface Enviavel {
    public void enviar(String mensagem);
}

```

```java
public class Notificacao implements Enviavel {
    protected String destinatario;
    
    public Notificacao(String destinatario) {
        this.destinatario = destinatario;
    }
    
    @Override
    public void enviar(String mensagem) {
        System.out.println("Enviando aviso geral para " + destinatario + ": " + mensagem);
    }
}

```

```java
public class NotificacaoUrgente extends Notificacao {
    private static int totalUrgentes = 0;
    
    public NotificacaoUrgente(String destinatario) {
        super(destinatario);
        totalUrgentes++;
    }
    
    @Override
    public void enviar(String mensagem) {
        System.out.print("[URGENTE] " + destinatario.toUpperCase() + ": " + mensagem);
    }
    
    public static int getTotalUrgentes() {
        return totalUrgentes;
    }
}

```

No método `main` de outra classe do mesmo pacote, executou-se o seguinte trecho de código:

```java
ArrayList<Enviavel> lista = new ArrayList<>();
lista.add(new Notificacao("aluno1@ufs.br"));
lista.add(new NotificacaoUrgente("professor1@ufs.br"));
for (Enviavel e : lista) {
    e.enviar("O sistema entrará em manutenção.");
}
System.out.println("Urgentes: " + NotificacaoUrgente.getTotalUrgentes());

```

Analisando o código e as regras de Programação Orientada a Objetos em Java, avalie as afirmações a seguir:

**I.** O código demonstra a aplicação prática de polimorfismo (sobreposição/sobrescrita de método), pois a chamada `e.enviar(...)` executará comportamentos diferentes a depender do tipo real do objeto instanciado na lista em tempo de execução.
**II.** A classe `NotificacaoUrgente` herda o atributo `destinatario` da classe `Notificacao`. Caso o modificador de `destinatario` fosse alterado de `protected` para `private`, o código da classe `NotificacaoUrgente` continuaria compilando sem erros, mas impediria a herança direta do atributo.
**III.** A variável `totalUrgentes` possui o modificador `static`, o que significa que ela é compartilhada por todas as instâncias da classe `NotificacaoUrgente`, agindo como um contador global da classe toda vez que o construtor é invocado.

É correto o que se afirma em:

* **A)** I, apenas.
* **B)** III, apenas.
* **C)** I e II, apenas.
* **D)** I e III, apenas.
* **E)** I, II e III.
