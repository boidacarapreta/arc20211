from errbot import BotPlugin, re_botcmd
from random import randint


class Labirinto(BotPlugin):
    """
    Jogo de labirinto feito em matriz de números inteiros.
    O objetivo é fazer com que o jogador saia do labirinto,
    e para isso será preciso movimentar-se pelas salas e
    corredores.
    Internamente, o jogo implementa uma matriz de inteiros
    para armazenar informações como:
    - Parede: 0
    - Sala ou corredor: 1
    - Posição e sentido do jogador:
      -  2: sentido Norte
      -  4: sentido Sul
      -  8: sentido Oeste
      - 16: sentido Leste
    Assim, o mapa acumula informações com base nessas
    potências de dois, como por exemplo:
    17 = 16 + 1 = jogador no sentido Leste + sala ou corredor
    """

    mapa_inteiros = [[0, 0, 0, 17, 0],
                     [0, 0, 0, 1, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 1, 1, 1],
                     [0, 0, 0, 0, 0]]

    # https://stackoverflow.com/a/10411108/5167118
    def converter_inteiro_para_binario(self, inteiro):
        """
        Converter número inteiro em string de 32 bits.
        """

        return f"{inteiro:032b}"

    def posicao_do_jogador(self):
        """
        Informar a orientação do jogador em relação ao mapa:
        - Norte (N)
        - Sul (S)
        - Oeste (O)
        - Leste (L)
        """

        x = 0
        for linha in self.mapa_inteiros:
            y = 0
            for coluna in linha:
                sentido = self.converter_inteiro_para_binario(coluna)[27:31]
                """
                Os sentidos estão organizados por bit,
                a contar da direita para a esquerda:
                - N: bit 30 (2^1)
                - S: bit 29 (2^2)
                - O: bit 28 (2^3)
                - L: bit 27 (2^4)
                Como o Python usa limite fechado a esquerda e aberto a direita,
                o intervalo vai de 27 (inclui) a 31 (não inclui).
                """
                if sentido == "0001":
                    return x, y, "N"
                elif sentido == "0010":
                    return x, y, "S"
                elif sentido == "0100":
                    return x, y, "O"
                elif sentido == "1000":
                    return x, y, "L"
                y += 1
            x += 1

    def atualizar_posicao_do_jogador(self, rotação):
        """
        Atualizar a posição ou sentido do jogador no mapa,
        que por se tratar de uma matriz de inteiros é feita
        uma operação de soma/subtração nas células para
        atualizar os dados do jogador.
        """

        x, y, sentido = self.posicao_do_jogador()
        if rotação == "direita":
            if sentido == "N":
                """
                Norte -> Leste
                - 2 (N) + 16 (L)
                """
                rotacionar = +14
            elif sentido == "S":
                """
                Sul -> Oeste
                - 4 (S) + 8 (O)
                """
                rotacionar = +4
            elif sentido == "O":
                """
                Oeste -> Norte
                - 8 (O) + 2 (N)
                """
                rotacionar = -6
            else:
                """
                Último caso é Leste ("L")
                Leste -> Sul
                 - 16 (L) + 4 (S)
                """
                rotacionar = -12
        else:
            """
            Se a rotação não é para direita, então é esquerda
            """
            if sentido == "N":
                """
                Norte -> Oeste
                - 2 (N) + 8 (O)
                """
                rotacionar = +6
            elif sentido == "S":
                """
                Sul -> Leste
                - 4 (S) + 16 (L)
                """
                rotacionar = +12
            elif sentido == "O":
                """
                Oeste -> Sul
                - 8 (O) + 4 (S)
                """
                rotacionar = -4
            else:
                """
                Último caso é Leste ("L")
                Leste -> Norte
                - 16 (L) + 2 (N)
                """
                rotacionar = -14
        """
        Atualiza o mapa de inteiros e informa o usuário o novo sentido
        """
        self.mapa_inteiros[x][y] += rotacionar
        return self.posicao_do_jogador()

    @re_botcmd(pattern=r"^(.*)mapa(.*)$")
    def mapa(self, msg, match):
        """
        Apresentar o mapa no bot.
        """

        for linha in self.mapa_inteiros:
            yield " ".join(map(str, linha))

    @re_botcmd(pattern=r"^(.*)(eu|sentido)(.*)$")
    def jogador(self, msg, match):
        """
        Informar a sentido do jogador como ponto cardeal.
        """

        linha, coluna, sentido = self.posicao_do_jogador()
        yield "Posição no mapa: [" + str(linha) + "," + str(coluna) + "]"
        yield "Sentido (ponto cardeal): " + sentido

    @re_botcmd(pattern=r"^(.*)direita(.*)$")
    def direita(self, msg, match):
        """
        Rotacionar 90 graus o jogador para a direita - na sua perspectiva.
        """

        x, y, sentido = self.atualizar_posicao_do_jogador("direita")
        yield "Novo sentido: " + sentido

    @re_botcmd(pattern=r"^(.*)esquerda(.*)$")
    def esquerda(self, msg, match):
        """
        Rotacionar 90 graus o jogador para a esquerda - na sua perspectiva.
        """

        x, y, sentido = self.atualizar_posicao_do_jogador("esquerda")
        yield "Novo sentido: " + sentido
