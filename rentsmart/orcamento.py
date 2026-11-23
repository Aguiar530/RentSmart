"""Classe que junta o imóvel e a taxa contratual para formar o orçamento."""

from rentsmart.formatacao import formatar_moeda

LARGURA = 64  # largura do texto exibido no terminal


class Orcamento:
    MESES_PROJECAO = 12

    def __init__(self, imovel, taxa_contratual):
        # Composição: o orçamento "tem um" imóvel e "tem uma" taxa contratual
        self.imovel = imovel
        self.taxa_contratual = taxa_contratual

    def calcular_aluguel_mensal(self):
        return self.imovel.calcular_aluguel_mensal()

    def gerar_projecao(self):
        """Lista com um dicionário por mês: aluguel, parcela da taxa e total."""
        projecao = []
        aluguel = self.calcular_aluguel_mensal()
        n_parcelas = self.taxa_contratual.quantidade_parcelas
        for mes in range(1, self.MESES_PROJECAO + 1):
            taxa = self.taxa_contratual.valor_parcela_no_mes(mes)
            projecao.append({
                "mes": mes,
                "aluguel": aluguel,
                "parcela": f"{mes}/{n_parcelas}" if taxa > 0 else "-",
                "taxa": taxa,
                "total": round(aluguel + taxa, 2),
            })
        return projecao

    def calcular_total_primeiro_ano(self):
        return round(sum(linha["total"] for linha in self.gerar_projecao()), 2)

    @staticmethod
    def _linha(descricao, valor):
        """Monta uma linha 'descrição ....... R$ valor' alinhada."""
        texto_valor = formatar_moeda(valor)
        pontos = "." * (LARGURA - len(descricao) - len(texto_valor) - 4)
        return f"  {descricao} {pontos} {texto_valor}"

    def formatar_resumo(self):
        """Gera o texto completo do orçamento detalhado."""
        linhas = ["=" * LARGURA,
                  "ORÇAMENTO DE LOCAÇÃO — RentSmart | R.M Imóveis".center(LARGURA),
                  "=" * LARGURA,
                  f"Imóvel: {self.imovel.descrever()}", ""]

        linhas.append("1) ALUGUEL MENSAL")
        for descricao, valor in self.imovel.detalhar_itens():
            linhas.append(self._linha(descricao, valor))
        linhas.append("  " + "-" * (LARGURA - 2))
        linhas.append(self._linha("VALOR MENSAL DO ALUGUEL", self.calcular_aluguel_mensal()))
        linhas.append("")

        linhas.append("2) TAXA CONTRATUAL (cobrada à parte do aluguel)")
        linhas.append(self._linha("Valor total da taxa", self.taxa_contratual.VALOR_TOTAL))
        linhas.append(f"  Condição escolhida: {self.taxa_contratual.descrever()}")
        linhas.append("")

        linhas.append("3) PROJEÇÃO DOS 12 PRIMEIROS MESES")
        linhas.append(f"  {'Mês':>3} | {'Aluguel':>12} | {'Taxa contratual':>15} | {'Total do mês':>12}")
        for item in self.gerar_projecao():
            linhas.append(f"  {item['mes']:>3} | {formatar_moeda(item['aluguel']):>12} | "
                          f"{formatar_moeda(item['taxa']):>15} | {formatar_moeda(item['total']):>12}")
        linhas.append("  " + "-" * (LARGURA - 2))
        linhas.append(self._linha("TOTAL PREVISTO NO 1º ANO", self.calcular_total_primeiro_ano()))
        linhas.append("=" * LARGURA)
        return "\n".join(linhas)
