from abc import ABC, abstractmethod
from datetime import timedelta

#Superclasse abstrata Equipamento
class Equipamento(ABC):
    def __init__(self, id, nome):
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

    #Métodos para mudar a disponibilidade quando o equipamento é emprestado ou devolvido
    def marcar_emprestado(self):
        self._disponivel = False

    def marcar_disponivel(self):
        self._disponivel = True

    #Cada subclasse informa qual é o seu tipo
    @abstractmethod
    def tipo(self):
        pass

    #Cada subclasse informa quantos dias tem de prazo (0 = devolver no mesmo dia)
    @abstractmethod
    def prazo_dias(self):
        pass

    #Metodo para calcular o prazo de devolução: soma os dias do prazo à data de retirada
    #e vai até 23:59:59 desse dia. Fica na superclasse para não repetir o código nas subclasses
    def calcular_prazo(self, retirada):
        return (retirada + timedelta(days=self.prazo_dias())).replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0
        )

    #Por padrão o equipamento não passa por vistoria na devolução
    def precisa_vistoria(self):
        return False

    def descricao_prazo(self):
        if self.prazo_dias() == 0:
            return "devolver no mesmo dia"
        return f"{self.prazo_dias()} dia(s)"

    def __str__(self):
        return f"#{self._id} - {self.tipo()} ({self._nome})"

#Subclasses
class Bola(Equipamento):
    def tipo(self):
        return "Bola"

    def prazo_dias(self):
        return 0

class Colete(Equipamento):
    def tipo(self):
        return "Colete"

    def prazo_dias(self):
        return 0

class Raquete(Equipamento):
    def tipo(self):
        return "Raquete de tênis de mesa"

    def prazo_dias(self):
        return 2

class Bicicleta(Equipamento):
    def tipo(self):
        return "Bicicleta"

    def prazo_dias(self):
        return 7

    #A bicicleta é o único equipamento que passa por vistoria
    def precisa_vistoria(self):
        return True
