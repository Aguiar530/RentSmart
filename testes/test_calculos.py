"""
Testes automáticos dos cálculos (biblioteca unittest, já vem com o Python).
Execute a partir da pasta do projeto:  python -m unittest discover testes
"""

import csv
import os
import tempfile
import unittest

from rentsmart.imoveis import Apartamento, Casa, Estudio
from rentsmart.taxa_contratual import TaxaContratual
from rentsmart.orcamento import Orcamento
from rentsmart.exportador_csv import ExportadorCSV


class TestApartamento(unittest.TestCase):
    def test_1_quarto_sem_garagem_com_criancas(self):
        self.assertEqual(Apartamento(1, False, True).calcular_aluguel_mensal(), 700.00)

    def test_1_quarto_sem_garagem_sem_criancas(self):
        self.assertEqual(Apartamento(1, False, False).calcular_aluguel_mensal(), 665.00)

    def test_2_quartos_com_garagem_com_criancas(self):
        self.assertEqual(Apartamento(2, True, True).calcular_aluguel_mensal(), 1200.00)

    def test_2_quartos_com_garagem_sem_criancas(self):
        # (700 + 200 + 300) = 1200 -> 5% = 60 -> 1140
        self.assertEqual(Apartamento(2, True, False).calcular_aluguel_mensal(), 1140.00)

    def test_quartos_invalidos(self):
        with self.assertRaises(ValueError):
            Apartamento(3, False, True)


class TestCasa(unittest.TestCase):
    def test_1_quarto_sem_garagem(self):
        self.assertEqual(Casa(1, False).calcular_aluguel_mensal(), 900.00)

    def test_2_quartos_com_garagem(self):
        self.assertEqual(Casa(2, True).calcular_aluguel_mensal(), 1450.00)

    def test_casa_nunca_tem_desconto(self):
        self.assertEqual(Casa(2, True).calcular_desconto(), 0.0)


class TestEstudio(unittest.TestCase):
    def test_sem_vagas(self):
        self.assertEqual(Estudio(False).calcular_aluguel_mensal(), 1200.00)

    def test_pacote_de_2_vagas(self):
        self.assertEqual(Estudio(True, 0).calcular_aluguel_mensal(), 1450.00)

    def test_pacote_mais_3_vagas(self):
        # 1200 + 250 + 3 x 60 = 1630, total de 5 vagas
        estudio = Estudio(True, 3)
        self.assertEqual(estudio.calcular_aluguel_mensal(), 1630.00)
        self.assertEqual(estudio.total_de_vagas(), 5)

    def test_vagas_negativas(self):
        with self.assertRaises(ValueError):
            Estudio(True, -1)

    def test_vagas_adicionais_sem_pacote(self):
        with self.assertRaises(ValueError):
            Estudio(False, 2)


class TestTaxaContratual(unittest.TestCase):
    def test_a_vista(self):
        self.assertEqual(TaxaContratual(1).calcular_parcelas(), [2000.00])

    def test_5_parcelas(self):
        self.assertEqual(TaxaContratual(5).calcular_parcelas(), [400.00] * 5)

    def test_3_parcelas_somam_2000(self):
        parcelas = TaxaContratual(3).calcular_parcelas()
        self.assertEqual(parcelas, [666.67, 666.67, 666.66])
        self.assertAlmostEqual(sum(parcelas), 2000.00, places=2)

    def test_parcelas_invalidas(self):
        for valor in (0, 6):
            with self.assertRaises(ValueError):
                TaxaContratual(valor)


class TestOrcamentoECSV(unittest.TestCase):
    def setUp(self):
        self.orcamento = Orcamento(Apartamento(2, True, False), TaxaContratual(3))

    def test_projecao_tem_12_meses(self):
        projecao = self.orcamento.gerar_projecao()
        self.assertEqual(len(projecao), 12)
        self.assertEqual(projecao[0]["total"], 1140.00 + 666.67)
        self.assertEqual(projecao[3]["taxa"], 0.0)  # mês 4: taxa já quitada

    def test_total_primeiro_ano(self):
        self.assertEqual(self.orcamento.calcular_total_primeiro_ano(), 1140.00 * 12 + 2000.00)

    def test_csv_gerado(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = ExportadorCSV(pasta).exportar(self.orcamento, "teste.csv")
            with open(caminho, encoding="utf-8-sig") as arquivo:
                linhas = list(csv.reader(arquivo, delimiter=";"))
            self.assertTrue(os.path.exists(caminho))
            self.assertEqual(len(linhas), 14)  # cabeçalho + 12 meses + total
            self.assertEqual(linhas[1], ["1", "1.140,00", "1/3", "666,67", "1.806,67"])
            self.assertEqual(linhas[13][4], "15.680,00")


if __name__ == "__main__":
    unittest.main()
