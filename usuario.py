from abc import ABC, abstractmethod

#Superclasse Usuario
class Usuario(ABC):
    def __init__(self, ra, nome):
        self._ra = ra
        self._nome = nome
        self._historico = []
        self._duracao_bloqueio = None

    #Getters
    @property
    def ra(self):
        return self._ra

    @property
    def nome(self):
        return self._nome

    @property
    def historico(self):
        return self._historico

    @property
    def duracao_bloqueio(self):
        return self._duracao_bloqueio

    #Numero de emprestimos realizados
    def emprestimos(self, emprestimo):
        self._historico.append(emprestimo)

    
    #Numero de emprestimos realizados
    def emprestimos(self, emprestimo):
        self._historico.append(emprestimo)

    #Função para bloquear o usuario.
    def bloqueio(self, data_bloqueio):
        if self._duracao_bloqueio is None or data_bloqueio > self._duracao_bloqueio:
            self._duracao_bloqueio = data_bloqueio

    #função para verificar se o usuario está bloqueado.
    def esta_bloqueado(self, data_atual):
        if self._duracao_bloqueio is None:
            return False
        return data_atual <= self._duracao_bloqueio

    @abstractmethod
    def limite_itens(self):
        pass

class Aluno(Usuario):
    def limite_itens(self):
        return 2

class Servidor(Usuario):
    def limite_itens(self):
        return 4

class Diretor(Usuario):
    def limite_itens(self):
        return 0
