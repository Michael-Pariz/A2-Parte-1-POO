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
