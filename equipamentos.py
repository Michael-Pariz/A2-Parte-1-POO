from abc import ABC, abstractmethod
from datetime import timedelta

#Superclasse abstrata Equipamento
class Equipamento(ABC):
    def __init__(self,id,nome):
        self._id = id
        self._nome = nome
        self._disponivel = True


    #Getters
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def disponivel(self):
        return self._disponivel

    #Metodo para calcular o prazo de devolução, o pass serve para que cada subclasse tenha sua própria implementação do método
    @abstractmethod
    def calcular_prazo(self,devolucao): 
        pass   

#Subclasses
class Bola(Equipamento):
    def calcular_prazo(self, devolucao):
        return devolucao.replace(
            hour=23, minute=59, second=59, microsecond=0
        )

class Colete(Equipamento):
    def calcular_prazo(self, devolucao):
        return devolucao.replace(
            hour=23, minute=59, second=59, microsecond=0
        )

class Raquete(Equipamento):
    def calcular_prazo(self, devolucao):
        return (devolucao + timedelta(days=2)).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0
        )

class Bicicleta(Equipamento):
    def calcular_prazo(self, devolucao):
        return (devolucao + timedelta(days=7)).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0
        )
