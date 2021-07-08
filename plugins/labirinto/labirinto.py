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
    5 = 4 + 1 = jogador no sentido Sul + sala ou corredor
    """

    mapa_binarios = [[0, 0, 0, 17, 0],
                     [0, 0, 0, 1, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 1, 1, 1],
                     [0, 0, 0, 0, 0]]

    # https://stackoverflow.com/a/10411108/5167118
    def converter_inteiro_para_binario(self, inteiro):
        """
        Converter número inteiro em string de 32 bits.
        """
        return f'{inteiro:032b}'

    def sentido_do_jogador(self, binario):
        """
        Informar a orientação do jogador em relação ao mapa:
        - Norte (N)
        - Sul (S)
        - Oeste (O)
        - Leste (L)
        """

        sentido = self.converter_inteiro_para_binario(binario)[27:31]
        """
        Os sentidos estão organizados por bit,
        a contar da direita para a esquerda:
        - N: bit 30
        - S: bit 29
        - O: bit 28
        - L: bit 27
        Como o Python usa limite fechado a esquerda e aberto a direita,
        o intervalo vai de 27 (inclui) a 31 (não inclui).
        """
        if sentido == '0001':
            return "N"
        elif sentido == '0010':
            return "S"
        elif sentido == '0100':
            return "O"
        elif sentido == '1000':
            return "L"

    @re_botcmd(pattern=r"^(.*)mapa(.*)$")
    def mapa(self, msg, match):
        """
        Apresentar o mapa no bot.
        """

        for linha in self.mapa_binarios:
            yield " ".join(map(str, linha))

    @re_botcmd(pattern=r"^(.*)sentido(.*)$")
    def jogador(self, msg, match):
        """
        Informar a sentido do jogador como ponto cardeal.
        """

        for linha in self.mapa_binarios:
            for celula in linha:
                sentido = self.sentido_do_jogador(celula)
                if sentido:
                    return sentido

    @re_botcmd(pattern=r"^(.*)[direita|esquerda](.*)$")
    def vira(self, msg, match):
        pass