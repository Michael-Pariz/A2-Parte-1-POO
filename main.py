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
                print("Sistema encerrado.")
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
                print(f"\n Não foi possível concluir: {erro}")

            input("\n Pressione Enter para voltar ao menu...")

      def __mostrar_menu(self):
        print("\n CONTROLE DE EMPRÉSTIMOS - ATLÉTICA ")
        print(f"Data do sistema: {formatar_data(self.__atletica.data_atual)}")
        print("1 - Emprestar equipamento")
        print("2 - Devolver equipamento")
        print("3 - Ver equipamentos disponíveis")
        print("4 - Ver equipamentos emprestados")
        print("5 - Histórico de uma pessoa")
        print("6 - Histórico de um equipamento")
        print("7 - Cadastrar pessoa")
        print("8 - Cadastrar equipamento")
        print("9 - Ver pessoas cadastradas")
        print("10 - Remover pessoa")
        print("11 - Remover equipamento")
        print("12 - Alterar data do sistema")
        print("0 - Sair")
