# milho_oeste

Partição do yield gap do milho segunda safra no Oeste do Paraná com coeficiente ky calibrado.

Trabalho de conclusão de curso de Agronomia, UTFPR Campus Santa Helena. Orientador: Prof. Dr. Fabrício Correia de Oliveira.

O roteiro completo, da escrita do projeto ao artigo, está em [planejamento.md](planejamento.md). As análises rodam no Google Colab: cada notebook tem um botão "Open in Colab" e começa com uma célula que instala as bibliotecas, copia este repositório e conecta o Google Drive.

| Etapa | Notebook |
|---|---|
| 1. Python básico | [01_python_basico](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/01_python_basico.ipynb) |
| 2. Dados de produtividade e clima | [02_dados_ibge_clima](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/02_dados_ibge_clima.ipynb) |
| 3. O MZA-FAO em um ciclo | [03_mza_um_ciclo](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/03_mza_um_ciclo.ipynb) |
| 4. Simulação dos 50 municípios | [04_simulacao_oeste](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/04_simulacao_oeste.ipynb) |
| 5. Verificação da produtividade potencial | [05_verificacao_pp](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/05_verificacao_pp.ipynb) |
| 6. Calibração e validação do ky | [06_calibracao_ky](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/06_calibracao_ky.ipynb) |
| 7. Partição do yield gap | [07_yield_gap](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/07_yield_gap.ipynb) |
| 8. DSSAT CERES-Maize e ky emergente | [08_dssat_ky_emergente](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/08_dssat_ky_emergente.ipynb) |
| 9. Figuras e tabelas do artigo | [09_figuras_artigo](https://colab.research.google.com/github/fcoliveira-utfpr/milho_oeste/blob/main/notebooks/09_figuras_artigo.ipynb) |

**Dados** (`dados/`): clima diário de Xavier et al. (BR-DWGD) nas sedes dos 50 municípios (1998–2025), produtividade municipal do IBGE/PAM (2003–2025), solo do MapBiomas Solo e malha municipal do IBGE.

**Funções** (`src/`): `mza_oeste.py` (MZA-FAO com a biblioteca [agrometeorologiapy](https://pypi.org/project/agrometeorologiapy/)), `avaliacao.py` (índices estatísticos) e `dssat_oeste.py` (DSSAT CERES-Maize via DSSATTools).
