# Roteiro do Vídeo Pitch — RentSmart (até 4 minutos)

**Duração planejada:** cerca de 3 min 50 s · **Formato:** gravação de tela com sua voz · **Publicação:** YouTube como "Não listado"

---

## Antes de gravar (preparação)

Deixe abertos, nesta ordem, para só trocar de janela durante o vídeo:

1. A página do seu repositório no GitHub (ou o README aberto no VS Code).
2. `docs/fluxograma.png`.
3. `docs/diagrama_classes.png`.
4. O VS Code com as abas `imoveis.py`, `taxa_contratual.py` e `orcamento.py`.
5. Um terminal já na pasta do projeto, com a tela limpa (`cls` no Windows ou `clear` no Mac/Linux).
6. A pasta `saidas/` vazia, para o CSV novo aparecer na hora.

Aumente a fonte do terminal e do VS Code (Ctrl + "+") para o professor conseguir ler no vídeo.

---

## Cena 1 — O problema (0:00 – 0:20)

**Na tela:** README do projeto no GitHub.

> "Olá, eu sou [seu nome] e este é o RentSmart. A imobiliária R.M Imóveis calculava os orçamentos de aluguel na mão, o que demorava e gerava erro em adicional, desconto e taxa de contrato. O RentSmart resolve isso: o atendente responde algumas perguntas e o sistema calcula tudo sozinho, mostra o orçamento detalhado e gera uma planilha com os 12 primeiros meses."

---

## Cena 2 — Fluxograma e lógica (0:20 – 0:50)

**Na tela:** `fluxograma.png`. Vá apontando com o mouse enquanto fala.

> "Antes de programar, eu montei este fluxograma. Do menu, o usuário escolhe o tipo de imóvel e o caminho se divide: casa e apartamento perguntam quartos e garagem, só o apartamento pergunta sobre crianças, e o estúdio pergunta sobre vagas. Depois tudo se junta: parcelas da taxa, cálculo, projeção de 12 meses e CSV. E toda resposta inválida faz a pergunta se repetir."

---

## Cena 3 — Estrutura de classes (0:50 – 1:25)

**Na tela:** `diagrama_classes.png`.

> "Nas classes: a Imovel tem a fórmula do aluguel, base mais adicionais menos desconto. Casa e Apartamento herdam de ImovelResidencial, porque têm quartos e garagem, e o Estúdio herda direto de Imovel. A TaxaContratual cuida do parcelamento, o Orcamento junta um imóvel e uma taxa, o ExportadorCSV grava o arquivo e a InterfaceTerminal conversa com o usuário."

---

## Cena 4 — Principais trechos do código (1:25 – 2:15)

**Na tela:** VS Code.

**4a — `imoveis.py`, métodos `calcular_subtotal` e `calcular_aluguel_mensal` da classe `Imovel`:**

> "Aqui está o cálculo, escrito uma vez só na classe-mãe. O subtotal soma base, adicional de quarto e garagem, e o aluguel mensal tira o desconto."

**4b — role até `class Apartamento`, método `calcular_desconto`:**

> "E aqui o polimorfismo: só o Apartamento reescreve o calcular_desconto, com cinco por cento se não houver crianças. Casa e estúdio usam o desconto zero da classe-mãe."

**4c — `taxa_contratual.py`, método `calcular_parcelas`:**

> "Na taxa, divido os dois mil reais pelas parcelas, e a última fica com o ajuste de centavos pra soma dar exatamente dois mil."

**4d — `orcamento.py`, método `gerar_projecao`:**

> "E o Orcamento faz um for de 1 a 12: em cada mês soma o aluguel com a parcela da taxa daquele mês, se ainda tiver parcela."

---

## Cena 5 — Demonstração de um orçamento completo (2:15 – 3:05)

**Na tela:** terminal. Digite exatamente:

| Pergunta | Digite |
|---|---|
| Comando | `python main.py` |
| Escolha uma opção | `1` |
| Tipo de imóvel | `1` (Apartamento) |
| Quantidade de quartos | `5` → mostre a mensagem de erro → depois `2` |
| Vaga de garagem | `S` |
| Possui crianças | `N` |
| Parcelas da taxa | `3` |

> "Agora rodando. Vou fazer um apartamento. Se eu digitar cinco quartos, ele recusa, porque só existem preços para um ou dois. Coloco dois, com garagem, cliente sem crianças, e a taxa em três vezes."

**Quando o orçamento aparecer, passe o mouse em cada linha:**

> "Olha o orçamento: setecentos de base, mais duzentos do quarto, mais trezentos da garagem, mil e duzentos. Com cinco por cento de desconto, fica mil cento e quarenta. A taxa aparece separada, em três parcelas. Na projeção, os três primeiros meses têm aluguel mais parcela, e depois só o aluguel."

Depois digite `0` para sair.

---

## Cena 6 — O arquivo CSV (3:05 – 3:30)

**Na tela:** abra a pasta `saidas/`, mostre o arquivo novo e abra no Excel (ou Google Planilhas / LibreOffice).

> "E aqui o CSV gerado automaticamente: mês, aluguel, qual parcela da taxa, valor da taxa e total do mês, com uma linha de totais no final. Os mesmos valores do terminal."

---

## Cena 7 — Como a POO ajudou + encerramento (3:30 – 3:55)

**Na tela:** volte ao `diagrama_classes.png`.

> "A orientação a objetos deixou o projeto organizado. Cada regra ficou na sua classe, então se um preço mudar, eu altero um lugar só. A herança evitou repetir o cálculo, o polimorfismo fez o orçamento funcionar com qualquer imóvel, e separar cálculo, arquivo e interface deixou tudo fácil de testar. Esse foi o RentSmart, obrigado!"

---

## Dicas finais

- Treine lendo em voz alta uma vez com cronômetro. Se passar de 4 minutos, encurte as falas da Cena 4.
- Não precisa decorar: fale com suas palavras seguindo a ordem das cenas.
- Ferramentas gratuitas para gravar: OBS Studio, ou a gravação de tela do próprio Windows (Win + Alt + R na Xbox Game Bar) ou do Mac (Cmd + Shift + 5).
- No YouTube, escolha a visibilidade **"Não listado"** e teste o link em uma aba anônima antes de enviar.
