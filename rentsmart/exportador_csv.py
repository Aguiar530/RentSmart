"""Classe responsável por gravar a projeção de 12 meses em um arquivo CSV."""

import csv
import os
from datetime import datetime

from rentsmart.formatacao import formatar_numero


class ExportadorCSV:
    CABECALHO = ["Mês", "Aluguel (R$)", "Parcela da taxa",
                 "Taxa contratual (R$)", "Total do mês (R$)"]

    def __init__(self, pasta_saida="saidas"):
        self.pasta_saida = pasta_saida

    def gerar_nome_arquivo(self, orcamento):
        """Ex.: projecao_apartamento_20261123_153000.csv (data/hora evita sobrescrever)."""
        momento = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"projecao_{orcamento.imovel.CODIGO}_{momento}.csv"

    def exportar(self, orcamento, nome_arquivo=None):
        """Cria o CSV e devolve o caminho do arquivo gerado."""
        os.makedirs(self.pasta_saida, exist_ok=True)  
        if nome_arquivo is None:
            nome_arquivo = self.gerar_nome_arquivo(orcamento)
        caminho = os.path.join(self.pasta_saida, nome_arquivo)
        projecao = orcamento.gerar_projecao()


        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(self.CABECALHO)
            for item in projecao:
                escritor.writerow([item["mes"],
                                   formatar_numero(item["aluguel"]),
                                   item["parcela"],
                                   formatar_numero(item["taxa"]),
                                   formatar_numero(item["total"])])
            
            escritor.writerow(["TOTAL",
                               formatar_numero(sum(i["aluguel"] for i in projecao)),
                               "",
                               formatar_numero(sum(i["taxa"] for i in projecao)),
                               formatar_numero(orcamento.calcular_total_primeiro_ano())])
        return caminho
