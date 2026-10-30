"""Índices estatísticos para comparar valores observados (obs) e simulados (sim).

Escritos de forma direta, uma linha por equação, para que possam ser lidos ao lado das
equações do artigo.
"""
import numpy as np
import pandas as pd


def _arrays(obs, sim):
    obs, sim = np.asarray(obs, dtype=float), np.asarray(sim, dtype=float)
    ok = ~(np.isnan(obs) | np.isnan(sim))          # ignora pares com valor faltante
    return obs[ok], sim[ok]


def mbe(obs, sim):
    """Erro médio (viés): positivo = o modelo superestima."""
    obs, sim = _arrays(obs, sim)
    return np.mean(sim - obs)


def rmse(obs, sim):
    """Raiz do erro quadrático médio, na unidade dos dados."""
    obs, sim = _arrays(obs, sim)
    return np.sqrt(np.mean((sim - obs) ** 2))


def r_pearson(obs, sim):
    """Coeficiente de correlação de Pearson."""
    obs, sim = _arrays(obs, sim)
    return np.corrcoef(obs, sim)[0, 1]


def d_willmott(obs, sim):
    """Índice de concordância de Willmott (1981), de 0 a 1."""
    obs, sim = _arrays(obs, sim)
    om = obs.mean()
    return 1 - np.sum((sim - obs) ** 2) / np.sum((np.abs(sim - om) + np.abs(obs - om)) ** 2)


def nse(obs, sim):
    """Eficiência de Nash-Sutcliffe: 1 = perfeito; 0 = tão bom quanto a média observada."""
    obs, sim = _arrays(obs, sim)
    return 1 - np.sum((sim - obs) ** 2) / np.sum((obs - obs.mean()) ** 2)


def kge(obs, sim):
    """Eficiência de Kling-Gupta (2009): combina correlação, variabilidade e viés."""
    obs, sim = _arrays(obs, sim)
    r = np.corrcoef(obs, sim)[0, 1]
    alfa = sim.std() / obs.std()
    beta = sim.mean() / obs.mean()
    return 1 - np.sqrt((r - 1) ** 2 + (alfa - 1) ** 2 + (beta - 1) ** 2)


def avaliar(obs, sim):
    """Todos os índices de uma vez, como uma linha de tabela."""
    return pd.Series({"n": len(_arrays(obs, sim)[0]), "MBE": mbe(obs, sim), "RMSE": rmse(obs, sim),
                      "r": r_pearson(obs, sim), "d": d_willmott(obs, sim), "NSE": nse(obs, sim),
                      "KGE": kge(obs, sim)})
