# milho_oeste

**Partição do yield gap do milho segunda safra no Oeste do Paraná com coeficiente ky calibrado**

Trabalho de conclusão de curso de Agronomia, UTFPR Campus Santa Helena.
Orientador: Prof. Dr. Fabrício Correia de Oliveira.

---

## A pesquisa em poucas linhas

O milho segunda safra (safrinha) do Oeste do Paraná colhe bem menos do que poderia. Esta pesquisa quantifica
essa diferença, o **yield gap**, e a divide em três parcelas:

```
PP  produtividade potencial   (radiação + temperatura, sem falta de água)
PA  produtividade atingível   (PP penalizada pelo déficit hídrico de cada fase, via coeficiente ky)
PR  produtividade real        (IBGE, Produção Agrícola Municipal)

yield gap total = PP − PR = déficit hídrico inevitável + data de semeadura + manejo
```

A PP e a PA vêm do **Modelo da Zona Agroecológica da FAO** (MZA-FAO), rodado dia a dia em 50 municípios, 27 anos
e 9 datas de semeadura. O coeficiente **ky**, que diz o quanto a produtividade cai com a falta de água em cada
fase, é **calibrado** com os dados do IBGE, sem deixar que ele absorva o efeito do manejo. O **DSSAT
CERES-Maize**, um modelo de processo, serve de segunda opinião.

O roteiro completo, da escrita do projeto ao artigo, está em **[planejamento.md](planejamento.md)**.

---

## Por onde começar

1. Leia o [planejamento.md](planejamento.md), principalmente "A pesquisa em uma página" e a Etapa 0.
2. Escreva o projeto (Etapa 0) no Google Docs indicado no planejamento.
3. Abra o notebook 01 pelo botão do Colab (tabela abaixo), faça **Arquivo → Salvar uma cópia no Drive** e siga
   os notebooks em ordem. Cada um depende dos resultados do anterior.

---

## Estrutura dos arquivos

```
milho_oeste/
├── README.md                         este arquivo
├── planejamento.md                   roteiro do trabalho: etapas, código explicado, o que entregar e escrever
│
├── dados/                            dados de entrada, já recortados para os 50 municípios do Oeste do Paraná
│   ├── municipios_oeste.csv          código IBGE, nome, latitude, longitude, altitude, CAD do solo (mm/m),
│   │                                 argila e areia (%) das áreas de lavoura
│   ├── ibge_pam_milho_oeste.csv      área plantada e colhida (ha), produção (t) e produtividade (kg/ha) do milho,
│   │                                 1ª e 2ª safra (coluna `safra`), 2003 a 2025 (IBGE/PAM)
│   ├── clima_oeste.parquet           clima diário na sede de cada município, 1998 a 2025 (Xavier et al., BR-DWGD):
│   │                                 chuva `pr` (mm), `Tmax` e `Tmin` (°C), umidade `RH` (%), radiação `Rs`
│   │                                 (MJ m⁻² dia⁻¹), vento `u2` (m/s) e ETo `ET` (mm/dia)
│   ├── solo_camadas_oeste.csv        argila e areia em camadas de 10 cm (MapBiomas Solo), usadas no DSSAT
│   └── malha_municipios_oeste.geojson limites municipais, para os mapas
│
├── src/                              funções do projeto, importadas pelos notebooks
│   ├── mza_oeste.py                  MZA-FAO: fenologia por graus-dia, Kc, raízes, balanço hídrico, PP e PA de um
│   │                                 ciclo (`simular`), laço por município (`simular_municipio`) e eficiência
│   │                                 climática para a calibração (`ec`, `preparar_janela`, `ec_janela`)
│   ├── avaliacao.py                  índices estatísticos: MBE, RMSE, r, d de Willmott, NSE e KGE (`avaliar`)
│   └── dssat_oeste.py                DSSAT CERES-Maize: arquivos de clima e solo, cultivar com coeficientes
│                                     ajustáveis e simulação em sequeiro e irrigado (`simular`)
│
└── notebooks/                        uma etapa por notebook, comentados para quem está aprendendo Python
    ├── 01_python_basico.ipynb
    ├── ...
    └── 09_figuras_artigo.ipynb
```

