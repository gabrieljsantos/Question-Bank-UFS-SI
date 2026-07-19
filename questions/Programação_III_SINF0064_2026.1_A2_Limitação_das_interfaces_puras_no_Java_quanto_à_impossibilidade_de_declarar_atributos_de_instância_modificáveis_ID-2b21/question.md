
2. (0,6 pontos) Um analista de sistemas propõe a substituição de uma classe abstrata por uma interface em um módulo de autenticação. A classe original possui a assinatura apresentada a seguir:

```java
public abstract class Autenticador {
    private String chaveSecreta;
    public abstract boolean validar(String token);
}

```

Ao tentar migrar essa estrutura para uma interface pura do Java, qual limitação técnica o desenvolvedor encontrará?

* **A)** O fato de que interfaces não podem ser implementadas por classes que pertençam a pacotes diferentes daquele onde a interface foi criada.
* **B)** A impossibilidade de declarar o atributo de instância `chaveSecreta`, visto que todos os campos declarados em interfaces são implicitamente constantes públicas, estáticas e finais (`public static final`).
* **C)** A restrição de que nenhum método dentro de uma interface pode possuir o modificador de retorno `boolean`.
* **D)** A impossibilidade de definir assinaturas de métodos que recebam parâmetros do tipo `String`.



