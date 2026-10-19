from math import ceil

from data import formatar_data_hora
from excecoes import ErroAtletica

#Classe Empréstimo
class Emprestimo:
    def __init__(self, usuario, equipamento, retirada):
        self._usuario = usuario
        self._equipamento = equipamento
        self._retirada = retirada
        #o prazo depende do tipo do equipamento (polimorfismo)
        self._prazo_devolucao = equipamento.calcular_prazo(retirada)
        self._devolucao = None
        self._dias_atraso = 0
        self._vistoria = None
        self._danificado = False

    #Getters
    @property
    def usuario(self):
        return self._usuario

    @property
    def equipamento(self):
        return self._equipamento

    @property
    def retirada(self):
        return self._retirada

    @property
    def prazo_devolucao(self):
        return self._prazo_devolucao

    @property
    def devolucao(self):
        return self._devolucao

    @property
    def dias_atraso(self):
        return self._dias_atraso

    @property
    def vistoria(self):
        return self._vistoria

    @property
    def danificado(self):
        return self._danificado

    #Função para verificar se o empréstimo está ativo ou não
    def esta_ativo(self):
        return self._devolucao is None

    #Calcula quantos dias de atraso existem até uma data
    #Pega a quantidade de segundos depois do prazo e converte para dias, arredondando para cima
    #com ceil, e garantindo que seja no minimo 1 dia
    def _calcular_atraso(self, data):
        if data <= self._prazo_devolucao:
            return 0
        segundos_atraso = (data - self._prazo_devolucao).total_seconds()
        return max(1, ceil(segundos_atraso / 86400))

    #Atraso até agora, para saber quem está atrasado antes de devolver
    def atraso_atual(self, data_atual):
        if not self.esta_ativo():
            return self._dias_atraso
        return self._calcular_atraso(data_atual)

    def devolver(self, data_devolucao, vistoria=None, danificado=False):

        #verifica se o empréstimo já foi devolvido ou não
        if not self.esta_ativo():
            raise ErroAtletica("Empréstimo já foi devolvido.")

        if data_devolucao < self._retirada:
            raise ErroAtletica("Data de devolução não pode ser anterior à data de retirada.")

        #verifica se o equipamento precisa de vistoria e se a vistoria foi realizada ou não
        if self._equipamento.precisa_vistoria() and vistoria is None:
            raise ErroAtletica("Vistoria é obrigatória para devolução deste equipamento.")

        self._devolucao = data_devolucao
        self._vistoria = vistoria
        self._dias_atraso = self._calcular_atraso(data_devolucao)

        #se teve vistoria, ela decide se está danificado; se não, vale o que foi informado
        if vistoria is not None:
            self._danificado = vistoria.esta_danificada()
        else:
            self._danificado = danificado

        return self._dias_atraso

    def estado_devolucao(self):
        if self._vistoria is not None:
            return str(self._vistoria)
        if self._danificado:
            return "devolvido danificado"
        return "sem danos"

    #Texto com as informações do empréstimo, usado nas listagens do menu
    def resumo(self, data_atual):
        texto = f"{self._equipamento} | com {self._usuario.nome}"
        texto = texto + f" | retirada {formatar_data_hora(self._retirada)}"
        texto = texto + f" | prazo {formatar_data_hora(self._prazo_devolucao)}"

        if self.esta_ativo():
            atraso = self.atraso_atual(data_atual)
            if atraso > 0:
                texto = texto + f" | ATRASADO {atraso} dia(s)"
            else:
                texto = texto + " | em aberto"
        else:
            texto = texto + f" | devolvido {formatar_data_hora(self._devolucao)}"
            if self._dias_atraso > 0:
                texto = texto + f" | {self._dias_atraso} dia(s) de atraso"
            texto = texto + " | " + self.estado_devolucao()
        return texto
