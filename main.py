from datas import formatar_data
from equipamentos import Bicicleta, Bola, Colete, Raquete

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
            
    def __listar_disponiveis(self):
        linhas = []
        for equipamento in self.__atletica.listar_disponiveis():
            linhas.append(f"{equipamento} - prazo: {equipamento.descricao_prazo()}")
        self.__imprimir_lista("Equipamentos disponíveis:", linhas, "Nenhum equipamento disponível.")

    def __listar_emprestados(self):
        linhas = self.__resumos(self.__atletica.emprestimos_ativos())
        self.__imprimir_lista("Equipamentos emprestados:", linhas, "Nenhum equipamento emprestado.")

def main():
    
if __name__ == "__main__":
    main()
