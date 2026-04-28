# Projeto_computacao_grafica

## O que é este projeto?

Este é um programa de **computação gráfica** que cria imagens realistas em 3D usando uma técnica chamada **Ray Tracing** (traçado de raios). Pense nele como uma câmera virtual: em vez de tirar uma foto do mundo real, ele "desenha" uma cena virtual calculando como a luz se comporta em um ambiente imaginário.

---

## Conceito Principal: Como funciona o Ray Tracing?

O Ray Tracing simula o caminho da luz de forma **invertida** ao que acontece na realidade:

1. **Na vida real**: A luz sai de uma fonte (como uma lâmpada), bate nos objetos, e parte dessa luz chega aos nossos olhos.
2. **No Ray Tracing**: O programa faz o oposto — ele "dispara" raios imaginários **da câmera**, passando por cada pixel da imagem, em direção à cena 3D.

Quando um raio atinge um objeto, o programa calcula:
- **Qual objeto foi atingido?** (uma esfera, um plano, uma caixa...)
- **De onde vem a luz?** (há uma fonte de luz iluminando esse ponto?)
- **O ponto está na sombra?** (algum outro objeto está bloqueando a luz?)
- **Qual a cor do objeto?** (o material pode ser vermelho fosco, metálico brilhante, etc.)

Com essas informações, o programa decide **qual cor cada pixel da imagem deve ter**. O resultado é uma imagem fotorrealista com iluminação, sombras e reflexos realistas.

---

## Renderização Progressiva: Os Passos do Projeto

A grande sacada deste projeto é que ele não gera a imagem final de uma só vez. Ele evolui **passo a passo**, onde cada passo adiciona um novo recurso visual ao anterior. Isso permite ver exatamente como cada técnica melhora a imagem.

### Passo 1 — Esfera vermelha simples (sem sombras)
**O que acontece**: Uma esfera vermelha aparece sobre um plano cinza, iluminada por uma única fonte de luz pontual.  
**O que ainda não tem**: Nenhum cálculo de sombra — mesmo áreas que deveriam estar escuras ficam iluminadas.  
**Analogia**: Imagine uma bola vermelha em uma sala onde a luz "mágica" ilumina tudo igualmente, sem criar sombras no chão.

### Passo 1.5 — Adicionando sombras
**O que muda**: Agora o programa verifica se algo está bloqueando a luz entre a fonte de luz e o objeto. Se estiver, aquele ponto fica escuro (na sombra).  
**Resultado**: A esfera começa a projetar uma sombra dura e bem definida no plano.

### Passo 2 — Modelo de iluminação Phong
**O que muda**: Em vez de apenas pintar a esfera de vermelho, o programa agora calcula a iluminação de forma mais sofisticada usando o **modelo Phong**, que considera três componentes:
- **Ambiente**: Uma luz base que ilumina tudo minimamente (simula a luz indireta do ambiente).
- **Difusa**: A luz que bate no objeto e se espalha em todas as direções (é o que dá cor ao objeto).
- **Especular**: Os brilhos pontuais que aparecem em superfícies lisas (como o reflexo em uma bola de metal).

**Resultado**: A esfera agora parece um objeto 3D real, com gradientes de luz e um brilho especular que dá a sensação de profundidade.

### Passo 3 — Antialiasing (suavização de bordas)
**O problema**: Sem antialiasing, as bordas dos objetos ficam serrilhadas, parecendo "degraus" (o famoso efeito *aliasing*).  
**A solução**: Em vez de disparar **um único raio** por pixel, o programa dispara **vários raios** levemente deslocados dentro do mesmo pixel e faz uma média das cores.  
**Resultado**: As bordas ficam suaves e naturais, sem o efeito de "escadinha".

### Passo 3.1 — Duas fontes de luz
**O que muda**: Adiciona-se uma segunda fonte de luz pontual.  
**Resultado**: Agora os objetos projetam **duas sombras**, uma para cada luz — similar a quando você está em uma sala com duas lâmpadas.

### Passo 4 — Luz de área (sombras suaves)
**O que muda**: Em vez de uma fonte de luz pontual (um ponto minúsculo), o programa usa uma **luz de área** — uma superfície retangular que emite luz.  
**Por que isso importa**: Na vida real, sombras raramente têm bordas duras e perfeitas. Quanto mais próximo você está da sombra, mais nítida ela é; quanto mais longe, mais borrada. Luzes de área reproduzem esse efeito naturalmente.  
**Resultado**: As sombras agora têm **bordas suaves e graduais**, muito mais realistas.

### Passo 5 — Elipsoide + mais amostras de luz
**O que muda**: A esfera é substituída por um **elipsoide** (uma esfera esticada, parecida com um ovo). Isso demonstra que a matemática do programa funciona para formas além de esferas perfeitas. Também aumenta a quantidade de cálculos de luz para melhorar a qualidade.  
**Resultado**: Um objeto com formato diferente aparece na cena, provando que o sistema é flexível.

