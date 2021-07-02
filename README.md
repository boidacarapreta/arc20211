[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/boidacarapreta/arc20211)

# Projeto da disciplina

O problema escolhido para este semestre é um _chatbot_ integrado ao Discord. Mais especificamente, um jogo baseado em texto inspirado nos clássicos e (muito) antigos jogos de computador.

## Referências

Nos anos 1990, tive acesso ao jogo [Indiana Jones and the Fate of Atlantis](https://en.wikipedia.org/wiki/Indiana_Jones_and_the_Fate_of_Atlantis), o primeiro de vários da LucasArts. Essa mistura de _point-and-click_ com ações textuais era bastante interessante: ao clicar em uma área da tela, havia um contexto de opções para selecionar. Foi, inclusive, o que me chamou a atenção quando vi o anúncio de [Backbone](https://store.steampowered.com/app/865610/Backbone/)... Porém, a ideia de usar imagens no bot me soou atrativa pelo efeito multimídia, mas eu imaginei algo ainda mais simples, mais apegado ao texto - dado o meu uso recorrente de [Twine](https://twinery.org) como ferramenta de trabalho e de [ensino](https://github.com/boidacarapreta/cab20202).

Há pouco tempo, ao ler [Jogador Número 1](http://www.leya.com.br/jogador-n-1/) - e depois assistir ao filme - tive uma onda de nostalgia, passando por [Adventure](<https://en.wikipedia.org/wiki/Adventure_(1980_video_game)>), onde as ações eram ainda mais simples: apenas texto. Estamos falando de Atari, afinal (CGA existia apenas nos computadores dos anos 1980 em diante, como por exemplo [The Ethernal castle [REMASTERED]](https://www.theeternalcastle.net)).

Assim, veio a ideia de resgatar uma ideia há muito adormecida: jogos de masmorra, _dungeon-like_, em texto puro. Vale arte ASCII, como [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). Mas, para chegar lá, usei mais referências como a minissérie [GDLK](https://www.netflix.com/title/81019087) e até em lançamentos recentes como [Stories Untold](https://storiesuntoldgame.com/trailer).

## Sobre o jogo

O jogo, baseado puramente em texto, é a fuga do jogador de um labirinto. Todas as ações do personagem são comandos relativamente flexíveis, como por exemplo:

```
porta
abrir a porta
girar a maçaneta da porta
avançar até a porta
empurrar a porta
```

que são opções possíveis para interagir com o objeto `porta`. O jogo, como parte da experiência de imersão, não diz quais comandos são aceitos (ao contrário dos menus contextuais), embora haja uma sugestão na descrição do ambiente. E quando digo imersão, é isto mesmo: o jogador deve experimentar, vasculhar, desvendar o ambiente onde está, usando - claro - apenas texto.

Falando em ambiente, o labirinto está dividido em salas e corredores, onde cada sala pode ter bens de inventário, como chaves e poções, e obstáculos como portas trancadas e monstros. Fugas ou lutas fazem parte, embora alguns monstros corram bastante!

Além disso, o labirinto é criado proceduralmente para cada rodada e para cada jogador. Entretanto, o progresso é salvado automaticamente: por tratar-se do Discord, pode-se começar num dispositivo e continuar em outro.

## Implementação

Este jogo foi pensado para ensinar programação **E** divertir (principalmente o [seu criador](https://github.com/boidacarapreta)). O mapa usará:

- Estruturas de dados simples para manipulação da informação, com ênfase em matrizes (vetores, ou _arrays_);
- Números binários para guardar informações por "pixel" do mapa;
- Salvamento em banco de dados (não relacional) externo;
- Integração com outras aplicações via APIs e _webhooks_.

Assim, ao longo da disciplina, o jogo ganhará complexidade de acordo com os conceitos vistos na disciplina. Inicialmente, será apenas uma matriz, ou um vetor de vetores com informação binária: `0` para parede e `1` para sala ou corredor, como por exemplo:

```
1 1 1 1 1 0 0
0 0 0 0 1 0 0
0 0 1 1 1 0 0
0 0 1 1 1 0 0
0 0 0 0 1 0 0
0 0 0 0 1 1 1
```

Partindo da primeira coluna e primeira linha, há uma sequência de `1` indicando o caminho para percorrer, com uma sala exatamente no meio do mapa (matriz 2 x 3 de valores `1`), terminando o caminho na última linha e última coluna.

O primeiro jogador (pode haver vários!) é representado por uma potência de 2, como por exemplo 2^8. Logo, na matriz:

```
1 1 257 1 1 0 0
0 0   0 0 1 0 0
0 0   1 1 1 0 0
0 0   1 1 1 0 0
0 0   0 0 1 0 0
0 0   0 0 1 1 1
```

o jogador está na primeira linha e terceira coluna, já que há o valor 257 = 256 + 1 = 2^8 + 2^0 = primeiro jogador + corredor/sala. É uma forma barata de armazenar, interessante de estudar e que permite muitas expansões:

- Potências de 2 entre 0 e 7 (primeiro byte): mapa;
- Potências de 2 entre 8 e 15 (segundo byte): jogadores;
- Potências de 2 entre 16 e 31 (terceiro byte): espada;
- Potências de 2 entre 32 e 47 (quarto byte): inimigos;

assim como inventário, pontos de ataque e de defesa, poções, magias etc. etc. Um pixel com valor 33025 = 32768 + 256 + 1 = 2^16 + 2^8 + 2^0 = espada + primeiro jogador + corredor/sala = primeiro personagem com espado no corredor/sala.

Mas calma! Primeiro um único mapa estático, um único jogador. Depois, mapas por jogador, mapas procedurais, e assim por diante.

Outra coisa importante: para não cansar a leitura, as frases e descrições serão escolhidas aleatoriamente de um banco de frases por tipo:

- Sucesso: "`Meus parabéns!`", "`Eis o novo campeão!`" e
- Morte: "`E finda a história deste bravo jogador`", "`Escreva "reiniciar" para invocar o jogador dos mortos`"

de forma que as descrições sejam mais dinâmicas.

Parece complicado apenas lendo a explicação deste jogo? Imagina jogá-lo usando apenas texto! Por isso usarei bastante o [kanban](https://github.com/boidacarapreta/arc20211/projects/1) para organizar as ideias.

# Equipes e repositórios

- [glass-queens](https://github.com/glass-queens): [arc](https://github.com/glass-queens/arc)
- [lasscampos](https://github.com/lasscampos): [ARC-2021](https://github.com/lasscampos/ARC-2021)
- [iftelecom](https://github.com/iftelecom): [arc21](https://github.com/iftelecom/arc21)
- [darkzone2](https://github.com/darkzone2): [ARC_20211_ChatBot](https://github.com/darkzone2/ARC_20211_ChatBot)
- [lasscampos](https://github.com/lasscampos): [ARC-2021](https://github.com/lasscampos/ARC-2021)
- [anaozuao](https://github.com/anaozuao): [ARC2021-1_Roberto](https://github.com/anaozuao/ARC2021-1_Roberto)
- [Vitor-1921](https://github.com/Vitor-1921): [ARC-8](https://github.com/Vitor-1921/ARC-8)
