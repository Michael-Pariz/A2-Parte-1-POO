from atletica import Atletica
from datas import formatar_data
from entrada import escolher, ler_data, ler_inteiro, ler_sim_nao, ler_texto
from equipamentos import Bicicleta, Bola, Colete, Raquete
from excecoes import ErroAtletica
from usuarios import Aluno, Servidor


class Menu:
    def __init__(self, atletica):
        self.__atletica = atletica

    def executar(self):
        while True:
            self.__mostrar_menu()
            opcao = input("Escolha uma opção: ").strip()
            print()

            if opcao == "0":
                print("Sistema encerrado. Até logo!")
                break

            try:
                if opcao == "1":
                    self.__emprestar()
                elif opcao == "2":
                    self.__devolver()
                elif opcao == "3":
                    self.__listar_disponiveis()
                elif opcao == "4":
                    self.__listar_emprestados()
                elif opcao == "5":
                    self.__historico_pessoa()
                elif opcao == "6":
                    self.__historico_equipamento()
                elif opcao == "7":
                    self.__cadastrar_pessoa()
                elif opcao == "8":
                    self.__cadastrar_equipamento()
                elif opcao == "9":
                    self.__listar_pessoas()
                elif opcao == "10":
                    self.__remover_pessoa()
                elif opcao == "11":
                    self.__remover_equipamento()
                elif opcao == "12":
                    self.__alterar_data()
                else:
                    print("Opção inválida. Digite um dos números do menu.")
                    continue
            except ErroAtletica as erro:
                print(f"\nNão foi possível concluir: {erro}")

            input("\nPressione Enter para voltar ao menu...")

    def __mostrar_menu(self):
        print("\n========== CONTROLE DE EMPRÉSTIMOS - ATLÉTICA ==========")
        print(f"Data do sistema: {formatar_data(self.__atletica.data_atual)}")
        print("  1 - Emprestar equipamento")
        print("  2 - Devolver equipamento")
        print("  3 - Ver equipamentos disponíveis")
        print("  4 - Ver equipamentos emprestados")
        print("  5 - Histórico de uma pessoa")
        print("  6 - Histórico de um equipamento")
        print("  7 - Cadastrar pessoa")
        print("  8 - Cadastrar equipamento")
        print("  9 - Ver pessoas cadastradas")
        print(" 10 - Remover pessoa")
        print(" 11 - Remover equipamento")
        print(" 12 - Alterar data do sistema")
        print("  0 - Sair")

    def __imprimir_lista(self, titulo, linhas, mensagem_vazia):
        # mostra uma lista de textos; devolve False se a lista estiver vazia
        print(titulo)
        if len(linhas) == 0:
            print(f"  {mensagem_vazia}")
            return False
        for linha in linhas:
            print(f"  - {linha}")
        return True

    def __resumos(self, emprestimos):
        # transforma uma lista de empréstimos em uma lista de textos
        linhas = []
        for emprestimo in emprestimos:
            linhas.append(emprestimo.resumo(self.__atletica.data_atual))
        return linhas

    # ---------- empréstimo e devolução ----------

    def __emprestar(self):
        linhas = []
        for equipamento in self.__atletica.listar_disponiveis():
            linhas.append(str(equipamento))
        if not self.__imprimir_lista("Equipamentos disponíveis:", linhas,
                                     "Nenhum equipamento disponível no momento."):
            return

        codigo = ler_inteiro("\nCódigo do equipamento: ", minimo=1)
        matricula = ler_texto("Matrícula de quem vai pegar: ")
        emprestimo = self.__atletica.emprestar(matricula, codigo)
        print(f"\nEmpréstimo registrado: {emprestimo.equipamento} com {emprestimo.usuario.nome}.")
        print(f"Devolver até {formatar_data(emprestimo.data_limite)}.")

    def __devolver(self):
        linhas = self.__resumos(self.__atletica.emprestimos_ativos())
        if not self.__imprimir_lista("Equipamentos emprestados:", linhas,
                                     "Nenhum equipamento emprestado no momento."):
            return

        codigo = ler_inteiro("\nCódigo do equipamento devolvido: ", minimo=1)
        equipamento = self.__atletica.emprestimo_ativo_do(codigo).equipamento

        danificado = False
        resultados_vistoria = None
        if equipamento.precisa_vistoria():
            print("Vistoria da devolução:")
            resultados_vistoria = {}
            for item in equipamento.itens_vistoria():
                resultados_vistoria[item] = ler_sim_nao(f"  O(a) {item} está em bom estado? (s/n): ")
        else:
            danificado = ler_sim_nao("O equipamento voltou danificado? (s/n): ")

        emprestimo = self.__atletica.devolver(codigo, danificado, resultados_vistoria)
        print(f"\nDevolução registrada: {equipamento} ({emprestimo.estado_devolucao()}).")

        atraso = emprestimo.dias_atraso()
        if atraso > 0:
            usuario = emprestimo.usuario
            situacao = usuario.situacao(self.__atletica.data_atual)
            print(f"Devolvido com {atraso} dia(s) de atraso. {usuario.nome} ficou {situacao}.")
        else:
            print("Devolvido dentro do prazo.")

    # ---------- consultas ----------

    def __listar_disponiveis(self):
        linhas = []
        for equipamento in self.__atletica.listar_disponiveis():
            linhas.append(f"{equipamento} - prazo: {equipamento.descricao_prazo()}")
        self.__imprimir_lista("Equipamentos disponíveis:", linhas, "Nenhum equipamento disponível.")

    def __listar_emprestados(self):
        linhas = self.__resumos(self.__atletica.emprestimos_ativos())
        self.__imprimir_lista("Equipamentos emprestados:", linhas, "Nenhum equipamento emprestado.")


    def __historico_pessoa(self):
        usuario = self.__atletica.buscar_usuario(ler_texto("Matrícula: "))
        print(f"\n{usuario}")
        print(f"Situação: {usuario.situacao(self.__atletica.data_atual)}")
        print(f"Itens com a pessoa agora: {len(usuario.emprestimos_ativos())} de {usuario.limite_itens()}")
        print(f"Devoluções com atraso: {usuario.total_devolucoes_com_atraso()}")
        print(f"Devoluções com dano: {usuario.total_devolucoes_danificadas()}")
        linhas = self.__resumos(usuario.historico)
        self.__imprimir_lista("Histórico:", linhas, "Nenhum empréstimo registrado.")

    def __historico_equipamento(self):
        codigo = ler_inteiro("Código do equipamento: ", minimo=1)
        historico = self.__atletica.historico_equipamento(codigo)

        danificados = 0
        for emprestimo in historico:
            if emprestimo.devolvido_danificado:
                danificados = danificados + 1

        print(f"\n{self.__atletica.buscar_equipamento(codigo)}")
        print(f"Vezes emprestado: {len(historico)} | Devoluções com dano: {danificados}")
        linhas = self.__resumos(historico)
        self.__imprimir_lista("Histórico:", linhas, "Este equipamento ainda não foi emprestado.")

    def __listar_pessoas(self):
        linhas = []
        for usuario in self.__atletica.listar_usuarios():
            quantidade = len(usuario.emprestimos_ativos())
            situacao = usuario.situacao(self.__atletica.data_atual)
            linhas.append(f"{usuario} - {quantidade}/{usuario.limite_itens()} itens - {situacao}")
        self.__imprimir_lista("Pessoas cadastradas:", linhas, "Nenhuma pessoa cadastrada.")

    # ---------- cadastros ----------

    def __cadastrar_pessoa(self):
        tipo = escolher("Tipo de pessoa:", ["Aluno", "Servidor"])
        nome = ler_texto("Nome: ")
        matricula = ler_texto("Matrícula: ")

        if tipo == 0:
            usuario = Aluno(nome, matricula)
        else:
            usuario = Servidor(nome, matricula)

        self.__atletica.cadastrar_usuario(usuario)
        print(f"\nCadastrado: {usuario}. Pode ter até {usuario.limite_itens()} itens ao mesmo tempo.")

    def __cadastrar_equipamento(self):
        tipo = escolher("Tipo de equipamento:", ["Bola", "Raquete de tênis de mesa", "Colete", "Bicicleta"])
        modalidade = ""
        if tipo == 0:
            modalidade = Bola.MODALIDADES[escolher("Modalidade:", Bola.MODALIDADES)]
        descricao = input("Descrição (opcional, ex: cor, marca, número): ")

        codigo = self.__atletica.gerar_codigo()
        if tipo == 0:
            equipamento = Bola(codigo, modalidade, descricao)
        elif tipo == 1:
            equipamento = Raquete(codigo, descricao)
        elif tipo == 2:
            equipamento = Colete(codigo, descricao)
        else:
            equipamento = Bicicleta(codigo, descricao)

        self.__atletica.cadastrar_equipamento(equipamento)
        print(f"\nCadastrado: {equipamento}. Prazo de empréstimo: {equipamento.descricao_prazo()}.")

    def __remover_pessoa(self):
        usuario = self.__atletica.buscar_usuario(ler_texto("Matrícula: "))
        if ler_sim_nao(f"Remover {usuario}? (s/n): "):
            self.__atletica.remover_usuario(usuario.matricula)
            print("Pessoa removida.")
        else:
            print("Remoção cancelada.")

    def __remover_equipamento(self):
        codigo = ler_inteiro("Código do equipamento: ", minimo=1)
        equipamento = self.__atletica.buscar_equipamento(codigo)
        if ler_sim_nao(f"Remover {equipamento}? (s/n): "):
            self.__atletica.remover_equipamento(codigo)
            print("Equipamento removido.")
        else:
            print("Remoção cancelada.")

    def __alterar_data(self):
        print("Use esta opção para simular a passagem dos dias e testar atrasos.")
        escolha = escolher("O que deseja fazer?", ["Avançar alguns dias", "Informar uma data"])
        if escolha == 0:
            dias = ler_inteiro("Quantos dias? ", minimo=1)
            self.__atletica.avancar_dias(dias)
        else:
            nova_data = ler_data("Nova data (dd/mm/aaaa): ")
            self.__atletica.definir_data(nova_data)
        print(f"Data do sistema agora: {formatar_data(self.__atletica.data_atual)}")


