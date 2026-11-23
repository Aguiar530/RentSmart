"""Funções auxiliares para exibir valores no padrão brasileiro."""


def formatar_numero(valor):
    """Converte 1234.5 em '1.234,50' (padrão brasileiro)."""
    texto = f"{valor:,.2f}"  # gera '1,234.50' (padrão americano)
    # troca vírgula por ponto e ponto por vírgula, usando 'X' como coringa
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_moeda(valor):
    """Converte 1234.5 em 'R$ 1.234,50'."""
    if valor < 0:
        return f"- R$ {formatar_numero(-valor)}"
    return f"R$ {formatar_numero(valor)}"
