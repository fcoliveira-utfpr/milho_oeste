# Planejamento do trabalho do Leonardo

**Título provisório.** Partição do yield gap do milho segunda safra no Oeste do Paraná com coeficiente ky calibrado

**Orientador.** Prof. Dr. Fabrício Correia de Oliveira (UTFPR, Campus Santa Helena)
**Duração.** 12 meses, organizados em etapas. Uma etapa começa quando a anterior foi entregue e conferida pelo orientador.
**Produtos.** Projeto de TCC (Etapa 0), artigo científico (alvo inicial *Agrometeoros* ou *Revista Brasileira de Engenharia Agrícola e Ambiental*) e resumo no SICITE.

| Onde fica o quê | Link |
|---|---|
| Projeto (texto, escrito na Etapa 0) | [Google Docs, Projeto_TCC1_Leonardo](https://docs.google.com/document/d/116Xqk0QABoqhPXf6kFE_XUrcNBp-UV9TzGH6DA15_QA/edit?usp=sharing) |
| Código, dados e notebooks | `github.com/fcoliveira-utfpr/milho_oeste` |
| Caderno de aprendizagem (antes dos notebooks do TCC) | [00_aprendizagem no Colab](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/00_aprendizagem.ipynb) |
| Resultados das análises | Seu Google Drive, pasta `milho_oeste/resultados` (criada pelos notebooks) |
| Referências | Grupo da biblioteca Zotero do orientador |

---

## Sumário

- [Como ler este documento](#como-ler-este-documento)
- [A pesquisa em uma página](#a-pesquisa-em-uma-página)
- [Como o trabalho roda no Colab](#como-o-trabalho-roda-no-colab)
- [Etapa 0. Escrita do projeto](#etapa-0-escrita-do-projeto)
- [Caderno de aprendizagem](#caderno-de-aprendizagem)
- [Etapa 1. Python básico no Colab](#etapa-1-python-básico-no-colab)
- [Etapa 2. Dados de produtividade e clima](#etapa-2-dados-de-produtividade-e-clima)
- [Etapa 3. O MZA-FAO em um município e um ano](#etapa-3-o-mza-fao-em-um-município-e-um-ano)
- [Etapa 4. Simulação dos 50 municípios](#etapa-4-simulação-dos-50-municípios)
- [Etapa 5. Verificação da produtividade potencial](#etapa-5-verificação-da-produtividade-potencial)
- [Etapa 6. Calibração e validação do ky](#etapa-6-calibração-e-validação-do-ky)
- [Etapa 7. Produtividade atingível e partição do yield gap](#etapa-7-produtividade-atingível-e-partição-do-yield-gap)
- [Etapa 8. DSSAT CERES-Maize e ky emergente](#etapa-8-dssat-ceres-maize-e-ky-emergente)
- [Etapa 9. Figuras e tabelas do artigo](#etapa-9-figuras-e-tabelas-do-artigo)
- [Etapa 10. Escrita do artigo](#etapa-10-escrita-do-artigo)
- [Pontos de decisão, riscos e referências](#pontos-de-decisão-com-o-orientador)

---

## Como ler este documento

Este é o roteiro do seu trabalho, do projeto ao artigo. Cada etapa tem:

1. **Objetivo**: o que a etapa resolve e por que ela existe;
2. **Botão "Open in Colab"**: abre o notebook da etapa no navegador, pronto para rodar;
3. **O que o notebook faz**: as seções do notebook, na ordem;
4. **Trechos de código explicados**: os blocos mais importantes, para você entender antes de rodar;
5. **O que observar**: o que conferir nos resultados e a ordem de grandeza esperada (do teste feito pelo orientador);
6. **Entregar**: o critério para passar à etapa seguinte;
7. **O que escrever**: o trecho do projeto ou do artigo que nasce daquela etapa.

Há dois tipos de notebook. O **caderno de aprendizagem** (`00_aprendizagem`) é um só, separado em nove capítulos, e ensina em exemplos pequenos cada ideia e cada ferramenta da pesquisa. Os **notebooks do TCC** (`01` a `09`) são a pesquisa em si. A ordem é: primeiro o caderno de aprendizagem inteiro, depois os notebooks 01 a 09 (ver [Caderno de aprendizagem](#caderno-de-aprendizagem)).

Você não precisa saber programar para começar. A programação é aprendida fazendo. Os notebooks são comentados linha a linha, e as funções difíceis (balanço hídrico, produtividade potencial e atingível) já existem na biblioteca `agrometeorologiapy`, desenvolvida pelo orientador, e nos arquivos da pasta `src/`. Seu trabalho é rodar, entender cada passo, interpretar os resultados e escrever.

---

## A pesquisa em uma página

### Pergunta

Quanto da diferença entre o que o milho segunda safra poderia produzir no Oeste do Paraná e o que o produtor de fato colhe vem da falta de água, quanto vem da data de semeadura e quanto vem do manejo? Essas proporções mudam entre municípios e entre anos?

### Níveis de produtividade

```
PP  produtividade potencial     radiação + temperatura + genótipo, sem falta de água
 │      YG_hídrico = PP − PA     (dividido em: inevitável + evitável pela data de semeadura)
PA  produtividade atingível     PP penalizada pelo déficit hídrico de cada fase, via ky
 │      YG_manejo  = PA − PR
PR  produtividade real          IBGE, Produção Agrícola Municipal (PAM)

YG_total = PP − PR = YG_inevitável + YG_data + YG_manejo
```

Esse esquema é o mesmo de Sentelhas et al. (2015) e do *Global Yield Gap Atlas* (GYGA; van Ittersum et al., 2013; Grassini et al., 2015). No Brasil, o grupo de Zanon, Streck e Grassini (UFSM e Universidade de Nebraska) aplica o mesmo raciocínio à soja e ao milho com modelos de processo e levantamentos de lavoura (Soares et al., 2025).

Dois indicadores acompanham o trabalho: a **eficiência climática** EC = PA/PP (quanto do potencial o clima deixa produzir) e a **eficiência de manejo** EM = PR/PA (quanto do atingível o produtor colhe).

### A contribuição

1. **Calibração do ky por fase** para o milho segunda safra do Oeste do Paraná, com dados públicos (IBGE e clima em grade de Xavier et al.). Os valores de Doorenbos & Kassam são de 1979, de outros ambientes e outras cultivares.
2. **Calibração sem raciocínio circular.** Calibrar o ky contra a média do IBGE faria o ky absorver o manejo, e o yield gap de manejo desapareceria por construção. O trabalho calibra contra quebras **relativas** (Etapa 6).
3. **Partição do gap em três parcelas**: déficit hídrico inevitável, data de semeadura e manejo.
4. **Verificação com um modelo de processo** (DSSAT CERES-Maize).

### Objetivos

**Geral.** Quantificar o yield gap do milho segunda safra nos 50 municípios do Oeste do Paraná e particioná-lo entre déficit hídrico, data de semeadura e manejo, a partir de coeficientes de resposta ao déficit hídrico (ky) calibrados regionalmente.

**Específicos.**

- Estimar a produtividade potencial pelo Modelo da Zona Agroecológica da FAO (MZA-FAO) e confrontá-la com as maiores produtividades observadas na região;
- Calibrar e validar o ky por fase fenológica pelas estratégias de envoltória superior e de anomalia sem tendência;
- Quantificar a produtividade atingível e as parcelas do yield gap e espacializá-las por município;
- Analisar a tendência temporal do yield gap de manejo e a variabilidade interanual do yield gap hídrico;
- Comparar o ky calibrado com o de Doorenbos & Kassam e com o ky emergente do DSSAT CERES-Maize.

### Hipóteses

- O ky calibrado na floração é menor que o tabelado (1,5), porque os híbridos atuais toleram melhor o déficit nessa fase.
- O déficit hídrico domina o yield gap nos anos secos e na faixa oeste da mesorregião, e o yield gap de manejo diminui ao longo da série.

---

## Como o trabalho roda no Colab

**Todas as análises rodam no Google Colab**, no navegador, sem instalar nada no computador.

### O repositório do projeto

```
github.com/fcoliveira-utfpr/milho_oeste
├── planejamento.md              este documento
├── dados/
│   ├── municipios_oeste.csv          50 municípios: coordenadas, altitude, CAD do solo, argila, areia
│   ├── ibge_pam_milho_oeste.csv      produtividade, área e produção do milho (1ª e 2ª safra), 2003 a 2025
│   ├── clima_oeste.parquet           clima diário de Xavier et al. na sede de cada município, 1998 a 2025
│   ├── solo_camadas_oeste.csv        argila e areia em camadas de 10 cm (MapBiomas Solo), para o DSSAT
│   └── malha_municipios_oeste.geojson limites municipais, para os mapas
├── src/
│   ├── mza_oeste.py             MZA-FAO: simulação de um ciclo, laço por município, eficiência climática
│   ├── avaliacao.py             índices estatísticos: RMSE, MBE, r, d de Willmott, NSE, KGE
│   └── dssat_oeste.py           DSSAT CERES-Maize: clima, solo, cultivar, sequeiro e irrigado
└── notebooks/                   00 = caderno de aprendizagem; 01 a 09 = notebooks do TCC, um por etapa
```

### A célula 0 de cada notebook

Todo notebook começa com a mesma célula de preparação. **Rode-a sempre primeiro**, toda vez que abrir o notebook. No Colab, ela:

1. instala as bibliotecas que faltam (`!pip install agrometeorologiapy`, e `DSSATTools` no notebook 08);
2. copia o repositório com `git clone` (dados + funções) para a máquina do Colab; se já foi copiado na sessão, só atualiza com `git pull`;
3. conecta o seu **Google Drive** e cria a pasta `milho_oeste/resultados`.

```python
NO_COLAB = "google.colab" in sys.modules
if NO_COLAB:
    !pip -q install agrometeorologiapy==1.0.1
    !git clone -q https://github.com/fcoliveira-utfpr/milho_oeste.git /content/milho_oeste
    os.chdir("/content/milho_oeste")
    drive.mount("/content/drive")
    SAIDA = Path("/content/drive/MyDrive/milho_oeste/resultados")
```

- `!` no início da linha manda o comando para o terminal do Colab.
- **O Colab apaga tudo quando a sessão fecha** (inatividade, fim do dia). Por isso cada etapa grava seus resultados no Drive (`SAIDA`), e a etapa seguinte lê de lá. Os notebooks 05 a 09 dependem dos arquivos gravados pelos anteriores.

### Regras de trabalho

- **Rode as células em ordem**, de cima para baixo. Se algo der um erro estranho, use *Ambiente de execução → Reiniciar e executar tudo*.
- **Não edite o notebook original.** Use *Arquivo → Salvar uma cópia no Drive* e trabalhe na cópia.
- **Escreva, em células de texto, o que você entendeu de cada resultado.** Isso vira o rascunho do artigo.
- **Exercícios**: cada notebook termina com perguntas. Responda na célula vazia logo abaixo.
- **Erro é normal.** Leia a última linha da mensagem de erro. Antes de pedir ajuda, tente entender o que ela diz; depois, mande ao orientador o print do erro e o que você tentou.

---

## Etapa 0. Escrita do projeto

**Objetivo.** Escrever o projeto do TCC no [Google Docs do projeto](https://docs.google.com/document/d/116Xqk0QABoqhPXf6kFE_XUrcNBp-UV9TzGH6DA15_QA/edit?usp=sharing). O projeto obriga a entender a pergunta, o método e a literatura **antes** de rodar qualquer análise, e boa parte dele vira a Introdução e o Material e Métodos do artigo.

### Como o documento está organizado

O documento já tem a formatação da UTFPR (capa, folha de rosto, resumo, abstract, sumário, seções e cronograma). Em cada tópico há:

- **texto em azul e itálico**: orientação do que escrever. Apague à medida que escrever;
- **texto em preto**: exemplo, que pode ser mantido, adaptado ou substituído.

Escreva os textos e quando estiver uma boa quantidade avancada, informe o orientador e avise o que mudou. Use os comentários do Google Docs para dúvidas pontuais.

### Antes de escrever

1. Recomendo que **Faça as leituras de base, nesta ordem**, com uma ficha de meia página para cada uma:

| Ordem | Referência | Para qual seção do projeto |
|---|---|---|
| 1 | Doorenbos & Kassam (1979), *FAO 33*, cap. 1 a 3 | 3.4, 3.5 |
| 2 | Allen et al. (1998), *FAO 56*, cap. 1, 2 e 6 | 3.2 |
| 3 | Sentelhas et al. (2015) | 1, 3.3 |
| 4 | Andrea et al. (2018) | 3.3 |
| 5 | Battisti et al. (2018) | 3.4, 4.4 |
| 6 | da Silva et al. (2019) | 3.5 |
| 7 | van Ittersum et al. (2013); Grassini et al. (2015) | 3.3 |
| 8 | Soares et al. (2025) | 1, 3.3 |
| 9 | Affholder et al. (2013); Djaman et al. (2013) | 3.4, 3.5 |
| 10 | Xavier et al. (2022) | 3.6 |

### Ordem de escrita

Não escreva na ordem do sumário. A ordem que funciona é:

1. **Objetivos (2).** Já há exemplos. Leia, entenda e ajuste. Se você não conseguir explicar cada objetivo com suas palavras, volte às leituras.
2. **Referencial teórico (3).** Uma subseção por vez, a partir das fichas. Cada parágrafo termina com citação.
3. **Metodologia (4).** Escreva no futuro, com as equações numeradas. Use o próprio planejamento e os notebooks das Etapas 3, 6 e 7 como guia (as equações estão lá).
4. **Introdução (1).** Em funil: importância do milho → Paraná e Oeste → risco climático da safrinha → yield gap → lacuna → hipótese e objetivo. Já há três parágrafos de exemplo.
5. **Cronograma (5).** Ajuste os meses ao início real do trabalho. Cada linha corresponde a uma etapa deste planejamento.
6. **Resumo e abstract.** Por último, quando todo o resto estiver pronto.

### Regras de estilo

- **Títulos sem dois-pontos.**
- **Sem primeira pessoa**: "neste trabalho", "nesta pesquisa".
- **Toda afirmação tem citação**, ao final do parágrafo: (SENTELHAS et al., 2015).
- **Equações numeradas**, (1), (2)..., seguidas de "em que:" e da descrição de cada variável, com unidade.
- **Quando faltar um número, deixe o marcador** [INSERIR VALOR]. Nunca invente.
- Antes de entregar, apague todos os textos em azul e confira se todo autor citado está nas referências, e vice-versa.

### Entregar

O projeto completo no Google Docs, sem textos em azul, revisado pelo orientador. Depois de aprovado, exporte em PDF e docx para a entrega formal.

---

## Caderno de aprendizagem

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/00_aprendizagem.ipynb)

**Objetivo.** Aprender, antes da pesquisa, cada ideia e cada ferramenta que os notebooks do TCC usam. Os notebooks 01 a 09 rodam o trabalho completo (50 municípios, calibração, partição), e muita coisa acontece em poucas linhas. O caderno de aprendizagem separa essas coisas em exemplos pequenos, para você chegar aos notebooks do TCC sabendo o que cada passo faz.

### Como ele está organizado

É **um único notebook**, com **um capítulo para cada notebook do TCC**, na mesma ordem. Em cada capítulo há dois tipos de item:

- **Resolvido**: o exemplo vem pronto, com explicação e comentários. Rode, leia e mude os valores para ver o efeito;
- **Para pensar e resolver**: perguntas para responder com código ou com texto, na célula vazia abaixo. Umas pedem uma conta; outras pedem que você explique um resultado com suas palavras.

| Capítulo | O que ensina | Prepara para |
|---|---|---|
| 1 | Funções, laços e decisões com a soma térmica (graus-dia, dias até a maturação) | Etapa 1 |
| 2 | pandas com a série do IBGE: tendência tecnológica, anomalia, chuva da safrinha | Etapa 2 |
| 3 | Balanço hídrico de "balde" feito à mão, ISNA e a equação do ky | Etapa 3 |
| 4 | Laços de simulação com `M.simular`, resumo por grupo, gravar e retomar | Etapa 4 |
| 5 | PP × IBGE: junção de tabelas, gráfico 1:1 e quantis | Etapa 5 |
| 6 | Índices de desempenho, calibração em dados sintéticos (grade, otimizador, validação) e o raciocínio circular | Etapa 6 |
| 7 | Partição do yield gap com números simples, o limite do YG_data, Mann-Kendall e Sen | Etapa 7 |
| 8 | Ky emergente por mínimos quadrados e o efeito da soma térmica no ciclo | Etapa 8 |
| 9 | Figura com dois painéis em 300 dpi e tabela para o artigo | Etapa 9 |

### Como usar

1. Faça o caderno **inteiro, do capítulo 1 ao 9, antes de abrir o notebook 01 do TCC**. Ele pode ser feito ao mesmo tempo que a escrita do projeto (Etapa 0): os capítulos 3, 6 e 7 ajudam a escrever a Metodologia.
2. Os itens resolvidos rodam em poucos segundos cada um, e nada precisa ser gravado no Drive.
3. As respostas dos itens "para pensar e resolver" são a pauta das reuniões com o orientador.

**Entregar.** O caderno com todos os itens "para pensar e resolver" respondidos. O item 1 do capítulo 6 (o raciocínio circular) é o mais importante: sem entendê-lo, a Etapa 6 não faz sentido.

---

## Etapa 1. Python básico no Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/01_python_basico.ipynb)

**Antes desta etapa:** capítulo 1 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Aprender o mínimo de Python para seguir o projeto, usando exemplos de agrometeorologia.

**O que o notebook faz.**

1. Variáveis e contas (temperatura média, amplitude térmica);
2. Listas e o laço `for` (chuva acumulada de uma semana);
3. Decisões com `if` (risco de geada, Tmin ≤ 2 °C);
4. Funções (graus-dia, a base da fenologia do milho);
5. Dicionários (os ky de cada fase);
6. Tabelas com pandas (o clima diário de Santa Helena);
7. A ETo de um dia, passo a passo, com as funções da biblioteca (Penman-Monteith FAO 56);
8. A ETo de um mês e o gráfico comparando com a ETo da base Xavier.

**Trecho explicado: uma função**

```python
def graus_dia(tmax, tmin, tb=10.0):
    tmed = (tmax + tmin) / 2
    return max(tmed - tb, 0.0)      # abaixo de Tb a planta não se desenvolve
```

`def` cria uma função: uma receita que recebe valores e devolve um resultado com `return`. `tb=10.0` é um valor padrão, que pode ser omitido na chamada.

**O que observar.** A ETo calculada para 01/03/2020 em Santa Helena fica em torno de 6,1 mm/dia, perto dos 6,2 mm/dia da base Xavier. Pense por que não são idênticas.

**Entregar.** O notebook com os dois exercícios resolvidos e um parágrafo, com suas palavras, explicando o que é a ETo e de que variáveis ela depende.

---

## Etapa 2. Dados de produtividade e clima

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/02_dados_ibge_clima.ipynb)

**Antes desta etapa:** capítulo 2 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Conhecer os dados: quanto o Oeste produz, como a produtividade evoluiu e quais anos tiveram quebra.

**O que o notebook faz.**

1. Resume os municípios (altitude, CAD, argila e areia);
2. Calcula a série regional da produtividade (média simples, ponderada pela área e percentil 90) e a tendência tecnológica;
3. Calcula a anomalia de cada ano em relação à tendência e lista os anos de quebra;
4. Resume o clima da safrinha (fevereiro a junho) e relaciona o balanço chuva − ETo com a anomalia.

**Trecho explicado: tendência tecnológica**

```python
a, b = np.polyfit(anual.index, anual["ponderada"], 1)   # reta: rendimento = a·ano + b
```

A inclinação `a` é o **ganho tecnológico**: quanto a produtividade cresce por ano por genética e manejo. É por isso que comparar 2005 com 2025 diretamente não faz sentido: a tendência precisa ser retirada.

**O que observar.** Ganho tecnológico perto de 110 kg/ha por ano; 2021 é o pior ano da série (cerca de 40% abaixo da tendência), seguido de 2009, 2005 e 2004. A correlação entre o balanço chuva − ETo e a anomalia é moderada (cerca de 0,5): o clima explica parte, mas não toda a variação, porque importa **quando** falta água, e há também a geada.

**Entregar.** Figura da série (`fig_serie_produtividade.png`), a lista dos três piores anos com a causa de cada um (boletins do DERAL/SEAB) e a tabela dos 10 municípios de maior área.

**O que escrever.** No projeto, item 4.2 (dados). No artigo, a subseção *Área de estudo e dados*.

---

## Etapa 3. O MZA-FAO em um município e um ano

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/03_mza_um_ciclo.ipynb)

**Antes desta etapa:** capítulo 3 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Entender, passo a passo, o que o modelo faz num único ciclo (Santa Helena, semeadura em 05/02).

**O que o modelo faz, dia a dia.**

1. Soma os graus-dia (Tb = 10 °C) até 1.450 °C dia, a maturação de um híbrido precoce;
2. Divide o ciclo nas cinco fases de Doorenbos & Kassam: estabelecimento (15% da soma térmica), vegetativo (30%), floração (12%), enchimento (30%) e maturação (13%);
3. Calcula a ETc = Kc × ETo (Kc de 0,3 a 1,2) e faz a raiz crescer de 0,10 a 0,40 m até o fim do vegetativo;
4. Faz o balanço hídrico da cultura (30 dias de aquecimento antes da semeadura) e obtém a ETR;
5. Calcula a PP pela radiação e temperatura (IAF = 5, índice de colheita 0,40, umidade 13%);
6. Penaliza a PP pelo déficit de cada fase com o ky e obtém a PA.

**Trecho explicado: o produtório, na mão**

```python
fator = 1.0
for f in M.FASES:
    perda = M.KY_DK[f] * (1 - r[f"ISNA_{f}"])   # fração perdida na fase
    fator = fator * max(1 - perda, 0)
```

PA = PP × Π [1 − ky,i (1 − ETRi/ETci)]. O **ISNA** (ETR/ETc) de cada fase resume a falta de água. Conhecidos o ISNA e a PP, a PA sai dessa conta simples para **qualquer** ky. Por isso a simulação é feita uma vez (Etapa 4), e a calibração (Etapa 6) só refaz esse produto.

**O que observar.** Em 2019, PP ≈ 6.100 e PA ≈ 3.160 kg/ha; em 2020 (estiagem), PA ≈ 70 kg/ha, quase zero, enquanto o IBGE registrou 2.200 kg/ha. Essa é a primeira pista de que o ky tabelado, no produtório, pune demais. A PP de 6.000 a 7.000 kg/ha também é baixa perto das produtividades atuais, o que será tratado na Etapa 5.

**Entregar.** Os gráficos dos ciclos de 2019 e 2020 e as respostas aos exercícios (efeito da data de semeadura; PA de 2020 com ky da floração = 0,8).

**O que escrever.** Item 4.3 do projeto e a subseção *Modelo da Zona Agroecológica da FAO* do artigo, com as equações da fenologia, do balanço hídrico, da PP e da PA.

---

## Etapa 4. Simulação dos 50 municípios

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/04_simulacao_oeste.ipynb)

**Antes desta etapa:** capítulo 4 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Rodar o MZA-FAO para 50 municípios × 27 anos (1999 a 2025) × 9 datas de semeadura (dias 5, 15 e 25 de janeiro, fevereiro e março): 12.150 ciclos. É a base de todas as etapas seguintes.

**O que o notebook faz.**

1. Laço sobre os municípios; cada município é gravado num arquivo próprio no Drive (`simulacao_parcial/`), então, se o Colab cair, basta rodar de novo e os prontos são pulados;
2. Junta tudo em `simulacao_mza_oeste.parquet`;
3. Resume PP, PA e ISNA por data de semeadura;
4. Calcula a PA média da janela usual de semeadura (15/01, 05/02, 25/02 e 15/03), que é a comparável com o IBGE.

**Trecho explicado: retomar de onde parou**

```python
arquivo = parcial / f"{m.cod_ibge}.parquet"
if arquivo.exists():
    continue                     # já simulado numa sessão anterior: pula
```

**O que observar.** Cerca de 8 a 10 segundos por município, 6 a 8 minutos ao todo. A PP cai das semeaduras de janeiro para as de março (menos radiação e temperatura no outono).

**Entregar.** O arquivo `simulacao_mza_oeste.parquet` no Drive, a figura `fig_pp_pa_data.png` e as respostas aos exercícios.

---

## Etapa 5. Verificação da produtividade potencial

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/05_verificacao_pp.ipynb)

**Antes desta etapa:** capítulo 5 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Conferir se a PP está numa faixa realista antes de calibrar. A PP é o teto: com manejo perfeito e sem falta de água, nenhum município deveria colher acima dela de forma sistemática.

**O que o notebook faz.**

1. Conta quantas vezes a PR do IBGE passa da PP;
2. Compara a PP com o percentil 95 e a média do IBGE ano a ano;
3. Pede que você complete uma tabela com o topo dos ensaios de cultivares do IDR-Paraná e as estimativas do GYGA;
4. Propõe um **fator de ajuste da PP** e grava a decisão em `parametros.json`.

**Trecho explicado: o fator equivale a outro índice de colheita**

No MZA-FAO, a PP é proporcional ao índice de colheita (Cc). O projeto usa Cc = 0,40, valor da época de Doorenbos & Kassam; híbridos modernos chegam perto de 0,50. Multiplicar a PP por um fator equivale a usar Cc = 0,40 × fator.

```python
fator_proposto = np.quantile(recentes["PR_sobre_PP"], 0.95)   # PP acima de 95% das PR recentes
```

**O que observar.** A PR passa da PP em cerca de 15% dos município-anos, e em 31% dos anos recentes: a PP está subestimada. O fator proposto fica perto de 1,2 (Cc ≈ 0,48), plausível para híbridos atuais.

**Entregar.** A figura `fig_pp_vs_ibge.png`, a tabela IDR/GYGA preenchida e a decisão sobre o fator, tomada com o orientador.

**O que escrever.** No artigo, como a PP foi verificada e ajustada, com a justificativa do índice de colheita.

---

## Etapa 6. Calibração e validação do ky

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/06_calibracao_ky.ipynb)

**Antes desta etapa:** capítulo 6 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Encontrar os ky de cada fase que fazem a quebra simulada reproduzir a quebra observada. É a etapa central do trabalho.

### Por que não calibrar contra a média do IBGE

PR = PA − perda por manejo. Se o ky for ajustado para a PA reproduzir a média do IBGE, ele aprende também o manejo, e o yield gap de manejo some por construção. A solução é calibrar contra **quebras relativas**, em que o manejo varia pouco:

- **Estratégia A, envoltória superior.** Em cada ano, o percentil 90 dos municípios (quem maneja bem), dividido pela tendência desse percentil (regressão quantílica, q = 0,9). São 23 pontos, um por ano.
- **Estratégia B, anomalia sem tendência.** Em cada município, a produtividade dividida pelo "teto" da própria série (regressão quantílica, q = 0,9). São cerca de 1.140 pontos.

### O detalhe que decide o resultado

O teto do IBGE é a produtividade dos **anos bons**, e mesmo nos anos bons houve algum déficit. A produtividade relativa observada é, portanto, a eficiência climática **em relação à dos anos bons**. O lado simulado é normalizado da mesma forma: a EC de cada ano dividida pelo quantil 0,9 da EC do município. Sem essa normalização, o otimizador empurra todos os ky para o limite inferior (o notebook mostra como testar isso).

### O que o notebook faz

1. Calcula a produtividade relativa observada (A e B);
2. Define o lado simulado normalizado;
3. **Busca em grade**: 8.000 combinações de ky (vegetativo, floração, enchimento, de 0,1 a 2,0), com o mapa da superfície do erro;
4. **Otimização numérica** (`scipy.optimize.minimize`, limites de 0,05 a 2,5), partindo dos valores tabelados;
5. **Validação deixando um ano de fora**: calibra com 22 anos e testa no ano retirado, para cada ano;
6. Tabela final do ky e gravação em `ky_calibrado.json`.

Estabelecimento (0,4) e maturação (0,2) ficam nos valores de Doorenbos & Kassam: com 23 anos, calibrar os cinco ky dá sobreajuste.

**Trecho explicado: o erro que o otimizador minimiza**

```python
def erro(x, estrategia, anos=None):
    o, s = (obs_A, sim_A(x)) if estrategia == "A" else (obs_B, sim_B(x))
    o, s = o.align(s, join="inner")      # só os pares que existem nos dois lados
    ...
    return rmse(o, s)
```

**O que observar (teste do orientador).**

| | Vegetativo | Floração | Enchimento |
|---|---|---|---|
| Doorenbos & Kassam | 0,40 | 1,50 | 0,50 |
| Estratégia B | 0,45 | 0,51 | 0,16 |
| Estratégia B, faixa da validação (5–95%) | 0,42–0,47 | 0,48–0,55 | 0,14–0,18 |

- A estratégia B é estável: grade e otimizador chegam ao mesmo ponto, e o ky varia pouco entre as rodadas da validação. Na validação, o RMSE cai de 0,28 (ky tabelado) para 0,17, e o NSE passa de −1,4 para 0,1.
- O ky da floração calibrado (≈ 0,5) é **um terço** do tabelado, o que apoia a primeira hipótese.
- A superfície do erro tem um "vale" comprido: várias combinações dão erro parecido. Discuta isso.
- A estratégia A (23 pontos) colapsa no limite inferior no vegetativo e no enchimento: poucos pontos e a média regional suaviza as quebras. Discuta por que a B é mais confiável.

**Entregar.** A tabela do ky, a tabela de desempenho, as figuras `fig_superficie_erro.png` e `fig_dispersao_validacao.png` e as respostas aos exercícios.

**O que escrever.** Item 4.4 do projeto; no artigo, a subseção *Calibração e validação do coeficiente ky* (raciocínio circular, as duas estratégias, a normalização, grade, otimizador e validação) e os resultados da calibração, comparando com da Silva et al. (2019).

---

## Etapa 7. Produtividade atingível e partição do yield gap

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/07_yield_gap.ipynb)

**Antes desta etapa:** capítulo 7 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Calcular a PA com o ky calibrado e dividir o yield gap em três parcelas.

### O nível da PA, um ponto de decisão

A PA precisa ficar **acima** da PR na grande maioria dos casos: o produtor não colhe mais do que a água permite. O notebook compara duas formas de calcular a PA:

| Nível | Fórmula | PA média | % com PR > PA |
|---|---|---|---|
| absoluto | PA = PP × EC | ≈ 4.470 kg/ha | ≈ 63% |
| normalizado | PA = PP × EC / EC₉₀ do município | ≈ 6.390 kg/ha | ≈ 13% |

No nível absoluto, o yield gap de manejo sairia negativo na maioria dos casos. Isso mostra que o balanço hídrico do MZA, com o clima da sede do município e raiz até 0,40 m, **superestima o patamar** do déficit, embora acerte a forma das quebras entre anos. O nível normalizado usa a mesma escala da calibração e admite que, nos anos bons de cada município, a água não limitou. O DSSAT (Etapa 8) ajuda a decidir. A escolha é feita com o orientador e precisa ser justificada no artigo.

### A partição

```
YG_total      = PP_janela − PR
YG_hídrico    = PP_janela − PA_janela
  YG_data       = parte do YG_hídrico que a melhor data de semeadura evitaria (PA_melhor − PA_janela, limitado ao YG_hídrico)
  YG_inevitável = YG_hídrico − YG_data
YG_manejo     = PA_janela − PR
YG_total = YG_inevitável + YG_data + YG_manejo
```

A melhor data de cada município é a de maior PA média ao longo dos anos. Também é calculado o **gap explorável**, 0,8 × PA − PR, porque na prática os melhores produtores chegam a cerca de 80% da PA (van Ittersum et al., 2013).

**O que o notebook faz.**

1. Compara os dois níveis da PA e registra a decisão;
2. Encontra a melhor data de cada município e calcula as parcelas;
3. Resume a partição (média simples e ponderada pela área colhida);
4. Faz o gráfico de barras empilhadas por ano;
5. Testa a tendência das parcelas (Mann-Kendall e inclinação de Sen);
6. Faz os mapas das três parcelas;
7. Compara a partição com o ky tabelado e com o calibrado.

**O que observar (teste do orientador, nível normalizado).**

- Partição ponderada pela área: inevitável ≈ 28%, data ≈ 27%, manejo ≈ 45% do YG_total (≈ 2.500 kg/ha).
- A melhor data é 05/01 em 38 municípios e 15/01 em 12, a semeadura mais cedo possível após a soja.
- YG_manejo **diminui** cerca de 100 kg/ha por ano (Mann-Kendall, p < 0,001); YG_hídrico não tem tendência. Isso apoia a segunda hipótese.
- Mapas: o gap hídrico inevitável é maior na faixa oeste (Guaíra, Santa Helena e a fronteira), e o de manejo é maior no leste da mesorregião.
- Com o ky tabelado, o manejo responderia por −7% do gap (sem sentido); com o calibrado, por cerca de 50%. Esse contraste mostra por que calibrar importa.

**Entregar.** A tabela da partição, as figuras `fig_particao_ano.png` e `fig_mapas_yield_gap.png`, os testes de tendência e as respostas aos exercícios. Extensão opcional: relação do YG_hídrico com o ENSO (índice ONI da NOAA).

**O que escrever.** O núcleo de Resultados e Discussão.

---

## Etapa 8. DSSAT CERES-Maize e ky emergente

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/08_dssat_ky_emergente.ipynb)

**Antes desta etapa:** capítulo 8 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Ponto de decisão.** Esta etapa só começa com as Etapas 6 e 7 concluídas e conferidas. Se o tempo apertar, o artigo se sustenta sem ela, e o DSSAT vai para a discussão como trabalho futuro.

**Objetivo.** Usar um modelo de processo como segunda opinião sobre o déficit hídrico, em cinco municípios: Santa Helena, Cascavel, Toledo, Guaíra e o de solo mais arenoso (Diamante D'Oeste).

**O que o notebook faz.**

1. Instala o `DSSATTools` (no Colab, o DSSAT roda direto, porque o pacote traz o programa para Linux);
2. **Calibra a fenologia da cultivar**: você ajusta P1 e P5 até o florescimento ficar perto de 60 dias e a maturação perto de 120 dias (semeadura em fevereiro), e G2 e G3 até a produtividade irrigada ficar perto do topo dos ensaios do IDR-Paraná;
3. Roda sequeiro e irrigado (irrigação automática) nas 4 datas da janela × 27 anos;
4. Calcula a perda pelo déficit segundo o DSSAT (1 − sequeiro/irrigado);
5. Ajusta o **ky emergente**: o ky que faz o ISNA do MZA reproduzir a perda do DSSAT;
6. Compara os três ky e a PP/PA dos dois modelos.

**Trecho explicado: alterar a cultivar**

```python
COEF = {"P1": 280, "P5": 900, "G2": 750, "G3": 8.5}   # ponto de partida
```

| Coeficiente | O que controla |
|---|---|
| P1 | soma térmica até o fim da fase juvenil: atrasa o florescimento |
| P5 | soma térmica do florescimento à maturação: alonga o enchimento |
| G2 | número máximo de grãos por planta |
| G3 | taxa de enchimento dos grãos |

**O que observar (teste do orientador).** Com o ponto de partida, o florescimento ocorre em cerca de 59 dias, a maturação em cerca de 126 dias, e a produtividade irrigada fica em torno de 11.900 kg/ha. A perda média pelo déficit segundo o DSSAT é de só **9%**, contra 70% no MZA com o ky tabelado: o perfil do DSSAT tem 180 cm e a raiz explora água em profundidade. Por isso o ky emergente também cai no limite inferior. Esse contraste é um resultado: ele reforça que o patamar do déficit do MZA está superestimado e ajuda a justificar o nível normalizado da Etapa 7. Teste sugerido: em `src/mza_oeste.py`, mude `Z_MAX` para 0,7 ou 1,0 m e refaça a Etapa 4.

**Entregar.** Os coeficientes finais da cultivar com a justificativa, a tabela dos três ky (`tabela_tres_ky.csv`) e a figura `fig_dssat_vs_mza.png`.

**O que escrever.** Item 4.6 do projeto; no artigo, uma subseção de Resultados e Discussão sobre a comparação entre os modelos.

---

## Etapa 9. Figuras e tabelas do artigo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/09_figuras_artigo.ipynb)

**Antes desta etapa:** capítulo 9 do [caderno de aprendizagem](#caderno-de-aprendizagem).

**Objetivo.** Gerar, num único lugar e com o mesmo padrão visual, as figuras e tabelas finais, em 300 dpi, na pasta `figuras_artigo/` do Drive.

| Fig./Tab. | Conteúdo | Origem |
|---|---|---|
| Fig. 1 | Mapa da área de estudo com a CAD do solo | 09 |
| Fig. 2 | Série da produtividade (média ponderada e percentil 90) com a tendência | 02 |
| Fig. 3 | PP e PA por data de semeadura | 04 |
| Fig. 4 | Superfície do erro e dispersão da validação | 06 |
| Fig. 5 | Mapas das parcelas do yield gap (kg/ha e % do total) | 07 e 09 |
| Fig. 6 | Barras empilhadas da partição por ano | 07 |
| Fig. 7 | DSSAT × MZA | 08 |
| Tab. 1 | Municípios: coordenadas, altitude, CAD, área média | 09 |
| Tab. 2 | ky: tabelado, estratégias A e B, emergente | 06 e 08 |
| Tab. 3 | Partição do yield gap por município | 09 |

Se a revista pedir mudanças (fonte, cores, tamanho), altere a célula da figura no notebook de origem e rode de novo.

---

## Etapa 10. Escrita do artigo

O artigo é escrito ao longo das etapas: cada uma indica o trecho que dela nasce. Esta etapa junta, revisa e fecha o texto. Escreva num Google Docs compartilhado com o orientador, com as citações pelo plugin do Zotero. Muito do texto vem do projeto (Etapa 0): a Introdução e o Material e Métodos passam do futuro para o passado ("foram utilizados").

### Regras de estilo

As mesmas da Etapa 0, mais estas: números com unidade e precisão coerente (kg ha⁻¹ sem casas decimais, ky com duas casas, percentuais com uma).

### Roteiro por seção

**Título.** Específico, com o recorte geográfico e o método, sem dois-pontos.

**Resumo e abstract.** Entre 150 e 200 palavras cada: contexto em uma frase, objetivo, dados e métodos, os principais números (ky da floração calibrado, % inevitável, % data, % manejo, tendência do gap de manejo) e uma frase de conclusão. De três a cinco palavras-chave, em minúsculas, separadas por ponto e vírgula.

**Introdução.** O funil do projeto, encurtado para quatro ou cinco parágrafos, terminando com "Neste sentido, o objetivo deste trabalho foi...".

**Material e Métodos.**

1. Área de estudo, com mapa (Fig. 1) e clima por Köppen (ALVARES et al., 2013);
2. Dados meteorológicos, de solo e de produtividade;
3. Modelo da Zona Agroecológica da FAO (equações da fenologia, do balanço hídrico, da PP e da PA);
4. Verificação da produtividade potencial (o fator e o índice de colheita);
5. Calibração do ky (as duas estratégias, a normalização, a grade, o otimizador e a validação);
6. Partição do yield gap (as equações das parcelas, o nível da PA e o gap explorável);
7. DSSAT CERES-Maize, se houver a Etapa 8;
8. Análise estatística (RMSE, MBE, d, NSE, KGE, Mann-Kendall e Sen), com a tabela das faixas de classificação e suas fontes (WILLMOTT, 1981; MORIASI et al., 2007).

**Resultados e Discussão.** Integrados, na ordem das etapas: PP e sua verificação → ky calibrado → validação → partição (média, anos, mapas) → tendência do gap de manejo → DSSAT. Em cada parágrafo:

1. **o resultado, com números** (médias, desvios, máximos, mínimos, proporções);
2. **a explicação** (o mecanismo agronômico, por exemplo, por que a semeadura de janeiro escapa do déficit de abril);
3. **a comparação com outros autores** (da Silva et al., 2019; Andrea et al., 2018; Sentelhas et al., 2015; Soares et al., 2025; GYGA), com concordâncias e discordâncias.

**Conclusões.** Um item curto por objetivo específico, sem abrir nova discussão.

**Agradecimentos.** UTFPR, Fundação Araucária ou CNPq e, se for o caso, CAPES.

**Disponibilidade de dados.** O repositório no GitHub, com os notebooks que reproduzem todas as figuras.

---

## Pontos de decisão com o orientador

| Após a etapa | Decisão | Onde fica registrada |
|---|---|---|
| 0 | Projeto aprovado | Google Docs |
| 5 | Fator da PP (índice de colheita equivalente) | `parametros.json` |
| 6 | Estratégia principal de calibração (A ou B) | `ky_calibrado.json` |
| 7 | Nível da PA (absoluto ou normalizado) | célula `NIVEL` do notebook 07 |
| 7 | Entra a Etapa 8 ou se passa direto às figuras | |
| 8 | Coeficientes da cultivar e teste de `Z_MAX` | notebook 08 |
| 9 | Periódico de destino e idioma | |

## Riscos e o que fazer

| Risco | Como lidar |
|---|---|
| PP abaixo do IBGE em muitos anos | ajustar o fator da PP na Etapa 5, com a justificativa do índice de colheita |
| ky no limite inferior | conferir a normalização do lado simulado (Etapa 6); calibrar menos fases |
| Superfície do erro plana (várias soluções) | reportar a faixa da validação como incerteza do ky; fixar mais fases |
| PR acima da PA em muitos casos | discutir o nível da PA (Etapa 7) e testar raízes mais profundas (`Z_MAX`) |
| DSSAT sem tempo para calibrar a cultivar | encerrar na Etapa 7; DSSAT vira trabalho futuro na discussão |
| Colab desconecta no meio da simulação | rodar de novo: os municípios prontos ficam no Drive e são pulados |

## Referências de base

Na biblioteca Zotero do orientador, salvo indicação.

- AFFHOLDER, F. et al. *Field Crops Research*, 2013.
- ALLEN, R. G. et al. *Crop evapotranspiration*. FAO Irrigation and Drainage Paper 56, 1998.
- ALVARES, C. A. et al. Köppen's climate classification map for Brazil. *Meteorologische Zeitschrift*, 2013.
- ANDREA, M. C. S. et al. *Agricultural Systems*, 2018.
- BATTISTI, R. et al. 2013; 2018.
- DA SILVA, [completar]. ky do milho segunda safra em Dourados, MS, 2019.
- DJAMAN, K. et al. 2013.
- DOORENBOS, J.; KASSAM, A. H. *Yield response to water*. FAO Irrigation and Drainage Paper 33, 1979.
- GRASSINI, P. et al. *Field Crops Research*, 2015.
- MORIASI, D. N. et al. *Transactions of the ASABE*, 2007. [incluir no Zotero]
- NÓIA JÚNIOR, R. S. et al. 2020.
- SAXTON, K. E.; RAWLS, W. J. *Soil Science Society of America Journal*, 2006 (propriedades hídricas do solo no DSSAT). [incluir no Zotero]
- SENTELHAS, P. C. et al. *The Journal of Agricultural Science*, 2015.
- SOARES, [completar] et al. Assessing environmental and management factors that drive soybean yield gaps in Brazil, 2025.
- VAN ITTERSUM, M. K. et al. *Field Crops Research*, 2013.
- WILLMOTT, C. J. On the validation of models. *Physical Geography*, 1981.
- XAVIER, A. C. et al. New improved Brazilian daily weather gridded data (1961–2020). *International Journal of Climatology*, 2022.
