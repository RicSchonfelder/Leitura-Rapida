import time
import os

def leitura_rapida(texto, velocidade=300):
    """
    Mostra palavras do texto sequencialmente no terminal para leitura rápida.

    :param texto: Texto completo a ser exibido palavra por palavra.
    :param velocidade: Velocidade em palavras por minuto (padrão: 300).
    """
    palavras = texto.split()  # Divide o texto em palavras
    intervalo = 60 / velocidade  # Calcula o intervalo entre palavras em segundos

    try:
        for palavra in palavras:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela para focar em uma palavra
            print(f"\n{palavra}\n")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\nLeitura interrompida pelo usuário.")

if __name__ == "__main__":
    texto = input("Insira o texto para leitura rápida: ")
    velocidade = int(input("Insira a velocidade em palavras por minuto (padrão: 300): ") or 300)
    leitura_rapida(texto, velocidade)