### Passo 6 — Luz de área com mais qualidade
**O que muda**: Mesmo conceito do passo 4, mas com **mais amostras** de luz.  
**Analogia**: É como se o programa "olhasse" para a luz de área mais vezes antes de decidir a cor final, resultando em uma imagem mais refinada.

### Passo 7 — Caixa (geometria de box)
**O que muda**: A esfera/elipsoide é substituída por uma **caixa** (um objeto retangular, como um dado).  
**Resultado**: Demonstra que o programa consegue lidar com objetos com faces planas e arestas vivas, não apenas formas curvas.

### Passo 8 — Caixa e Tetraedro Lado a Lado
**O que muda**: Adiciona-se uma nova primitiva de modelagem geométrica: o **Tetraedro**. A caixa e o tetraedro são renderizados simultaneamente na mesma cena.
**Resultado**: O sistema testa múltiplas interseções (raio-caixa e raio-triângulo) em objetos poliédricos, calculando as interações com a iluminação, sombras conjuntas sobre o plano e ordenação de profundidade no eixo z.

### Passo 9 — Cornell Box e Iluminação de Área Reflexiva
**O que muda**: Os objetos geométricos agora estão enclausurados em uma **Cornell Box** clássica simulada por múltiplos blocos/superfícies e iluminada exclusivamente de cima por uma luz retangular com poucas amostras.
**Resultado**: Renderiza tons limitados por um espaço fechado projetando cores laterais e sombras difusas resultantes da luz simulativamente limitada.

---

## Como o código está organizado?

O projeto segue uma estrutura organizada em camadas:

### 📁 Modelos (`src/models/`) — "As coisas na cena"
Aqui ficam as definições dos **objetos** que compõem a cena 3D:
- **Câmera**: Define de onde a imagem está sendo vista.
- **Objetos**: Esferas, elipsoides, planos, caixas.
- **Luzes**: Fontes de luz pontuais ou de área.
- **Materiais**: Define se uma superfície é fosca, brilhante, vermelha, etc.
- **Filme**: O "sensor" da câmera virtual — uma grade de 512×512 pixels onde a imagem é formada.

### 📁 Serviços (`src/services/`) — "Os algoritmos"
Aqui fica a **inteligência** do programa:
- **Interseção**: Calcula se um raio atingiu algum objeto.
- **Shading** (sombreamento): Calcula a cor final de cada pixel com base na iluminação.
- **Amostragem**: Gera raios extras para antialiasing e luzes de área.
- **Renderer** (renderizador): O motor principal — varre cada pixel, dispara raios e acumula cores.
- **Pipeline**: Orquestra tudo — decide qual passo renderizar, configura a cena e salva a imagem.

### 📁 Utilitários (`src/utils/`) — "Ferramentas"
Funções auxiliares, como salvar a imagem final como um arquivo PNG.

---

## Fluxo completo: do início ao fim

Quando você roda o programa, acontece o seguinte:

1. **Configuração**: O programa lê seus parâmetros (qual passo renderizar, qualidade, etc.).
2. **Montagem da cena**: Os objetos, luzes e câmera são posicionados.
3. **Renderização**: Para cada pixel da imagem:
   - Um ou mais raios são disparados da câmera.
   - O programa verifica qual objeto cada raio atingiu.
   - Calcula a cor com base na iluminação e sombras.
   - A cor é armazenada no "filme" da câmera.
4. **Pós-processamento**: As cores são ajustadas e limitadas a valores válidos.
5. **Salvamento**: A imagem é salva como um arquivo PNG.

---

## Tecnologias utilizadas

- **Python**: Linguagem principal.
- **NumPy**: Para cálculos matemáticos rápidos com vetores e matrizes.
- **PyGLM**: Biblioteca de matemática 3D (vetores, matrizes, transformações).
- **Pillow**: Para salvar as imagens como PNG.
- **pytest, ruff, mypy**: Ferramentas de teste e qualidade de código.

---

## Resumo visual

| Passo | Recurso adicionado | Resultado visual |
|-------|-------------------|------------------|
| 1 | Luz pontual, cor plana | Esfera vermelha sem sombras |
| 1.5 | Sombras | Sombras duras aparecem |
| 2 | Modelo Phong | Brilho e profundidade realistas |
| 3 | Antialiasing | Bordas suaves |
| 3.1 | Duas luzes | Múltiplas sombras |
| 4 | Luz de área | Sombras suaves e graduais |
| 5 | Elipsoide | Formato diferente |
| 6 | Mais amostras de luz | Qualidade superior |
| 7 | Caixa | Objetos com arestas |
| 8 | Tetraedro e múltiplas primitivas | Caixa e Tetraedro lado a lado com profundidade |
| 9 | Cornell Box | Geometria multi-faces fechada e iluminação de área |

---

## Conclusão

Este projeto é uma **demonstração educativa** de como funciona a renderização 3D por Ray Tracing. Ao invés de pular direto para a imagem final complexa, ele constrói o entendimento passo a passo — assim como se aprende a desenhar começando com formas simples e gradualmente adicionando detalhes, sombras e texturas.

Cada passo é uma peça do quebra-cabeça que, junta, forma uma imagem realista gerada inteiramente por matemática e algoritmos.