def carregar_dados_exemplo(atletica):
    atletica.cadastrar_usuario(Aluno("Ana Souza", "2024001"))
    atletica.cadastrar_usuario(Aluno("Bruno Lima", "2024002"))
    atletica.cadastrar_usuario(Servidor("Carla Mendes", "S1001"))
    atletica.cadastrar_equipamento(Bola(atletica.gerar_codigo(), "futsal"))
    atletica.cadastrar_equipamento(Bola(atletica.gerar_codigo(), "vôlei"))
    atletica.cadastrar_equipamento(Bola(atletica.gerar_codigo(), "basquete"))
    atletica.cadastrar_equipamento(Raquete(atletica.gerar_codigo(), "vermelha"))
    atletica.cadastrar_equipamento(Colete(atletica.gerar_codigo(), "azul nº 7"))
    atletica.cadastrar_equipamento(Bicicleta(atletica.gerar_codigo(), "Caloi preta"))


def main():
    atletica = Atletica()
    try:
        if ler_sim_nao("Deseja carregar dados de exemplo para teste? (s/n): "):
            carregar_dados_exemplo(atletica)
        menu = Menu(atletica)
        menu.executar()
    except KeyboardInterrupt:
        print("\nSistema encerrado.")
    except EOFError:
        print("\nSistema encerrado.")


if __name__ == "__main__":
    main()
