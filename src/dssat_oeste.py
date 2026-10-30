"""DSSAT CSM-CERES-Maize (via `DSSATTools`) para o milho segunda safra do Oeste do Paraná.

Roda as safras de um município em duas condições: sequeiro e irrigado (irrigação automática).
A razão sequeiro/irrigado é a perda pelo déficit hídrico segundo um modelo de processo, que
serve de referência para o "ky emergente" (notebook 08). Adaptado do projeto ML_maize_pr.

No Colab (Linux), o DSSATTools já traz o executável do DSSAT. No macOS, usa-se o DSSAT
compilado do código aberto, se existir em ~/Python/dssat-csm-os.
"""
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# O DSSAT (Fortran) aceita caminhos de até 80 caracteres. Cada processo usa uma pasta curta própria,
# criada antes de importar o DSSATTools (que monta a pasta do DSSAT dentro dela).
_RAIZ_TMP = Path.home() / ".dssat_tmp"
_RAIZ_TMP.mkdir(exist_ok=True)
tempfile.tempdir = tempfile.mkdtemp(prefix="d", dir=_RAIZ_TMP)

import DSSATTools.run as dssat_run  # noqa: E402
from DSSATTools.crop import Maize  # noqa: E402
from DSSATTools.filex import (AMIrrigation, Fertilizer, FertilizerEvent, Field, InitialConditions,  # noqa: E402
                              InitialConditionsLayer, Planting, SCGeneral, SCManagement, SCMethods,
                              SCOptions, SCOutputs, SimulationControls)
from DSSATTools.run import DSSAT  # noqa: E402
from DSSATTools.soil import SoilLayer, SoilProfile  # noqa: E402
from DSSATTools.weather import WeatherStation  # noqa: E402

if sys.platform == "darwin":
    _BIN = Path.home() / "Python" / "dssat-csm-os" / "build" / "bin" / "dscsm048"
    if _BIN.exists():
        dssat_run.BIN_PATH = str(_BIN)

CULTIVAR_BASE = "990003"      # cultivar genérica de ciclo curto do DSSAT (MZCER048.CUL)
POPULACAO = 6.0               # plantas m-2
ADUBO_N = 200                 # kg N ha-1 na semeadura (N não limitante: o foco é o clima)
FRACAO_AD_INICIAL = 0.7       # fração da água disponível no solo 30 dias antes da semeadura

# perfil do solo: espessura das camadas (mm) e camadas de 10 cm do MapBiomas Solo dentro de cada uma
ESPESSURA = [150, 150, 300, 300, 300, 300, 300]
MB_CAMADAS = [[1], [2], [3, 4, 5], [6, 7, 8], [9, 10], [10], [10]]
MATERIA_ORGANICA = [2.5, 2.0, 1.5, 1.0, 0.8, 0.6, 0.5]  # % (perfil típico de Latossolo cultivado)
BASES_CM = np.cumsum(ESPESSURA) / 10                       # 15, 30, 60, ..., 180 cm


def saxton_rawls(areia, argila, mo):
    """θ1500, θ33 e θs (m3 m-3) e Ks (mm/dia) por Saxton & Rawls (2006); areia e argila em fração."""
    S, C, OM = areia, argila, mo
    t1500t = -0.024 * S + 0.487 * C + 0.006 * OM + 0.005 * S * OM - 0.013 * C * OM + 0.068 * S * C + 0.031
    t1500 = t1500t + (0.14 * t1500t - 0.02)
    t33t = -0.251 * S + 0.195 * C + 0.011 * OM + 0.006 * S * OM - 0.027 * C * OM + 0.452 * S * C + 0.299
    t33 = t33t + (1.283 * t33t ** 2 - 0.374 * t33t - 0.015)
    ts33t = 0.278 * S + 0.034 * C + 0.022 * OM - 0.018 * S * OM - 0.027 * C * OM - 0.584 * S * C + 0.078
    ts33 = ts33t + (0.636 * ts33t - 0.107)
    ts = t33 + ts33 - 0.097 * S + 0.043
    lam = (np.log(t33) - np.log(t1500)) / (np.log(1500) - np.log(33))
    ks = 1930 * (ts - t33) ** (3 - lam) * 24
    return t1500, t33, ts, ks


