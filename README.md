# RentSmart — Sistema de Orçamento de Locação

**Autora:** Lara Machado Horacio  
**RA:** 249562  
**Disciplina:** Algorithmic Thinking & Introduction to Object-Oriented Programming  
**Empresa fictícia:** R.M Imóveis

Projeto acadêmico desenvolvido em Python para automatizar o cálculo de orçamentos de locação.

## Como executar

Requisito: Python 3.9 ou superior. Não é necessário instalar bibliotecas externas.

```bash
python main.py
```

Para executar os testes:

```bash
python -m unittest discover testes -v
```

## Estrutura

```text
RentSmart/
├── main.py
├── rentsmart/
│   ├── __init__.py
│   └── aplicacao.py
├── testes/
│   └── test_calculos.py
├── docs/
│   ├── Relatorio_Teorico_RentSmart.pdf
│   └── Roteiro_Video_Pitch.txt
├── exemplos/
│   └── projecao_rentsmart_12_meses.csv
└── saidas/
    └── (CSV gerado pelo programa)
```

## Funcionalidades

- Cadastro do nome do cliente e escolha do imóvel.
- Apartamento, casa e estúdio.
- Cálculo de aluguel-base, adicionais de quartos e estacionamento.
- Desconto de 5% para apartamento quando o cliente não possui crianças.
- Taxa contratual de R$ 2.000,00 apresentada separadamente e parcelável de 1 a 5 vezes.
- Validação de entradas.
- Exibição de orçamento detalhado.
- Geração de CSV com projeção de 12 meses.

## Regras de negócio

| Item | Valor/regra |
|---|---|
| Apartamento | R$ 700,00 de base |
| Casa | R$ 900,00 de base |
| Estúdio | R$ 1.200,00 de base |
| Segundo quarto — apartamento | + R$ 200,00 |
| Segundo quarto — casa | + R$ 250,00 |
| Garagem — apartamento/casa | + R$ 300,00 |
| Pacote inicial de 2 vagas — estúdio | + R$ 250,00 |
| Vaga extra — estúdio | + R$ 60,00 cada |
| Desconto | 5% sobre apartamento com adicionais, se não houver crianças |
| Taxa contratual | R$ 2.000,00, em até 5 parcelas |

## Organização orientada a objetos

A classe `Imovel` representa o imóvel e concentra as regras de cálculo e validação relacionadas à categoria, quartos e estacionamento. A classe `Orcamento` reúne os dados do cliente e do imóvel, calcula desconto, aluguel, taxa e gera a projeção CSV.

## Exemplo de cálculo

Apartamento com dois quartos, garagem e cliente sem crianças:

- Aluguel-base: R$ 700,00
- Segundo quarto: R$ 200,00
- Garagem: R$ 300,00
- Subtotal: R$ 1.200,00
- Desconto de 5%: R$ 60,00
- **Aluguel mensal: R$ 1.140,00**
- Taxa contratual: R$ 2.000,00, em cinco parcelas de R$ 400,00.
