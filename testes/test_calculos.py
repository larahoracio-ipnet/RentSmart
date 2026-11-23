import unittest
from decimal import Decimal
from rentsmart import Imovel, Orcamento

class TestRentSmart(unittest.TestCase):
    def test_apartamento_com_desconto_e_garagem(self):
        o = Orcamento("Teste", Imovel("apartamento", 2, garagem=True), False, 5)
        self.assertEqual(o.aluguel_mensal(), Decimal("1140.00"))

    def test_casa_dois_quartos_sem_garagem(self):
        o = Orcamento("Teste", Imovel("casa", 2), True, 2)
        self.assertEqual(o.aluguel_mensal(), Decimal("1150.00"))

    def test_estudio_com_pacote_e_vaga_extra(self):
        i = Imovel("estudio", 0, pacote_estudio=True, vagas_extras_estudio=1)
        o = Orcamento("Teste", i, True, 1)
        self.assertEqual(o.aluguel_mensal(), Decimal("1510.00"))

    def test_taxa_em_cinco_parcelas(self):
        o = Orcamento("Teste", Imovel("apartamento", 1), True, 5)
        self.assertEqual(o.parcela_taxa(), Decimal("400.00"))

    def test_rejeita_parcelamento_invalido(self):
        with self.assertRaises(ValueError):
            Orcamento("Teste", Imovel("casa", 1), True, 6)

if __name__ == "__main__":
    unittest.main()
