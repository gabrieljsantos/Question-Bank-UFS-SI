# Question Bank UFS SI


Banco colaborativo de questões acadêmicas organizado por disciplina, código, professor, período, avaliação, tema e identificador único.

O projeto possui três partes principais:

1. **Gerenciador do banco**, usado para criar a estrutura vazia de uma questão e editar seus metadados.
2. **Arquivos Markdown**, nos quais o enunciado e as respostas são escritos manualmente.
3. **Página Web**, usada para navegar pelo banco e visualizar as questões e respostas renderizadas.

> [!IMPORTANT]
> O gerenciador **não escreve o enunciado nem produz as respostas**. Ao criar uma questão, ele gera arquivos `.md` vazios. O conteúdo deve ser colocado manualmente depois.

---

> ### Acesso ao Banco de Questões
>
> O banco de questões pode ser acessado diretamente pelo GitHub Pages:
>
> [**Acessar o Question Bank UFS SI**](https://gabrieljsantos.github.io/Question-Bank-UFS-SI/)


---

## Regras de anonimização

Este banco utiliza nomes alternativos para evitar a exposição desnecessária de identidades.

- No campo **Colaborador**, use um apelido ou codinome.
- Não use nome completo, matrícula, e-mail ou outra identificação pessoal como nome de colaborador.
- No campo **Professor**, use somente o codinome já adotado pelo banco.
- As listas suspensas mostram codinomes que já aparecem nas questões existentes.
- Caso o professor ainda não esteja na lista, ou você não saiba qual codinome corresponde a ele, consulte a administração do banco antes de preencher o campo.
- Não publique a relação entre codinomes e nomes reais.
- Não invente outro codinome para um professor que talvez já esteja cadastrado.

Os codinomes identificam registros internamente, mas não devem ser usados para tentar revelar a identidade de professores ou colaboradores.

---

## Estrutura do projeto

```text
Question Bank UFS SI/
├── question_bank_manager.py   # Gerenciador gráfico do banco
├── rebuild_the_indexer.py     # Reconstrói o índice das questões
├── index.html                 # Página principal do visualizador
├── app.js                     # Carregamento e renderização do banco
├── styles.css                 # Aparência da página
├── README.md                  # Este arquivo
└── questions/
    ├── index.json             # Lista das pastas registradas
    └── <pasta-da-questao>/
        ├── metadata.json      # Metadados da questão
        ├── question.md        # Enunciado
        ├── answer_01.md       # Primeira resposta, quando criada
        ├── answer_02.md       # Segunda resposta, quando criada
        └── imagens...         # Fotografias, diagramas e outras mídias
```

Cada questão fica em uma pasta própria. O nome da pasta é montado automaticamente com base nos metadados:

```text
Disciplina_Codigo_Periodo_Avaliacao_Tag_ID
```

Não é necessário criar ou renomear essa pasta manualmente.

---

## Requisitos

- Python 3.10 ou superior;
- biblioteca `PySide6`;
- navegador moderno;
- VS Code ou outro editor compatível com Markdown.

### Instalação do PySide6

No Windows:

```powershell
py -m pip install PySide6
```

No Linux ou macOS:

```bash
python3 -m pip install PySide6
```

---

## Abrindo o gerenciador

Abra um terminal na pasta principal do projeto.

No Windows:

```powershell
py question_bank_manager.py
```

No Linux ou macOS:

```bash
python3 question_bank_manager.py
```

Por padrão, o gerenciador abre a própria pasta onde o script está localizado. O caminho ativo aparece na parte superior da janela.

O botão **Selecionar pasta do banco** só é necessário quando você deseja trabalhar em outra cópia do banco.

---

# Como adicionar uma questão

## 1. Abra a guia “Criar questão”

Preencha os campos do formulário.

| Campo | Como preencher |
|---|---|
| **Colaborador** | Apelido ou codinome do colaborador. Nunca use seu nome real. |
| **Disciplina** | Nome completo da disciplina. Prefira uma opção já existente na lista. |
| **Código da disciplina** | Código institucional da disciplina. Confira se corresponde à disciplina escolhida. |
| **Professor** | Codinome do professor. Consulte a administração caso tenha dúvida. |
| **Período** | Período acadêmico, por exemplo `2026.1`. |
| **Avaliação** | Número da avaliação, como `1`, `2` ou `3`. |
| **Tag da questão** | Título curto que identifique o assunto principal da questão. |
| **Conteúdos** | Assuntos relacionados, um por linha. |
| **Quantidade inicial de respostas** | Número de arquivos de resposta que devem ser criados. Pode ser zero. |

As caixas de colaborador, disciplina, código, professor e período são editáveis. Elas também apresentam valores já encontrados no banco para reduzir diferenças de escrita.

Antes de criar, confira a **prévia do nome da pasta** exibida pelo gerenciador.

## 2. Clique em “Criar questão”

O gerenciador cria automaticamente:

- uma pasta exclusiva para a questão;
- um identificador curto e único;
- o arquivo `metadata.json`;
- o arquivo vazio `question.md`;
- os arquivos vazios `answer_01.md`, `answer_02.md` e seguintes, conforme a quantidade selecionada;
- a entrada correspondente em `questions/index.json`.

> [!WARNING]
> A mensagem “Questão criada com sucesso” significa apenas que a estrutura foi criada. O enunciado e as respostas ainda estarão vazios.

## 3. Abra a pasta criada

A pasta estará dentro de:

```text
questions/
```

Abra o arquivo:

```text
question.md
```

Escreva ou cole nele o enunciado completo da questão.

Depois, abra cada arquivo de resposta:

```text
answer_01.md
answer_02.md
...
```

Preencha manualmente cada resposta.

---

# Como escrever os arquivos Markdown

O conteúdo é escrito em Markdown comum.

## Exemplo de enunciado

```markdown
## Questão 1 — Estruturas de dados

Considere a árvore apresentada na imagem abaixo.

![Árvore usada na questão](arvore.png)

Explique quais rotações são necessárias para balanceá-la.
```

## Exemplo de resposta

```markdown
## Resposta

O primeiro nó desbalanceado possui fator de balanceamento `+2`.

Como a inserção ocorreu na subárvore direita do filho esquerdo, deve ser aplicada uma rotação dupla:

1. rotação à esquerda no filho;
2. rotação à direita no nó desbalanceado.
```

## Elementos úteis

````markdown
# Título principal
## Seção
### Subseção

**texto em negrito**
*texto em itálico*

- item de lista
- outro item

1. primeiro passo
2. segundo passo

`código curto`

```java
public class Exemplo {
}
```
````

---

# Como adicionar imagens

A imagem precisa estar dentro da pasta da própria questão ou em uma subpasta localizada nela.

Exemplo com a imagem na mesma pasta do `question.md`:

```markdown
![Descrição da imagem](janela1.jpeg)
```

Exemplo com uma subpasta `images`:

```markdown
![Diagrama do autômato](images/automato.png)
```

Use nomes simples para os arquivos, preferencialmente em letras minúsculas, sem espaços e sem caracteres especiais:

```text
questao_01.png
diagrama_avl.jpg
tela_programa.jpeg
```

Não use um caminho absoluto do computador, como:

```text
C:\Users\usuario\Desktop\imagem.png
```

Esse caminho funcionaria apenas no computador de quem escreveu o arquivo. Use sempre um caminho relativo à pasta da questão.

## Inserção pelo próprio VS Code

Versões atuais do VS Code permitem:

- copiar uma imagem e colá-la em um arquivo Markdown;
- arrastar uma imagem para o editor Markdown;
- usar o comando **Markdown: Insert Image from Workspace**;
- visualizar o resultado pelo modo de pré-visualização.

Documentação oficial:

- [Markdown no Visual Studio Code](https://code.visualstudio.com/docs/languages/markdown)

No Windows, use:

- `Ctrl + Shift + V` para abrir a pré-visualização;
- `Ctrl + K` e depois `V` para abrir a pré-visualização ao lado do editor.

Depois de colar uma imagem, confirme que o arquivo foi salvo dentro da pasta da questão e que o caminho inserido no Markdown é relativo.

## Extensão opcional

Caso o recurso nativo não funcione adequadamente no seu ambiente, uma alternativa é instalar uma extensão voltada à colagem de imagens, por exemplo:

- [Paste Image MD](https://marketplace.visualstudio.com/items?itemName=mav-works.paste-image-md)

Esse tipo de extensão salva a imagem da área de transferência como arquivo e insere automaticamente a referência Markdown. Confira a pasta de destino configurada pela extensão antes de enviar a contribuição.

---

# Fotografias de questões

É permitido adicionar uma fotografia ou captura de tela da questão.

Procedimento recomendado:

1. salve a imagem dentro da pasta da questão;
2. use um nome de arquivo simples;
3. insira a imagem no `question.md`;
4. sempre que possível, também transcreva o texto do enunciado.

Exemplo:

```markdown
## Questão fotografada

![Fotografia do enunciado](foto_enunciado.jpg)

### Transcrição

Digite aqui o conteúdo textual da questão.
```

A transcrição facilita buscas, seleção de texto, acessibilidade e futuras correções.

Antes de adicionar uma fotografia, remova ou recorte informações pessoais, como nomes de alunos, matrículas, assinaturas, e-mails e outros dados que não sejam necessários para compreender a questão.

---

# Criando o `question.md` a partir de fotos com o Gemini

O procedimento abaixo apresenta um exemplo de uso do Gemini para transformar fotografias de uma prova em arquivos Markdown. A ferramenta de IA auxilia na transcrição e na organização, mas o conteúdo gerado deve ser comparado com as imagens originais antes de ser salvo.

## 1. Prepare as fotografias

Antes de enviá-las ao Gemini:

1. fotografe ou digitalize todas as páginas necessárias da prova;
2. organize as imagens na ordem correta;
3. confirme que o texto está legível;
4. recorte ou oculte nomes, matrículas, assinaturas e outros dados pessoais;
5. mantenha separadas as imagens, gráficos ou diagramas que serão inseridos manualmente no `question.md`.

É possível enviar todas as páginas da prova de uma vez. Depois disso, trabalhe uma questão por vez, informando claramente o número ou o trecho que deve ser processado.

## 2. Gere primeiro a tag da questão

Antes de criar a estrutura no gerenciador, peça ao Gemini uma identificação curta para a questão. Essa saída será usada no campo **Tag da questão**.

Prompt de exemplo:

```text
Analise a questão [NÚMERO DA QUESTÃO] presente nas imagens enviadas.

Resuma, em uma única linha e com poucas palavras, o assunto principal e o que a questão solicita.

A resposta será usada como tag de identificação da questão.

Responda somente com a tag, sem explicações, sem introdução, sem aspas e sem pontuação final.
```

Exemplos de saída:

```text
balanceamento de árvore AVL
```

```text
cálculo de campo elétrico
```

```text
interseção de autômatos finitos
```

Copie a frase gerada e cole no campo **Tag da questão** do gerenciador. Depois, preencha os demais metadados e crie a estrutura da questão.

## 3. Peça a transcrição em Markdown

Após criar a pasta da questão, solicite ao Gemini somente o conteúdo que será colocado no arquivo `question.md`.

Prompt de exemplo:

```text
Com base nas imagens da prova enviadas anteriormente, transcreva somente a questão [NÚMERO DA QUESTÃO] para Markdown.

Siga estas regras:

- preserve o texto e o sentido original do enunciado;
- preserve a ordem dos parágrafos, itens, subitens e alternativas;
- represente corretamente fórmulas, símbolos, tabelas e trechos de código;
- corrija somente erros evidentes causados pela leitura da imagem, sem reescrever a questão;
- não resolva a questão;
- não acrescente explicações, observações ou comentários;
- não escreva frases como “Aqui está o Markdown”;
- não coloque a resposta dentro de um bloco cercado por ```markdown;
- entregue somente o Markdown final, pronto para ser copiado e colado no arquivo question.md;
- quando algum trecho não estiver legível, marque-o como [trecho ilegível] em vez de inventar o conteúdo.
```

O objetivo é fazer com que a resposta do Gemini comece diretamente pelo conteúdo do enunciado. Assim, basta usar o botão de copiar da ferramenta e colar o resultado no `question.md`.

## 4. Trate imagens, gráficos e diagramas separadamente

Quando a questão contiver uma figura que será salva manualmente, adicione ao prompt anterior, quando necessário, o seguinte trecho opcional:

```text
Quando houver uma imagem, gráfico ou diagrama, indique sua posição no enunciado usando uma referência Markdown no formato:

![Descrição breve da imagem](nome_da_imagem.png)

Não tente recriar visualmente a imagem. Uma descrição objetiva pode ser adicionada apenas quando ajudar a compreender o conteúdo.
```

Esse trecho pode ser removido do prompt quando não for necessário que o Gemini descreva ou marque a imagem.

Depois da transcrição:

1. copie ou recorte a figura original da fotografia;
2. cole a imagem no `question.md` pelo recurso do VS Code ou pela extensão configurada;
3. confirme que o arquivo da imagem foi salvo dentro da pasta da questão;
4. substitua o nome provisório pelo caminho relativo correto;
5. mantenha uma descrição curta no texto alternativo da imagem.

Exemplo:

```markdown
Considere a árvore apresentada abaixo:

![Árvore AVL usada no enunciado](arvore_avl.png)

Determine quais rotações devem ser realizadas.
```

A descrição textual pode complementar a figura, mas não deve substituir informações visuais indispensáveis sem uma revisão manual.

## 5. Copie, cole e revise

Para cada questão da prova:

1. peça a tag curta;
2. copie a tag para o gerenciador;
3. crie a estrutura da questão;
4. peça a transcrição em Markdown;
5. copie somente a resposta gerada;
6. cole o conteúdo no `question.md` correspondente;
7. insira manualmente as imagens necessárias;
8. abra a pré-visualização Markdown no VS Code;
9. compare o resultado com a fotografia original;
10. corrija erros de transcrição, fórmulas, alternativas e caminhos de imagens.

Repita o processo até que todas as questões tenham sido cadastradas.

> [!IMPORTANT]
> A IA deve ser usada como ferramenta de transcrição e formatação. A versão publicada deve ser revisada por uma pessoa, principalmente quando houver fórmulas, símbolos, código, tabelas ou imagens com baixa qualidade.

---

# Respostas produzidas com auxílio de IA

Uma resposta pode ser inicialmente obtida com o auxílio de ChatGPT, Gemini, Copilot ou outro sistema semelhante.

Ela deve ser tratada como um rascunho, não como uma resposta automaticamente correta.

Antes de salvar:

1. confira todos os cálculos, conceitos, códigos e referências;
2. remova comentários desnecessários da conversa com o chatbot;
3. adapte o texto para responder diretamente à questão;
4. organize o conteúdo em Markdown;
5. teste códigos quando houver código executável;
6. não inclua dados pessoais no prompt ou no arquivo final;
7. não apresente como certeza algo que não foi verificado.

Quando existirem soluções diferentes, coloque cada solução em um arquivo separado:

```text
answer_01.md
answer_02.md
answer_03.md
```

Uma resposta pode apresentar uma solução direta, enquanto outra pode explicar o raciocínio, mostrar um algoritmo alternativo ou corrigir uma resposta anterior.

---

# Como modificar uma questão existente

## Alterar os metadados

1. abra o gerenciador;
2. entre na guia **Editar questão**;
3. selecione a questão na lista;
4. altere os campos necessários;
5. clique em **Salvar alterações**.

Ao salvar, o gerenciador pode renomear automaticamente a pasta da questão e sincronizar o `questions/index.json`.

Prefira alterar os metadados pelo gerenciador em vez de editar o `metadata.json` manualmente.

## Alterar o enunciado ou uma resposta

Edite diretamente os arquivos Markdown da pasta:

```text
question.md
answer_01.md
answer_02.md
...
```

O gerenciador não oferece um editor para o conteúdo desses arquivos.

## Adicionar uma nova resposta

1. abra a guia **Editar questão**;
2. selecione a questão;
3. clique em **+ Adicionar resposta**;
4. clique em **Salvar alterações**;
5. abra o novo arquivo `answer_XX.md` criado na pasta;
6. escreva a resposta manualmente.

## Remover uma resposta

1. selecione o arquivo na lista de respostas;
2. clique em **- Remover resposta**;
3. confirme a operação;
4. clique em **Salvar alterações**.

> [!CAUTION]
> Ao salvar, o arquivo removido será excluído da pasta. Verifique seu conteúdo antes de confirmar.

---

# Reconstrução do indexador

Use o botão **Reconstruir indexador** quando:

- uma pasta de questão foi copiada manualmente para `questions/`;
- o arquivo `questions/index.json` ficou desatualizado;
- metadados foram alterados fora do gerenciador;
- uma questão não aparece na página ou na lista do gerenciador;
- for necessário padronizar novamente os nomes das pastas.

O reconstrutor:

1. percorre as subpastas de `questions/`;
2. procura um `metadata.json` válido;
3. calcula o nome esperado da pasta;
4. renomeia pastas fora do padrão, quando possível;
5. gera novamente o `questions/index.json`.

Pastas sem `metadata.json` são ignoradas. Conflitos de nomes ou metadados incompletos são apresentados como erros.

Também é possível executar o reconstrutor pelo terminal:

No Windows:

```powershell
py rebuild_the_indexer.py
```

No Linux ou macOS:

```bash
python3 rebuild_the_indexer.py
```

---

# Visualizando o banco no navegador

**Versão online disponível em:** https://gabrieljsantos.github.io/Question-Bank-UFS-SI/

A página não deve ser aberta apenas com um clique duplo no `index.html`, pois o navegador precisa carregar os arquivos por HTTP.

Na pasta principal do projeto, execute:

No Windows:

```powershell
py -m http.server 8000
```

No Linux ou macOS:

```bash
python3 -m http.server 8000
```

Depois, abra:

```text
http://localhost:8000
```

A página principal organiza as questões por:

1. disciplina e código;
2. professor e período/turma;
3. avaliação;
4. tag e ID da questão.

Ao abrir uma questão, a página mostra os metadados, o enunciado e as respostas cadastradas.

---

# Fluxo recomendado para colaborar

1. atualize sua cópia do repositório;
2. execute o gerenciador;
3. escolha um codinome de colaborador que não revele seu nome;
4. use o codinome correto do professor;
5. crie a estrutura da questão;
6. abra a nova pasta em `questions/`;
7. preencha o `question.md`;
8. preencha os arquivos `answer_XX.md`;
9. adicione as imagens dentro da pasta da questão;
10. confira a pré-visualização Markdown no VS Code;
11. reconstrua o indexador;
12. abra a página local e confirme que tudo foi carregado corretamente;
13. revise os arquivos alterados antes de enviar a contribuição.

---

# Checklist antes de enviar

- [ ] Usei um apelido ou codinome no campo de colaborador.
- [ ] Não coloquei meu nome, matrícula ou e-mail nos metadados.
- [ ] Usei o codinome correto do professor.
- [ ] Consultei a administração quando tive dúvida sobre o professor.
- [ ] Preenchi o `question.md`, que inicialmente foi criado vazio.
- [ ] Preenchi todos os arquivos `answer_XX.md` necessários.
- [ ] Revisei respostas produzidas com auxílio de IA.
- [ ] Coloquei imagens dentro da pasta da questão.
- [ ] Usei caminhos relativos nas imagens.
- [ ] Removi informações pessoais de fotografias e capturas de tela.
- [ ] Testei a renderização da questão no navegador.
- [ ] Reconstruí o indexador e conferi se não houve erros.

---

## Resumo essencial

O gerenciador administra a **estrutura e os metadados**. O colaborador administra o **conteúdo**.

```text
Gerenciador → cria arquivos vazios
VS Code     → recebe o enunciado, as respostas e as imagens
Página Web  → exibe o material organizado
```