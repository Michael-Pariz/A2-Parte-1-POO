from datetime import datetime, timedelta

from emprestimo import Emprestimo
from excecoes import ErroAtletica


class Atletica:
    FATOR_BLOQUEIO = 2  #dias de bloqueio para cada dia de atraso

    def __init__(self):
        self._usuarios = []
        self._equipamentos = []
        self._emprestimos = []
        self._proximo_id = 1
        self._dias_avancados = 0  #usado para simular a passagem dos dias nos testes

    @property
    def usuarios(self):
        return self._usuarios.copy()

    @property
    def equipamentos(self):
        return self._equipamentos.copy()

    @property
    def emprestimos(self):
        return self._emprestimos.copy()

    # data do sistema 

    def agora(self):
        return datetime.now() + timedelta(days=self._dias_avancados)

    def avancar_dias(self, dias):
        if dias < 1:
            raise ErroAtletica("Informe pelo menos 1 dia.")
        self._dias_avancados = self._dias_avancados + dias

    def definir_data(self, nova_data):
        diferenca = (nova_data - self.agora().date()).days
        if diferenca < 0:
            raise ErroAtletica("A nova data não pode ser anterior à data atual do sistema.")
        self._dias_avancados = self._dias_avancados + diferenca

    # usuários

    def cadastrar_usuario(self, usuario):
        for u in self._usuarios:
            if u.ra == usuario.ra:
                raise ErroAtletica("Já existe um usuário com esse RA.")

        self._usuarios.append(usuario)

    def buscar_usuario(self, ra):
        for usuario in self._usuarios:
            if usuario.ra == ra:
                return usuario
        raise ErroAtletica(f"Nenhum usuário cadastrado com o RA {ra}.")

    def remover_usuario(self, ra):
        usuario = self.buscar_usuario(ra)
        if len(usuario.emprestimos_ativos()) > 0:
            raise ErroAtletica(f"{usuario.nome} ainda está com item(ns) emprestado(s). "
                               f"Registre a devolução antes de remover.")
        self._usuarios.remove(usuario)

    # equipamentos 

    def gerar_id(self):
        id = self._proximo_id
        self._proximo_id = self._proximo_id + 1
        return id

    def cadastrar_equipamento(self, equipamento):
        for e in self._equipamentos:
            if e.id == equipamento.id:
                raise ErroAtletica("Já existe um equipamento com esse ID.")

        self._equipamentos.append(equipamento)

    def buscar_equipamento(self, id):
        for equipamento in self._equipamentos:
            if equipamento.id == id:
                return equipamento
        raise ErroAtletica(f"Nenhum equipamento cadastrado com o ID {id}.")

    def remover_equipamento(self, id):
        equipamento = self.buscar_equipamento(id)
        if not equipamento.disponivel:
            raise ErroAtletica(f"{equipamento} está emprestado. Registre a devolução antes de remover.")
        self._equipamentos.remove(equipamento)

    def listar_disponiveis(self):
        disponiveis = []
        for equipamento in self._equipamentos:
            if equipamento.disponivel:
                disponiveis.append(equipamento)
        return disponiveis

    # empréstimos 

    def emprestimos_ativos(self):
        ativos = []
        for emprestimo in self._emprestimos:
            if emprestimo.esta_ativo():
                ativos.append(emprestimo)
        return ativos

    def emprestimo_ativo_do(self, id):
        equipamento = self.buscar_equipamento(id)
        for emprestimo in self._emprestimos:
            if emprestimo.esta_ativo() and emprestimo.equipamento.id == id:
                return emprestimo
        raise ErroAtletica(f"{equipamento} não está emprestado.")

    def emprestar(self, ra, id):
        usuario = self.buscar_usuario(ra)
        equipamento = self.buscar_equipamento(id)
        if not equipamento.disponivel:
            atual = self.emprestimo_ativo_do(id)
            raise ErroAtletica(f"{equipamento} já está emprestado com {atual.usuario.nome}.")

        agora = self.agora()
        usuario.verificar_pode_emprestar(agora)

        emprestimo = Emprestimo(usuario, equipamento, agora)
        equipamento.marcar_emprestado()
        usuario.adicionar_emprestimo(emprestimo)
        self._emprestimos.append(emprestimo)
        return emprestimo

    def devolver(self, id, vistoria=None, danificado=False):
        emprestimo = self.emprestimo_ativo_do(id)
        agora = self.agora()
        dias_atraso = emprestimo.devolver(agora, vistoria, danificado)
        emprestimo.equipamento.marcar_disponivel()

        #bloqueio: o dobro dos dias de atraso, contado a partir da devolução
        
        if dias_atraso > 0:
            fim_bloqueio = agora + timedelta(days=dias_atraso * self.FATOR_BLOQUEIO)
            emprestimo.usuario.bloqueio(fim_bloqueio)
        return emprestimo

    def historico_equipamento(self, id):
        self.buscar_equipamento(id)  #só para avisar se o ID não existe
        historico = []
        for emprestimo in self._emprestimos:
            if emprestimo.equipamento.id == id:
                historico.append(emprestimo)
        return historico

    #conta quantas vezes o equipamento foi devolvido danificado
    
    def total_devolucoes_danificadas(self, id):
        total = 0
        for emprestimo in self.historico_equipamento(id):
            if not emprestimo.esta_ativo() and emprestimo.danificado:
                total = total + 1
        return total
