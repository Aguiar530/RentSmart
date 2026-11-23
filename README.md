# RentSmart — Sistema de Orçamento de Locação

Aplicação em Python, com Programação Orientada a Objetos, que calcula automaticamente orçamentos de locação para a imobiliária **R.M Imóveis**. Trabalho da disciplina *Algorithmic Thinking & Introduction to Object-Oriented Programming*.

## Objetivo

Substituir o cálculo manual de orçamentos, que é lento e sujeito a erros. O sistema recebe as características da locação, aplica as regras comerciais da imobiliária, mostra um orçamento detalhado e gera um arquivo CSV com a projeção dos 12 primeiros meses do contrato.

## Tecnologias

- Python 3.8 ou superior
- Somente bibliotecas padrão do Python: `csv`, `os`, `datetime` e `unittest` (testes). **Não é preciso instalar nada com pip.**

## Estrutura do projeto

```
RentSmart/
├── main.py                    # ponto de entrada: python main.py
├── rentsmart/                 # código da aplicação
│   ├── imoveis.py             # classes Imovel, ImovelResidencial, Apartamento, Casa, Estudio
│   ├── taxa_contratual.py     # classe TaxaContratual (parcelamento da taxa)
│   ├── orcamento.py           # classe Orcamento (junta imóvel + taxa, projeção de 12 meses)
│   ├── exportador_csv.py      # classe ExportadorCSV (gera o arquivo .csv)
│   ├── interface.py           # classe InterfaceTerminal (menu, perguntas e validações)
│   └── formatacao.py          # funções para exibir valores em R$ (padrão brasileiro)
├── testes/
│   └── test_calculos.py       # testes automáticos dos cálculos
├── docs/
│   ├── RentSmart_Parte_Teorica.pdf   # documento teórico
│   ├── fluxograma.png                # fluxograma do sistema
│   ├── diagrama_classes.png          # diagrama de classes
│   └── roteiro_video_pitch.md        # roteiro do vídeo
├── exemplos/
│   ├── projecao_exemplo_apartamento.csv   # exemplo de CSV gerado
│   └── orcamento_exemplo_terminal.txt     # exemplo do orçamento exibido no terminal
└── saidas/                    # os CSVs gerados pelo programa são salvos aqui
```

## Como executar

1. Instale o Python 3 (https://www.python.org/downloads/). No Windows, marque a opção **"Add Python to PATH"**.
2. Baixe ou clone este repositório:
   ```bash
   git clone https://github.com/SEU-USUARIO/RentSmart.git
   cd RentSmart
   ```
3. Execute o programa a partir da pasta do projeto:
   ```bash
   python main.py
   ```
   (Em alguns sistemas o comando é `python3 main.py`.)
4. Para rodar os testes automáticos:
   ```bash
   python -m unittest discover testes -v
   ```

## Funcionalidades

- Menu inicial com as opções: fazer orçamento, consultar tabela de preços e sair.
- Escolha do tipo de imóvel: apartamento, casa ou estúdio.
- Perguntas conforme o imóvel: quantidade de quartos (1 ou 2) e vaga de garagem para casa/apartamento; pacote de vagas e vagas adicionais para estúdio; presença de crianças só para apartamento.
- Escolha do número de parcelas da taxa contratual (1 a 5).
- Validação de todas as respostas: o programa repete a pergunta quando o valor é inválido.
- Orçamento detalhado com aluguel-base, cada adicional, desconto, valor mensal final, taxa contratual em seção separada e tabela dos 12 meses.
- Geração automática do CSV em `saidas/projecao_<imovel>_<data_hora>.csv`, com as colunas Mês, Aluguel, Parcela da taxa, Taxa contratual e Total do mês, além de uma linha de totais. O arquivo usa `;` como separador para abrir corretamente no Excel em português.

## Regras de negócio

| Item | Valor |
|---|---|
| Apartamento (1 quarto) | R$ 700,00 |
| Casa (1 quarto) | R$ 900,00 |
| Estúdio | R$ 1.200,00 |
| 2º quarto — apartamento / casa | + R$ 200,00 / + R$ 250,00 |
| Vaga de garagem (casa ou apartamento) | + R$ 300,00 |
| Pacote de 2 vagas (estúdio) | + R$ 250,00 |
| Vaga adicional (estúdio) | + R$ 60,00 cada |
| Desconto apartamento, cliente sem crianças | 5% sobre o aluguel com adicionais |
| Taxa contratual (separada do aluguel) | R$ 2.000,00 em até 5x |

**Decisões sobre pontos ambíguos** (detalhadas no PDF): o desconto de 5% incide sobre base + quarto + garagem; vagas adicionais do estúdio só junto com o pacote; quando a taxa não divide exatamente, a última parcela recebe o ajuste de centavos; as parcelas começam no mês 1; o aluguel não tem reajuste na projeção.

## Exemplo

Apartamento, 2 quartos, com garagem, sem crianças, taxa em 3x:

- Aluguel: 700 + 200 + 300 = 1.200 → desconto de 5% (60) → **R$ 1.140,00 por mês**
- Taxa: 666,67 + 666,67 + 666,66 = R$ 2.000,00 (meses 1 a 3)
- Total previsto no 1º ano: **R$ 15.680,00**

Veja `exemplos/projecao_exemplo_apartamento.csv`.

## Links

- Vídeo pitch: *[cole aqui o link do YouTube]*

## Autor

Amanda Prado Aguiar — Gestão da Tecnologia da Informação, UniFECAF  
Professor: Vitor Jansen Vieira
