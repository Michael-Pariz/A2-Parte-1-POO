from abc import ABC, abstractmethod

from data import formatar_data_hora
from excecoes import ErroAtletica

#Superclasse Usuario
class Usuario(ABC):
    def __init__(self, ra, nome):
        self._ra = ra
        self._nome = nome
        self._historico = []
        self._bloqueado_ate = None

    #Getters
    @property
    def ra(self):
        return self._ra

    @property
    def nome(self):
        return self._nome

    #Devolve uma cópia para a lista não ser alterada por fora da classe
    @property
    def historico(self):
        return self._historico.copy()

    @property
    def bloqueado_ate(self):
        return self._bloqueado_ate

    #Cada subclasse informa o seu tipo e quantos itens pode ter ao mesmo tempo
    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def limite_itens(self):
        pass

    #Adiciona um empréstimo ao histórico do usuário
    def adicionar_emprestimo(self, emprestimo):
        self._historico.append(emprestimo)

    #Retorna só os empréstimos que ainda não foram devolvidos
    def emprestimos_ativos(self):
        ativos = []
        for emprestimo in self._historico:
            if emprestimo.esta_ativo():
                ativos.append(emprestimo)
        return ativos

    #Função para bloquear o usuario até uma data. Se já tiver um bloqueio maior, mantém o maior.
    def bloqueio(self, data_bloqueio):
        if self._bloqueado_ate is None or data_bloqueio > self._bloqueado_ate:
            self._bloqueado_ate = data_bloqueio

    #função para verificar se o usuario está bloqueado.
    def esta_bloqueado(self, data_atual):
        if self._bloqueado_ate is None:
            return False
        return data_atual <= self._bloqueado_ate

    #função para verificar se o usuario está com algum item atrasado agora
    def tem_item_atrasado(self, data_atual):
        for emprestimo in self.emprestimos_ativos():
            if emprestimo.atraso_atual(data_atual) > 0:
                return True
        return False

    #Verifica as regras antes de emprestar. Se alguma não for cumprida, lança ErroAtletica.
    def verificar_pode_emprestar(self, data_atual):
        if self.esta_bloqueado(data_atual):
            raise ErroAtletica(f"{self._nome} está bloqueado(a) por atraso até "
                               f"{formatar_data_hora(self._bloqueado_ate)}.")
        if self.tem_item_atrasado(data_atual):
            raise ErroAtletica(f"{self._nome} está com um item atrasado. "
                               f"Registre a devolução antes de emprestar outro.")
        quantidade = len(self.emprestimos_ativos())
        if quantidade >= self.limite_itens():
            raise ErroAtletica(f"{self._nome} já está com {quantidade} item(ns). "
                               f"O limite para {self.tipo().lower()} é {self.limite_itens()}.")

    def total_devolucoes_com_atraso(self):
        total = 0
        for emprestimo in self._historico:
            if not emprestimo.esta_ativo() and emprestimo.dias_atraso > 0:
                total = total + 1
        return total

    def total_devolucoes_danificadas(self):
        total = 0
        for emprestimo in self._historico:
            if not emprestimo.esta_ativo() and emprestimo.danificado:
                total = total + 1
        return total

    def situacao(self, data_atual):
        if self.esta_bloqueado(data_atual):
            return f"bloqueado(a) até {formatar_data_hora(self._bloqueado_ate)}"
        return "liberado(a)"

    def __str__(self):
        return f"{self._nome} ({self.tipo()} - RA {self._ra})"

class Aluno(Usuario):
    def tipo(self):
        return "Aluno"

    def limite_itens(self):
        return 2

class Servidor(Usuario):
    def tipo(self):
        return "Servidor"

    def limite_itens(self):
        return 4