def perfil(camadas_mun, dta_mm_m):
    """Perfil físico de 7 camadas; a água disponível (DUL − LL15) é ajustada à CAD do município."""
    g = camadas_mun.set_index("camada")
    areia = np.array([g.loc[c, "areia_pct"].mean() for c in MB_CAMADAS]) / 100
    argila = np.array([g.loc[c, "argila_pct"].mean() for c in MB_CAMADAS]) / 100
    ll15, dul, sat, ks = saxton_rawls(areia, argila, np.array(MATERIA_ORGANICA))
    fator = (dta_mm_m / 1000) / np.average(dul - ll15, weights=ESPESSURA)
    dul = ll15 + (dul - ll15) * fator
    sat = np.maximum(sat, dul + 0.03)
    return {"LL15": ll15, "DUL": dul, "SAT": sat, "BD": (1 - sat) * 2.65, "KS": ks,
            "argila": argila * 100, "areia": areia * 100}


def estacao(clima_mun, mun, insi="PRMZ"):
    """Arquivo de clima do DSSAT a partir do clima diário de Xavier et al."""
    c = clima_mun.reset_index().sort_values("data")
    tmed = (c["Tmax"] + c["Tmin"]) / 2
    es = 0.6108 * np.exp(17.27 * tmed / (tmed + 237.3))
    ea = (c["RH"] / 100 * es).clip(lower=0.05)
    orvalho = (237.3 * np.log(ea / 0.6108)) / (17.27 - np.log(ea / 0.6108))
    tab = pd.DataFrame({"date": pd.to_datetime(c["data"]), "srad": c["Rs"].round(1), "tmax": c["Tmax"].round(1),
                        "tmin": c["Tmin"].round(1), "rain": c["pr"].clip(lower=0).round(1),
                        "dewp": np.minimum(orvalho, c["Tmin"] + 2).round(1), "wind": (c["u2"] * 86.4).round(0)})
    mensal = tmed.groupby(pd.to_datetime(c["data"]).dt.month).mean()
    return WeatherStation(table=tab, lat=round(mun["latitude"], 3), long=round(mun["longitude"], 3), insi=insi,
                          elev=round(mun["altitude_m"]), tav=round(tmed.mean(), 1),
                          amp=round(mensal.max() - mensal.min(), 1), refht=2.0, wndht=2.0)


def solo(p, mun):
    """Perfil de solo do DSSAT a partir do perfil físico (`perfil`)."""
    topo = np.r_[0, BASES_CM[:-1]]
    camadas = [SoilLayer(slb=float(b), slll=round(float(ll), 3), sdul=round(float(du), 3), ssat=round(float(sa), 3),
                         sbdm=round(float(bd), 2), sloc=round(mo / 1.724, 2), slcl=round(float(ar), 1),
                         slsi=round(float(max(100 - ar - ae, 0)), 1), slhw=5.5,
                         srgf=1.0 if b <= 15 else round(float(np.exp(-0.02 * (t + b) / 2)), 3),
                         slni=round(mo / 1.724 / 12, 3), ssks=round(float(ks) / 10 / 24, 2))
               for b, t, ll, du, sa, bd, ks, mo, ar, ae in zip(BASES_CM, topo, p["LL15"], p["DUL"], p["SAT"], p["BD"],
                                                                 p["KS"], MATERIA_ORGANICA, p["argila"], p["areia"])]
    return SoilProfile(table=camadas, name="PRMZ000001", soil_data_source="MapBiomas", soil_clasification="C",
                       soil_series_name="Perfil municipal", site="PR", country="Brazil",
                       lat=round(mun["latitude"], 3), long=round(mun["longitude"], 3), scom="R", salb=0.13,
                       slu1=6.0, sldr=0.60, slro=73, slnf=1.0, slpf=1.0)


def cultivar(coeficientes=None):
    """Cultivar genérica com os coeficientes genéticos alterados (dicionário, ex.: {"P1": 200, "G2": 750})."""
    c = Maize(CULTIVAR_BASE)
    for k, v in (coeficientes or {}).items():
        c[k] = v
    return c


