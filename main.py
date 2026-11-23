"""
RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)
Ponto de entrada do programa. Execute com:  python main.py
"""

from rentsmart.interface import InterfaceTerminal


def main():
    interface = InterfaceTerminal()  # cria o objeto da interface
    try:
        interface.executar()
    except (KeyboardInterrupt, EOFError):
        # usuário apertou Ctrl+C ou fechou a entrada: encerra sem mostrar erro técnico
        print("\n\nPrograma encerrado pelo usuário.")


if __name__ == "__main__":
    main()
