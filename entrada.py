from datetime import datetime

from datas import FORMATO_DATA


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Este campo não pode ficar vazio.")


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("Valor inválido. Digite apenas números.")
            continue

        if minimo is not None and valor < minimo:
            print(f"O número deve ser no mínimo {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"O número deve ser no máximo {maximo}.")
        else:
            return valor


def ler_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta == "s" or resposta == "sim":
            return True
        if resposta == "n" or resposta == "nao" or resposta == "não":
            return False
        print("Responda com s (sim) ou n (não).")


def ler_data(mensagem):
    while True:
        texto = input(mensagem).strip()
        try:
            return datetime.strptime(texto, FORMATO_DATA).date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa, por exemplo 25/10/2026.")


def escolher(titulo, opcoes):
    # mostra as opções numeradas e devolve a posição escolhida na lista (começa em 0)
    print(titulo)
    for i in range(len(opcoes)):
        print(f"  {i + 1} - {opcoes[i]}")
    numero = ler_inteiro("Opção: ", 1, len(opcoes))
    return numero - 1
