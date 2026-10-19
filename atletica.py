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
        if any(
        u.ra == usuario.ra
        for u in self.__usuarios
        ):
            raise ValueError("Já existe um usuário com esse ra.")

        self.__usuarios.append(usuario)

    def cadastrar_equipamento(self, equipamento):
        if any(
        e.id == equipamento.id
        for e in self.__equipamentos
        ):
            raise ValueError("Já existe um equipamento com esse ID.")

        self.__equipamentos.append(equipamento)
