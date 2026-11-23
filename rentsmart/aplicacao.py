"""
RentSmart - Sistema de Orçamento de Locação
R.M Imóveis | Projeto acadêmico de Python e Programação Orientada a Objetos

Execução:
    python rentsmart.py

O sistema gera um CSV com a projeção dos 12 meses no diretório atual.
"""

import csv
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


TAXA_CONTRATUAL = Decimal("2000.00")
MESES_PROJECAO = 12
ARQUIVO_CSV = str(Path("saidas") / "projecao_rentsmart_12_meses.csv")


def dinheiro(valor: Decimal) -> str:
    """Formata valores no padrão monetário brasileiro."""
    valor = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def decimal_centavos(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class Imovel:
    """Representa o imóvel escolhido e calcula seu aluguel com adicionais."""
    tipo: str
    quartos: int
    garagem: bool = False
    pacote_estudio: bool = False
    vagas_extras_estudio: int = 0

    def aluguel_base(self) -> Decimal:
        tabela = {
            ("apartamento", 1): Decimal("700.00"),
            ("apartamento", 2): Decimal("700.00"),
            ("casa", 1): Decimal("900.00"),
            ("casa", 2): Decimal("900.00"),
            ("estudio", 0): Decimal("1200.00"),
        }
        return tabela[(self.tipo, self.quartos)]

    def adicional_quartos(self) -> Decimal:
        if self.tipo == "apartamento" and self.quartos == 2:
            return Decimal("200.00")
        if self.tipo == "casa" and self.quartos == 2:
            return Decimal("250.00")
        return Decimal("0.00")

    def adicional_garagem(self) -> Decimal:
        if self.tipo in ("apartamento", "casa") and self.garagem:
            return Decimal("300.00")
        if self.tipo == "estudio" and self.pacote_estudio:
            return Decimal("250.00") + Decimal("60.00") * self.vagas_extras_estudio
        return Decimal("0.00")

    def descricao_estacionamento(self) -> str:
        if self.tipo in ("apartamento", "casa"):
            return "1 vaga de garagem" if self.garagem else "Sem vaga de garagem"
        if self.pacote_estudio:
            total_vagas = 2 + self.vagas_extras_estudio
            return f"Pacote de {total_vagas} vaga(s) para estúdio"
        return "Sem pacote de estacionamento"

    def validar(self) -> None:
        if self.tipo not in ("apartamento", "casa", "estudio"):
            raise ValueError("Tipo de imóvel inválido.")
        if self.tipo in ("apartamento", "casa") and self.quartos not in (1, 2):
            raise ValueError("Apartamentos e casas aceitam 1 ou 2 quartos.")
        if self.tipo == "estudio" and self.quartos != 0:
            raise ValueError("Estúdio não utiliza quantidade de quartos.")
        if self.vagas_extras_estudio < 0:
            raise ValueError("A quantidade de vagas extras não pode ser negativa.")
        if self.tipo != "estudio" and (self.pacote_estudio or self.vagas_extras_estudio):
            raise ValueError("Pacote de estacionamento é exclusivo para estúdios.")
        if self.tipo == "estudio" and self.vagas_extras_estudio > 0 and not self.pacote_estudio:
            raise ValueError("Para adicionar vagas extras, selecione primeiro o pacote de 2 vagas.")


@dataclass
class Orcamento:
    """Agrupa os dados do cliente, imóvel, desconto e condição contratual."""
    cliente: str
    imovel: Imovel
    possui_criancas: bool
    parcelas_taxa: int

    def __post_init__(self):
        self.imovel.validar()
        if not self.cliente.strip():
            raise ValueError("O nome do cliente não pode ficar vazio.")
        if not 1 <= self.parcelas_taxa <= 5:
            raise ValueError("A taxa contratual pode ser parcelada de 1 a 5 vezes.")

    def valor_base(self) -> Decimal:
        return self.imovel.aluguel_base()

    def total_adicionais(self) -> Decimal:
        return self.imovel.adicional_quartos() + self.imovel.adicional_garagem()

    def valor_antes_desconto(self) -> Decimal:
        return self.valor_base() + self.total_adicionais()

    def desconto(self) -> Decimal:
        if self.imovel.tipo == "apartamento" and not self.possui_criancas:
            return decimal_centavos(self.valor_antes_desconto() * Decimal("0.05"))
        return Decimal("0.00")

    def aluguel_mensal(self) -> Decimal:
        return decimal_centavos(self.valor_antes_desconto() - self.desconto())

    def parcela_taxa(self) -> Decimal:
        return decimal_centavos(TAXA_CONTRATUAL / Decimal(self.parcelas_taxa))

    def resumo(self) -> dict:
        return {
            "cliente": self.cliente.strip(),
            "tipo": self.imovel.tipo.capitalize(),
            "quartos": "Não se aplica" if self.imovel.tipo == "estudio" else str(self.imovel.quartos),
            "estacionamento": self.imovel.descricao_estacionamento(),
            "aluguel_base": self.valor_base(),
            "adicional_quartos": self.imovel.adicional_quartos(),
            "adicional_estacionamento": self.imovel.adicional_garagem(),
            "desconto": self.desconto(),
            "aluguel_mensal": self.aluguel_mensal(),
            "taxa_contratual": TAXA_CONTRATUAL,
            "parcelas": self.parcelas_taxa,
            "valor_parcela_taxa": self.parcela_taxa(),
        }

    def gerar_projecao_csv(self, caminho: str = ARQUIVO_CSV) -> Path:
        """Gera 12 meses; a taxa é somada ao aluguel apenas nos meses parcelados."""
        destino = Path(caminho)
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow([
                "Mes", "Aluguel mensal (R$)", "Parcela taxa contratual (R$)",
                "Total previsto no mes (R$)"
            ])
            for mes in range(1, MESES_PROJECAO + 1):
                parcela = self.parcela_taxa() if mes <= self.parcelas_taxa else Decimal("0.00")
                total = self.aluguel_mensal() + parcela
                escritor.writerow([
                    mes,
                    f"{self.aluguel_mensal():.2f}",
                    f"{parcela:.2f}",
                    f"{total:.2f}",
                ])
        return destino


def ler_opcao(mensagem: str, opcoes: tuple[str, ...]) -> str:
    while True:
        valor = input(mensagem).strip().lower()
        if valor in opcoes:
            return valor
        print("Opção inválida. Escolha uma das opções apresentadas.")


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_sim_nao(mensagem: str) -> bool:
    return ler_opcao(mensagem + " (s/n): ", ("s", "n")) == "s"


def coletar_orcamento() -> Orcamento:
    print("\n=== RENTSMART | R.M IMÓVEIS ===")
    cliente = input("Nome do cliente: ").strip()
    while not cliente:
        print("O nome é obrigatório.")
        cliente = input("Nome do cliente: ").strip()

    tipo = ler_opcao(
        "Tipo de imóvel (apartamento/casa/estudio): ",
        ("apartamento", "casa", "estudio")
    )

    if tipo == "estudio":
        quartos = 0
        pacote = ler_sim_nao("Deseja contratar o pacote inicial de 2 vagas por R$ 250,00?")
        extras = 0
        if pacote:
            extras = ler_inteiro("Quantidade de vagas adicionais (0 a 10): ", 0, 10)
        garagem = False
    else:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja 1 vaga de garagem por R$ 300,00?")
        pacote = False
        extras = 0

    possui_criancas = True
    if tipo == "apartamento":
        possui_criancas = ler_sim_nao("O cliente possui crianças?")

    parcelas = ler_inteiro("Em quantas parcelas deseja pagar a taxa contratual (1 a 5)? ", 1, 5)

    imovel = Imovel(
        tipo=tipo,
        quartos=quartos,
        garagem=garagem,
        pacote_estudio=pacote,
        vagas_extras_estudio=extras
    )
    return Orcamento(cliente, imovel, possui_criancas, parcelas)


def exibir_resumo(orcamento: Orcamento) -> None:
    r = orcamento.resumo()
    print("\n" + "=" * 52)
    print("                 ORÇAMENTO RENTSMART")
    print("=" * 52)
    print(f"Cliente:                         {r['cliente']}")
    print(f"Imóvel:                          {r['tipo']}")
    print(f"Quartos:                         {r['quartos']}")
    print(f"Estacionamento:                  {r['estacionamento']}")
    print("-" * 52)
    print(f"Aluguel-base:                    {dinheiro(r['aluguel_base'])}")
    print(f"Adicional por quartos:           {dinheiro(r['adicional_quartos'])}")
    print(f"Adicional estacionamento:       {dinheiro(r['adicional_estacionamento'])}")
    print(f"Desconto aplicado:              -{dinheiro(r['desconto'])}")
    print("-" * 52)
    print(f"ALUGUEL MENSAL:                  {dinheiro(r['aluguel_mensal'])}")
    print("-" * 52)
    print(f"Taxa contratual (separada):      {dinheiro(r['taxa_contratual'])}")
    print(f"Parcelamento:                    {r['parcelas']}x de {dinheiro(r['valor_parcela_taxa'])}")
    print("A taxa contratual não está incluída no aluguel mensal.")
    print("=" * 52)


def main() -> None:
    try:
        orcamento = coletar_orcamento()
        exibir_resumo(orcamento)
        arquivo = orcamento.gerar_projecao_csv()
        print(f"\nCSV gerado com sucesso: {arquivo.resolve()}")
        print("A projeção apresenta os 12 meses e separa aluguel e taxa contratual.")
    except (ValueError, KeyError) as erro:
        print(f"\nNão foi possível concluir o orçamento: {erro}")


if __name__ == "__main__":
    main()
