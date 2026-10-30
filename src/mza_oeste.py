"""Simulação do milho segunda safra pelo Modelo da Zona Agroecológica da FAO (MZA-FAO).

Uma simulação = (município, ano, data de semeadura), em escala diária, com o clima de Xavier et al.
O balanço hídrico da cultura, a produtividade potencial (PPf) e a atingível (PA) vêm da biblioteca
agrometeorologiapy; aqui ficam só a fenologia por graus-dia, as curvas de Kc e de profundidade
das raízes e os indicadores por fase. Adaptado do projeto ML_maize_pr.
"""
import numpy as np
import pandas as pd
from agrometeorologiapy import (
    angulo_horario_nascer,
    balanco_hidrico_cultura,
    declinacao_solar,
    fator_correcao_distancia,
    irradiancia_extraterrestre,
)
from agrometeorologiapy.produtividade import produtividade_atingivel, produtividade_potencial

# ---------------------------------------------------------------- parâmetros da cultura
TB = 10.0                 # temperatura-base (°C)
CT = 1450.0               # soma térmica da semeadura à maturação fisiológica (°C dia)

# fases do Kc (FAO 56) como frações da soma térmica: inicial, desenvolvimento, intermediária, final
FASES_KC = (0.17, 0.28, 0.33, 0.22)
KC_INI, KC_MED, KC_FIN = 0.3, 1.2, 0.6

# fases do ky de Doorenbos & Kassam (1979), como frações da soma térmica
FASES_KY = {"estabelecimento": 0.15, "vegetativo": 0.30, "floracao": 0.12,
            "enchimento": 0.30, "maturacao": 0.13}
FASES = list(FASES_KY)
KY_DK = {"estabelecimento": 0.4, "vegetativo": 0.4, "floracao": 1.5, "enchimento": 0.5, "maturacao": 0.2}

Z_INI, Z_MAX = 0.10, 0.40  # profundidade efetiva das raízes (m): cresce até o fim do vegetativo
IAF, CC, UMIDADE = 5.0, 0.40, 13.0
SPINUP = 30                # dias de balanço hídrico antes da semeadura (solo com palha, Kc inicial)
JANELA_MAX = 300           # dias após a semeadura; sem atingir a CT, o ciclo fica incompleto

ANOS = range(1999, 2026)
DATAS = [(m, d) for m in (1, 2, 3) for d in (5, 15, 25)]   # (mês, dia) das 9 semeaduras
JANELA = ["15/01", "05/02", "25/02", "15/03"]               # datas que representam o produtor


def graus_dia(tmax, tmin, tb=TB):
    """Mesma regra de `agrometeorologiapy.data_maturacao_fisiologica`."""
    tmed = (tmax + tmin) / 2
    amp = np.maximum(tmax - tmin, 0.1)
    return np.where(tb < tmin, tmed - tb, np.where(tmax > tb, (tmax - tb) ** 2 / (2 * amp), 0.0))


def qo_diaria(lat, datas):
    """Irradiância extraterrestre diária (MJ m-2 dia-1)."""
    nda = datas.day_of_year.to_numpy()
    dec = declinacao_solar(nda)
    return irradiancia_extraterrestre(lat, dec, angulo_horario_nascer(lat, dec), fator_correcao_distancia(nda))


def _fase(frac_acum, limites):
    """Índice da fase de cada dia a partir da fração acumulada da soma térmica."""
    return np.minimum(np.searchsorted(np.cumsum(limites), frac_acum, side="right"), len(limites) - 1)


def _kc(frac):
    a, b, c, _ = np.cumsum(FASES_KC)
    return np.select(
        [frac < a, frac < b, frac < c],
        [KC_INI, KC_INI + (KC_MED - KC_INI) * (frac - a) / (b - a), KC_MED],
        KC_MED + (KC_FIN - KC_MED) * np.clip((frac - c) / (1 - c), 0, 1),
    )