---

## Notebooks

| Etapa | Notebook | O que faz | Grava no Drive |
|---|---|---|---|
| 1 | [01_python_basico](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/01_python_basico.ipynb) | Python básico com exemplos de agrometeorologia; ETo por Penman-Monteith | |
| 2 | [02_dados_ibge_clima](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/02_dados_ibge_clima.ipynb) | Série de produtividade, tendência tecnológica, anos de quebra, clima da safrinha | figura da série |
| 3 | [03_mza_um_ciclo](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/03_mza_um_ciclo.ipynb) | Um ciclo do MZA-FAO passo a passo; a equação do ky na mão | |
| 4 | [04_simulacao_oeste](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/04_simulacao_oeste.ipynb) | 50 municípios × 27 anos × 9 datas de semeadura (≈ 7 min) | `simulacao_mza_oeste.parquet` |
| 5 | [05_verificacao_pp](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/05_verificacao_pp.ipynb) | PP × IBGE, IDR e GYGA; fator de ajuste da PP | `parametros.json` |
| 6 | [06_calibracao_ky](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/06_calibracao_ky.ipynb) | Calibração do ky (busca em grade e otimizador) e validação deixando um ano de fora (≈ 3 min) | `ky_calibrado.json` |
| 7 | [07_yield_gap](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/07_yield_gap.ipynb) | PA com o ky calibrado, partição do yield gap, tendência e mapas | `yield_gap.parquet` |
| 8 | [08_dssat_ky_emergente](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/08_dssat_ky_emergente.ipynb) | DSSAT irrigado × sequeiro em 5 municípios; ky emergente | `dssat_oeste.parquet` |
| 9 | [09_figuras_artigo](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/09_figuras_artigo.ipynb) | Figuras e tabelas finais em 300 dpi | `figuras_artigo/` |

Cada notebook é organizado em seções numeradas, com uma explicação antes de cada bloco de código, comentários
linha a linha, exercícios no final e a indicação do que escrever no artigo.

---

## Como os notebooks rodam no Colab

A primeira célula de todo notebook (**célula 0**) prepara o ambiente. Rode-a sempre primeiro:

1. **instala** as bibliotecas que o Colab não tem (`agrometeorologiapy`; `DSSATTools` no notebook 08);
2. **copia este repositório** para a máquina do Colab com `git clone` (dados + funções);
3. **conecta o Google Drive** e cria a pasta `MyDrive/milho_oeste/resultados`.

O Colab apaga tudo quando a sessão fecha. Por isso cada etapa grava os resultados no Drive, e a etapa seguinte lê
de lá. Fora do Colab, a mesma célula usa a pasta `resultados/` local (ignorada pelo git).

Para rodar no próprio computador: Python 3.11 ou mais novo e
`pip install agrometeorologiapy==1.0.1 pandas pyarrow statsmodels scipy matplotlib geopandas pymannkendall`
(e `DSSATTools==3.0.2` para o notebook 08).

---

## Fontes dos dados

- **Clima:** Xavier, A. C. et al. New improved Brazilian daily weather gridded data (1961–2020). *International
  Journal of Climatology*, 2022.
- **Produtividade:** IBGE, Produção Agrícola Municipal (PAM), tabela 839 (milho, 1ª e 2ª safra).
- **Solo:** MapBiomas Solo (textura e capacidade de água disponível sobre as áreas de lavoura).
- **Malha municipal:** IBGE.

Os dados foram preparados no projeto [ML_maize_pr](https://github.com/fcoliveira-utfpr/ML_maize_pr). O MZA-FAO
usa a biblioteca [agrometeorologiapy](https://pypi.org/project/agrometeorologiapy/).