def _ler_summary(txt):
    linhas = txt.splitlines()
    i = next(k for k, l in enumerate(linhas) if l.startswith("@"))
    cab = linhas[i].replace("@", " ").split()
    dados = [l.split() for l in linhas[i + 1:] if l.strip()]
    df = pd.DataFrame([d for d in dados if len(d) == len(cab)], columns=cab)
    num = df.apply(pd.to_numeric, errors="coerce")
    return num.where(num.notna(), df).replace(-99, np.nan).copy()


def _data_juliana(s):
    return pd.to_datetime(s.astype("Int64").astype(str), format="%Y%j", errors="coerce")


def simular(clima_mun, camadas_mun, mun, datas, irrigado, coeficientes=None, ano_ini=1999, n_anos=27):
    """Safras de `ano_ini` a `ano_ini + n_anos − 1` para cada data de semeadura (mês, dia).

    Devolve uma tabela com a produtividade de grãos (kg/ha, 13% de umidade), os dias até a antese
    (florescimento) e até a maturação.
    """
    p = perfil(camadas_mun, mun["dta_mm_m"])
    campo = Field(id_field="PRMZ0001", wsta=estacao(clima_mun, mun), id_soil=solo(p, mun), flob=0, fldt="DR000",
                  fldd=0, flds=0, sltx="C", sldp=180)
    linhas = []
    with tempfile.TemporaryDirectory(prefix="r") as pasta:
        env = DSSAT(pasta)
        for mes, dia in datas:
            semeadura = date(ano_ini, mes, dia)
            inicio = semeadura - timedelta(days=30)
            agua = p["LL15"] + FRACAO_AD_INICIAL * (p["DUL"] - p["LL15"])
            ic = InitialConditions(pcr="SB", icdat=inicio, icres=3000, icren=0.8, icrip=0, icrid=0, icrn=1, icre=1,
                                   table=[InitialConditionsLayer(icbl=float(b), sh2o=round(float(w), 3), snh4=0.5,
                                                                 sno3=2.0) for b, w in zip(BASES_CM, agua)])
            ctrl = SimulationControls(
                general=SCGeneral(sdate=inicio, nyers=n_anos),
                options=SCOptions(water="Y", nitro="Y", symbi="N"),
                methods=SCMethods(evapo="F"),
                management=SCManagement(irrig="A" if irrigado else "N", ferti="R", harvs="M"),
                outputs=SCOutputs(grout="N", waout="N", caout="N"),
                irrigation=AMIrrigation(imdep=30, ithrl=50, ithru=100) if irrigado else None)
            adubo = Fertilizer(table=[FertilizerEvent(fdate=semeadura, fmcd="FE005", facd="AP002", fdep=5,
                                                      famn=ADUBO_N)])
            try:
                env.run_treatment(field=campo, cultivar=cultivar(coeficientes),
                                  planting=Planting(pdate=semeadura, ppop=POPULACAO, ppoe=POPULACAO, plrs=50, pldp=5),
                                  initial_conditions=ic, fertilizer=adubo, simulation_controls=ctrl, verbose=False)
            except ValueError:
                pass  # com pandas 3 o DSSATTools falha ao ler a saída; o Summary.OUT é lido abaixo
            s = _ler_summary((Path(pasta) / "Summary.OUT").read_text(errors="ignore"))
            s = s.copy().assign(pdat=_data_juliana(s["PDAT"]), adat=_data_juliana(s["ADAT"]), mdat=_data_juliana(s["MDAT"]))
            for _, r in s.dropna(subset=["pdat"]).iterrows():
                linhas.append({"cod_ibge": mun["cod_ibge"], "ano": r["pdat"].year, "semeadura": f"{dia:02d}/{mes:02d}",
                               "rend": r["HWAM"],
                               "dias_antese": (r["adat"] - r["pdat"]).days if pd.notna(r["adat"]) else np.nan,
                               "dias_maturacao": (r["mdat"] - r["pdat"]).days if pd.notna(r["mdat"]) else np.nan,
                               "irrigacao_mm": r.get("IRCM", np.nan)})
    return pd.DataFrame(linhas)
