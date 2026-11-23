"""
Classes que representam os imóveis da R.M Imóveis.

Hierarquia (herança):

    Imovel                      -> regras comuns a todos os imóveis
    ├── ImovelResidencial       -> regras comuns a casas e apartamentos
    │   ├── Apartamento
    │   └── Casa
    └── Estudio

Cada classe guarda os próprios valores (aluguel-base, adicionais) e sabe
calcular o próprio aluguel. Assim, quem usa o objeto só precisa chamar
calcular_aluguel_mensal(), sem se preocupar com o tipo do imóvel
(polimorfismo).
"""


class Imovel:
    """Classe-mãe: define o 'roteiro' de cálculo usado por todos os imóveis."""

    TIPO = "Imóvel"          # nome exibido ao usuário
    CODIGO = "imovel"        # nome usado no arquivo CSV
    ALUGUEL_BASE = 0.0

    def calcular_aluguel_base(self):
        return self.ALUGUEL_BASE

    def calcular_adicional_quartos(self):
        return 0.0  # por padrão não há adicional (sobrescrito nas subclasses)

    def calcular_adicional_garagem(self):
        return 0.0

    def calcular_subtotal(self):
        """Aluguel-base + todos os adicionais (antes do desconto)."""
        return (self.calcular_aluguel_base()
                + self.calcular_adicional_quartos()
                + self.calcular_adicional_garagem())

    def calcular_desconto(self):
        return 0.0  # só o Apartamento tem desconto

    def calcular_aluguel_mensal(self):
        """Valor final do aluguel: subtotal menos o desconto."""
        return round(self.calcular_subtotal() - self.calcular_desconto(), 2)

    def descrever(self):
        """Texto curto com as características escolhidas."""
        return self.TIPO

    def detalhar_itens(self):
        """Lista de (descrição, valor) usada para montar o orçamento."""
        return [(f"Aluguel-base ({self.TIPO.lower()})", self.calcular_aluguel_base())]


class ImovelResidencial(Imovel):
    """Base para Casa e Apartamento: ambos têm 1 ou 2 quartos e 1 vaga opcional."""

    QUARTOS_PERMITIDOS = (1, 2)
    ADICIONAL_SEGUNDO_QUARTO = 0.0   # cada subclasse define o seu valor
    VALOR_GARAGEM = 300.00

    def __init__(self, quartos, tem_garagem):
        if quartos not in self.QUARTOS_PERMITIDOS:
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_adicional_quartos(self):
        if self.quartos == 2:
            return self.ADICIONAL_SEGUNDO_QUARTO
        return 0.0

    def calcular_adicional_garagem(self):
        if self.tem_garagem:
            return self.VALOR_GARAGEM
        return 0.0

    def descrever(self):
        garagem = "com vaga de garagem" if self.tem_garagem else "sem vaga de garagem"
        return f"{self.TIPO} — {self.quartos} quarto(s), {garagem}"

    def detalhar_itens(self):
        itens = [(f"Aluguel-base ({self.TIPO.lower()} de 1 quarto)",
                  self.calcular_aluguel_base())]
        itens.append(("Adicional de 2º quarto", self.calcular_adicional_quartos()))
        itens.append(("Vaga de garagem", self.calcular_adicional_garagem()))
        return itens


class Apartamento(ImovelResidencial):
    TIPO = "Apartamento"
    CODIGO = "apartamento"
    ALUGUEL_BASE = 700.00
    ADICIONAL_SEGUNDO_QUARTO = 200.00
    PERCENTUAL_DESCONTO = 0.05  # 5% para quem não possui crianças

    def __init__(self, quartos, tem_garagem, possui_criancas):
        super().__init__(quartos, tem_garagem)  # reaproveita o construtor da classe-mãe
        self.possui_criancas = possui_criancas

    def calcular_desconto(self):
        """5% sobre o valor já com os adicionais, só se NÃO houver crianças."""
        if self.possui_criancas:
            return 0.0
        return round(self.calcular_subtotal() * self.PERCENTUAL_DESCONTO, 2)

    def descrever(self):
        criancas = "possui crianças" if self.possui_criancas else "não possui crianças"
        return f"{super().descrever()}, {criancas}"

    def detalhar_itens(self):
        itens = super().detalhar_itens()
        if self.possui_criancas:
            itens.append(("Desconto 5% (não se aplica: há crianças)", 0.0))
        else:
            itens.append(("Desconto 5% (cliente sem crianças)", -self.calcular_desconto()))
        return itens


class Casa(ImovelResidencial):
    TIPO = "Casa"
    CODIGO = "casa"
    ALUGUEL_BASE = 900.00
    ADICIONAL_SEGUNDO_QUARTO = 250.00


class Estudio(Imovel):
    """Estúdio: não tem opção de quartos e usa a regra de pacote de vagas."""

    TIPO = "Estúdio"
    CODIGO = "estudio"
    ALUGUEL_BASE = 1200.00
    VALOR_PACOTE_VAGAS = 250.00   # pacote inicial com 2 vagas
    VAGAS_NO_PACOTE = 2
    VALOR_VAGA_ADICIONAL = 60.00

    def __init__(self, contrata_pacote, vagas_adicionais=0):
        if vagas_adicionais < 0:
            raise ValueError("A quantidade de vagas adicionais não pode ser negativa.")
        if not contrata_pacote and vagas_adicionais > 0:
            raise ValueError("Vagas adicionais só podem ser contratadas junto com o pacote.")
        self.contrata_pacote = contrata_pacote
        self.vagas_adicionais = vagas_adicionais

    def total_de_vagas(self):
        if not self.contrata_pacote:
            return 0
        return self.VAGAS_NO_PACOTE + self.vagas_adicionais

    def calcular_adicional_garagem(self):
        if not self.contrata_pacote:
            return 0.0
        return self.VALOR_PACOTE_VAGAS + self.vagas_adicionais * self.VALOR_VAGA_ADICIONAL

    def descrever(self):
        if not self.contrata_pacote:
            return f"{self.TIPO} — sem vagas de estacionamento"
        return f"{self.TIPO} — {self.total_de_vagas()} vaga(s) de estacionamento"

    def detalhar_itens(self):
        itens = super().detalhar_itens()
        if self.contrata_pacote:
            itens.append(("Pacote inicial de 2 vagas", self.VALOR_PACOTE_VAGAS))
            itens.append((f"Vagas adicionais ({self.vagas_adicionais} x R$ 60,00)",
                          self.vagas_adicionais * self.VALOR_VAGA_ADICIONAL))
        else:
            itens.append(("Estacionamento (não contratado)", 0.0))
        return itens