def simular(clima_mun, lat, dta, semeadura, ky=KY_DK, ct=CT, diario=False):
    """Simula um ciclo.

    clima_mun : clima diário de um município, indexado pela data
    lat       : latitude (graus decimais, negativa no hemisfério sul)
    dta       : água disponível no solo (mm por metro de profundidade)
    semeadura : data de semeadura ("2020-02-05" ou pd.Timestamp)
    diario    : se True, devolve também a tabela diária do ciclo (para gráficos)
    """
    semeadura = pd.Timestamp(semeadura)
    janela = clima_mun.loc[semeadura - pd.Timedelta(days=SPINUP): semeadura + pd.Timedelta(days=JANELA_MAX)]
    pos = janela.index >= semeadura
    campo = janela.loc[pos]

    gd = graus_dia(campo["Tmax"].to_numpy(), campo["Tmin"].to_numpy())
    acum = np.cumsum(gd)
    completo = bool(acum[-1] >= ct)
    ciclo = int(np.searchsorted(acum, ct) + 1) if completo else len(campo)
    campo = campo.iloc[:ciclo].copy()
    frac = np.minimum(acum[:ciclo] / ct, 1.0)

    campo["fase_ky"] = np.array(FASES)[_fase(frac, list(FASES_KY.values()))]
    frac_fim_veg = FASES_KY["estabelecimento"] + FASES_KY["vegetativo"]
    z = Z_INI + (Z_MAX - Z_INI) * np.clip(frac / frac_fim_veg, 0, 1)

    # ---- balanço hídrico da cultura (aquecimento com Kc e raiz iniciais antes da semeadura)
    pre = janela.loc[~pos]
    bh_in = pd.DataFrame({
        "Chuva": np.r_[pre["pr"].to_numpy(), campo["pr"].to_numpy()],
        "ETc": np.r_[KC_INI * pre["ET"].to_numpy(), _kc(frac) * campo["ET"].to_numpy()],
        "CAD": np.r_[np.full(len(pre), Z_INI * dta), z * dta],
    })
    bh = balanco_hidrico_cultura(bh_in).iloc[len(pre):].reset_index(drop=True)
    for col in ["ETc", "ETR", "DEF", "EXC", "ARM"]:
        campo[col] = bh[col].to_numpy()

    # ---- produtividade potencial e atingível
    pp_in = pd.DataFrame({"data": campo.index, "Tmed": ((campo["Tmax"] + campo["Tmin"]) / 2).to_numpy(),
                          "Qg": campo["Rs"].to_numpy(), "Qo": qo_diaria(lat, campo.index)})
    ppf = produtividade_potencial(pp_in, lat=lat, rota="C4", IAF=IAF, Cc=CC, U=UMIDADE, intervalo="d").attrs["PPf"]
    pa = produtividade_atingivel(ppf, campo["ETR"].to_numpy(), campo["ETc"].to_numpy(),
                                 ky=ky, fase=campo["fase_ky"].to_numpy())

    # ---- indicadores por fase de Doorenbos & Kassam
    floracao = campo.index[campo["fase_ky"] == "floracao"]
    saida = {"ciclo_dias": ciclo, "ciclo_incompleto": not completo,
             "data_floracao": floracao[0] if len(floracao) else pd.NaT,
             "data_maturacao": campo.index[-1], "PPf": ppf, "PA": pa.attrs["PA"] if completo else 0.0}
    for nome, g in campo.groupby("fase_ky", sort=False):
        etc = g["ETc"].sum()
        saida.update({
            f"ISNA_{nome}": g["ETR"].sum() / etc if etc > 0 else 1.0,
            f"chuva_{nome}": g["pr"].sum(),
            f"ETc_{nome}": etc,
            f"ETR_{nome}": g["ETR"].sum(),
            f"DEF_{nome}": g["DEF"].sum(),
            f"Tmed_{nome}": ((g["Tmax"] + g["Tmin"]) / 2).mean(),
            f"Tmax_{nome}": g["Tmax"].mean(),
            f"Tmin_{nome}": g["Tmin"].min(),
            f"geada_{nome}": int((g["Tmin"] <= 2.0).sum()),
            f"calor_{nome}": int((g["Tmax"] >= 35.0).sum()),
        })
    if diario:
        return saida, campo
    return saida


def simular_municipio(clima_mun, cod, lat, dta, anos=ANOS, datas=DATAS, ct=CT):
    """Todas as combinações ano × data de semeadura de um município."""
    linhas = []
    for ano in anos:
        for mes, dia in datas:
            r = simular(clima_mun, lat, dta, pd.Timestamp(ano, mes, dia), ct=ct)
            r.update(cod_ibge=cod, ano=ano, semeadura=f"{dia:02d}/{mes:02d}")
            linhas.append(r)
    return pd.DataFrame(linhas)


def ec(df, ky):
    """Eficiência climática PA/PPf pelo produtório, para um dicionário de ky por fase.

    Usa só o ISNA de cada fase: com a simulação feita uma vez, qualquer ky é testado sem
    refazer o balanço hídrico (é o que torna a calibração rápida).
    """
    fator = 1.0
    for f in FASES:
        fator = fator * (1 - ky[f] * (1 - df[f"ISNA_{f}"])).clip(lower=0)
    return fator


def preparar_janela(sim, datas=JANELA):
    """Organiza as datas da janela de semeadura em matrizes (município-ano × data).

    Devolve um dicionário com o índice (cod_ibge, ano), a PPf e o ISNA de cada fase. Serve
    para calcular depressa a eficiência climática da janela com qualquer ky (`ec_janela`).
    """
    jan = sim[sim["semeadura"].isin(datas)].copy()
    jan["semeadura"] = pd.Categorical(jan["semeadura"], categories=datas)
    tab = jan.pivot_table(index=["cod_ibge", "ano"], columns="semeadura", observed=False,
                          values=["PPf"] + [f"ISNA_{f}" for f in FASES]).dropna()
    return {"indice": tab.index, "PPf": tab["PPf"].to_numpy(),
            **{f: tab[f"ISNA_{f}"].to_numpy() for f in FASES}}


def ec_janela(prep, ky):
    """Eficiência climática da janela: soma da PA das datas dividida pela soma da PPf."""
    fator = np.ones_like(prep["PPf"])
    for f in FASES:
        fator = fator * np.clip(1 - ky[f] * (1 - prep[f]), 0, None)
    return pd.Series((prep["PPf"] * fator).sum(axis=1) / prep["PPf"].sum(axis=1), index=prep["indice"], name="EC")
