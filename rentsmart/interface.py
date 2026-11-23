"""
Interface de terminal: mostra o menu, faz as perguntas, valida as respostas
e cria os objetos (Apartamento, Casa, Estudio, TaxaContratual, Orcamento).
Esta classe NÃO faz cálculos: ela só conversa com o usuário.
"""

from rentsmart.imoveis import Apartamento, Casa, Estudio
from rentsmart.taxa_contratual import TaxaContratual
from rentsmart.orcamento import Orcamento
from rentsmart.exportador_csv import ExportadorCSV
from rentsmart.formatacao import formatar_moeda


class InterfaceTerminal:

    def __init__(self):
        self.exportador = ExportadorCSV()

    # ------------------------------------------------------------------
    # Métodos de leitura com validação (repetem a pergunta até a resposta ser válida)
    # ------------------------------------------------------------------
    def ler_inteiro(self, mensagem, minimo, maximo=None):
        while True:
            resposta = input(mensagem).strip()
            try:
                numero = int(resposta)
            except ValueError:
                print("  [!] Digite apenas um número inteiro.")
                continue
            if numero < minimo or (maximo is not None and numero > maximo):
                if maximo is None:
                    print(f"  [!] O valor deve ser maior ou igual a {minimo}.")
                else:
                    print(f"  [!] Escolha um valor entre {minimo} e {maximo}.")
                continue
            return numero

    def ler_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem + " (S/N): ").strip().upper()
            if resposta in ("S", "SIM"):
                return True
            if resposta in ("N", "NAO", "NÃO"):
                return False
            print("  [!] Responda com S para sim ou N para não.")

    # ------------------------------------------------------------------
    # Fluxo principal
    # ------------------------------------------------------------------
    def executar(self):
        print("\nBem-vindo(a) ao RentSmart — R.M Imóveis")
        while True:
            print("\n========== MENU PRINCIPAL ==========")
            print("1 - Fazer novo orçamento")
            print("2 - Consultar tabela de preços")
            print("0 - Sair")
            opcao = self.ler_inteiro("Escolha uma opção: ", 0, 2)
            if opcao == 1:
                self.fazer_orcamento()
            elif opcao == 2:
                self.exibir_tabela_precos()
            else:
                print("Obrigado por usar o RentSmart. Até logo!")
                break

    def escolher_imovel(self):
        """Pergunta o tipo e as características e devolve o objeto do imóvel."""
        print("\nTipo de imóvel:")
        print("1 - Apartamento")
        print("2 - Casa")
        print("3 - Estúdio")
        tipo = self.ler_inteiro("Escolha o tipo de imóvel: ", 1, 3)

        if tipo == 1 or tipo == 2:
            quartos = self.ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
            garagem = self.ler_sim_nao("Deseja 1 vaga de garagem por R$ 300,00/mês?")
            if tipo == 1:
                criancas = self.ler_sim_nao("O cliente possui crianças?")
                return Apartamento(quartos, garagem, criancas)
            return Casa(quartos, garagem)

        # tipo == 3 -> Estúdio
        pacote = self.ler_sim_nao("Deseja o pacote de 2 vagas por R$ 250,00/mês?")
        adicionais = 0
        if pacote:
            adicionais = self.ler_inteiro(
                "Quantas vagas adicionais (R$ 60,00 cada)? Digite 0 para nenhuma: ", 0)
        return Estudio(pacote, adicionais)

    def fazer_orcamento(self):
        imovel = self.escolher_imovel()
        parcelas = self.ler_inteiro(
            "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
            1, TaxaContratual.MAX_PARCELAS)
        taxa = TaxaContratual(parcelas)

        orcamento = Orcamento(imovel, taxa)
        print("\n" + orcamento.formatar_resumo())

        try:
            caminho = self.exportador.exportar(orcamento)
            print(f"\nArquivo CSV gerado com sucesso: {caminho}")
        except OSError as erro:
            print(f"\n[ERRO] Não foi possível gerar o arquivo CSV: {erro}")

    def exibir_tabela_precos(self):
        """Mostra as regras usando as constantes das próprias classes."""
        print("\n========== TABELA DE PREÇOS ==========")
        print(f"Apartamento (1 quarto) .... {formatar_moeda(Apartamento.ALUGUEL_BASE)}")
        print(f"  + 2º quarto ............. {formatar_moeda(Apartamento.ADICIONAL_SEGUNDO_QUARTO)}")
        print(f"  + vaga de garagem ....... {formatar_moeda(Apartamento.VALOR_GARAGEM)}")
        print("  - 5% de desconto se o cliente não possui crianças")
        print(f"Casa (1 quarto) ........... {formatar_moeda(Casa.ALUGUEL_BASE)}")
        print(f"  + 2º quarto ............. {formatar_moeda(Casa.ADICIONAL_SEGUNDO_QUARTO)}")
        print(f"  + vaga de garagem ....... {formatar_moeda(Casa.VALOR_GARAGEM)}")
        print(f"Estúdio ................... {formatar_moeda(Estudio.ALUGUEL_BASE)}")
        print(f"  + pacote de 2 vagas ..... {formatar_moeda(Estudio.VALOR_PACOTE_VAGAS)}")
        print(f"  + cada vaga adicional ... {formatar_moeda(Estudio.VALOR_VAGA_ADICIONAL)}")
        print(f"Taxa contratual ........... {formatar_moeda(TaxaContratual.VALOR_TOTAL)}"
              f" (em até {TaxaContratual.MAX_PARCELAS}x, cobrada à parte)")
