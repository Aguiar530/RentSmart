"""Classe que representa a taxa contratual e o seu parcelamento."""

from rentsmart.formatacao import formatar_moeda


class TaxaContratual:
    VALOR_TOTAL = 2000.00
    MAX_PARCELAS = 5

    def __init__(self, quantidade_parcelas):
        if not 1 <= quantidade_parcelas <= self.MAX_PARCELAS:
            raise ValueError(f"A taxa pode ser paga em 1 a {self.MAX_PARCELAS} parcelas.")
        self.quantidade_parcelas = quantidade_parcelas

    def calcular_parcelas(self):
        """
        Retorna a lista com o valor de cada parcela.
        Quando a divisão não é exata (ex.: 2000 / 3), a última parcela
        recebe o ajuste de centavos para que a soma dê exatamente R$ 2.000,00.
        """
        n = self.quantidade_parcelas
        valor = round(self.VALOR_TOTAL / n, 2)
        ultima = round(self.VALOR_TOTAL - valor * (n - 1), 2)
        return [valor] * (n - 1) + [ultima]

    def valor_parcela_no_mes(self, mes):
        """Valor da taxa cobrado no mês informado (0 se já foi quitada)."""
        if mes <= self.quantidade_parcelas:
            return self.calcular_parcelas()[mes - 1]
        return 0.0

    def descrever(self):
        if self.quantidade_parcelas == 1:
            return f"à vista, 1x de {formatar_moeda(self.VALOR_TOTAL)}"
        parcelas = self.calcular_parcelas()
        if parcelas[0] == parcelas[-1]:
            return f"{self.quantidade_parcelas}x de {formatar_moeda(parcelas[0])}"
        return (f"{self.quantidade_parcelas}x ({self.quantidade_parcelas - 1}x de "
                f"{formatar_moeda(parcelas[0])} + 1x de {formatar_moeda(parcelas[-1])})")
