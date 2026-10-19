from datetime import timedelta
from emprestimo import Emprestimo


class Atletica:
    def __init__(self):
        self.__usuarios = []
        self.__equipamentos = []
        self.__emprestimos = []

    @property
    def usuarios(self):
        return self.__usuarios.copy()

    @property
    def equipamentos(self):
        return self.__equipamentos.copy()

    @property
    def emprestimos(self):
        return self.__emprestimos.copy()

    def cadastrar_usuario(self, usuario):
        if usuario in self.__usuarios:
            raise ValueError("Usuário já cadastrado.")

        self.__usuarios.append(usuario)
