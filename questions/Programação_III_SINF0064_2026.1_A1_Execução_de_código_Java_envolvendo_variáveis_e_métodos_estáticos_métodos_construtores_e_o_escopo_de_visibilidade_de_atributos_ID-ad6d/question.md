(0,5 ponto) Considere o código Java abaixo, projetado para monitorar a emissão de ordens de serviço em uma plataforma de engenharia:

```java
public class OrdemServico {
    private static int contadorOS = 100;
    private int idObjeto;
    protected String descricao;

    public OrdemServico(String descricao) {
        contadorOS += 5;
        this.idObjeto = contadorOS;
        this.descricao = descricao;
    }

    public void exibirRelatorio() {
        System.out.print(this.idObjeto + ":" + this.descricao + " ");
    }

    public static int getContador() {
        return contadorOS;
    }
}

```

Um desenvolvedor executa o seguinte bloco de código no método `main`:

```java
public static void main(String[] args) {
    OrdemServico os1 = new OrdemServico("Manutencao");
    OrdemServico os2 = new OrdemServico("Instalacao");
    os1.exibirRelatorio();

    System.out.print(OrdemServico.getContador());
}

```

Assinale a alternativa que apresenta a saída correta exibida no console após a execução:

a) 105:Manutencao 105

b) 100:Manutencao 110

c) 110:Manutencao 110

d) O código não compila, pois um método estático (`getContador`) não pode acessar uma variável de classe privada (`private static`).

e) 105:Manutencao 110