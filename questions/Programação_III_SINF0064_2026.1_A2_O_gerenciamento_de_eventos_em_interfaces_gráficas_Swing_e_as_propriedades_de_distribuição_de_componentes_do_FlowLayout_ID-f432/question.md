(0,6 pontos) Considere o código abaixo, escrito na linguagem de programação Java, que constrói uma janela simples utilizando a especificação Swing e o modelo de delegação de eventos:
*(O início desta questão encontra-se no final da página anterior)*

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class FormularioBasico extends JFrame {
    private JTextField txtEntrada;
    private JLabel lblResultado;
    private JButton btnProcessar;

    public FormularioBasico() {
        setTitle("Sistema de Validação");
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new FlowLayout());

        txtEntrada = new JTextField(15);
        btnProcessar = new JButton("Validar");
        lblResultado = new JLabel("Aguardando...");

        btnProcessar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String texto = txtEntrada.getText();
                if (texto.trim().isEmpty()) {
                    lblResultado.setText("Campo Vazio!");
                } else {
                    lblResultado.setText("Texto: " + texto.toUpperCase());
                }
            }
        });

        add(txtEntrada);
        add(btnProcessar);
        add(lblResultado);
        setVisible(true);
    }

    public static void main(String[] args) {
        new FormularioBasico();
    }
}

```

A partir da análise do código e dos conceitos de programação de interfaces gráficas em Java, avalie as asserções a seguir e a relação proposta entre elas:

**I.** Ao digitar a palavra "enade" no campo de texto e clicar no botão "Validar", o rótulo (`lblResultado`) passará a exibir o texto "Texto: ENADE".

**II.** O gerenciador de layout `FlowLayout` posiciona os componentes em uma grade rígida de linhas e colunas de tamanho fixo, o que impede que o texto do rótulo (`lblResultado`) seja atualizado dinamicamente em tempo de execução após o clique do botão.

A respeito dessas asserções, assinale a opção correta.

* **A)** As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.
* **B)** As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.
* **C)** A asserção I é uma afirmação verdadeira, e a II é uma proposição falsa.
* **D)** A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.
* **E)** Ambas as asserções são proposições falsas.
