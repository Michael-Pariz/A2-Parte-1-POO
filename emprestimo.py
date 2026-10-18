from datetime import datetime
from equipamentos import Bicicleta

#Classe Empréstimo
class Emprestimo:
    def __init__(self, usuario, equipamento, retirada):
        self._usuario = usuario
        self._equipamento = equipamento
        self._retirada = retirada
        self._prazo_devolucao = equipamento.calcular_prazo_devolucao(retirada)
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

    def devolver(self, data_devolucao, vistoria=None):
        
         #função para verificar se o empréstimo já foi devolvido ou não
        if not self.esta_ativo():
            raise ValueError("Empréstimo já foi devolvido.")

        
        if data_devolucao < self._retirada:
            raise ValueError("Data de devolução não pode ser anterior à data de retirada.")

        #verifica se o equipamento é uma bicicleta e se a vistoria foi realizada ou não
        if (
            isinstance(self._equipamento, Bicicleta) and vistoria is None
        ):
            raise ValueError("Vistoria é obrigatória para devolução de bicicleta.")

        self._devolucao = data_devolucao
        self._vistoria = vistoria

        #verifica se a devolução foi feita após o prazo de devolução e calcula os dias de atraso
        if data_devolucao > self._prazo_devolucao:
            self._dias_atraso = (data_devolucao - self._prazo_devolucao).days

        #verifica se a vistoria foi realizada e se o equipamento está danificado
        if vistoria is not None:
            self._danificado = vistoria.esta_danificada()

        return self._dias_atraso
