# -*- coding: utf-8 -*-
"""
ANALIZADOR AUTOMATIZADO DE OPERACIONES DE CONCENTRACIÓN (FUSIONES)
====================================================================
Herramienta de apoyo académico para el análisis preliminar de operaciones
de concentración horizontal, conforme a la metodología del Índice de
Herfindahl-Hirschman (IHI / HHI) utilizada como estándar de referencia
por la Fiscalía Nacional Económica (FNE) de Chile en su "Guía para el
Análisis de Operaciones de Concentración".

Autor: Herramienta desarrollada con Claude (Anthropic) para fines académicos.
Curso: Derecho Económico II — Pontificia Universidad Católica de Chile.

EJECUCIÓN:
    1. Instalar dependencias:
       pip install streamlit plotly pandas
    2. Ejecutar:
       streamlit run analizador_fusiones.py

DISCLAIMER:
    Esta herramienta tiene fines pedagógicos y de apoyo al análisis
    preliminar. No constituye asesoría legal vinculante ni reemplaza
    el análisis técnico-económico que realiza la FNE en un procedimiento
    real bajo el D.L. 211. Los umbrales numéricos utilizados corresponden
    a los estándares de referencia comparados (FNE / DOJ-FTC Horizontal
    Merger Guidelines) entregados como parámetros de este ejercicio.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="Analizador de Concentración de Mercado | IHI - FNE",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETTE = [
    "#0B2545", "#C9A227", "#13315C", "#1B998B", "#5C677D",
    "#D8973C", "#2E294E", "#8AA29E", "#4F5D75", "#7C90A0",
]
ALERT_COLOR = "#A4243B"   # color reservado para la entidad fusionada (resalte)
GREEN = "#1E7B45"
YELLOW = "#B8860B"
RED = "#A4243B"

# =====================================================================
# ESTILOS CSS — DASHBOARD CORPORATIVO
# =====================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #F4F6F8;
    }

    /* Encabezado principal */
    .app-header {
        background: linear-gradient(135deg, #0B2545 0%, #13315C 100%);
        padding: 2rem 2.2rem;
        border-radius: 14px;
        color: #FFFFFF;
        margin-bottom: 1.6rem;
        box-shadow: 0 8px 24px rgba(11, 37, 69, 0.25);
    }
    .app-header h1 {
        font-weight: 800;
        font-size: 1.9rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .app-header p {
        font-weight: 400;
        font-size: 0.95rem;
        opacity: 0.85;
        margin: 0;
    }
    .app-header .badge {
        display: inline-block;
        background: rgba(201, 162, 39, 0.18);
        color: #C9A227;
        border: 1px solid rgba(201,162,39,0.4);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.7rem;
    }

    /* Tarjetas de sección */
    .section-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 2px 10px rgba(20, 30, 50, 0.06);
        border: 1px solid #E7EAEE;
        margin-bottom: 1.2rem;
    }
    .section-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #0B2545;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Métricas custom */
    .metric-box {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        border: 1px solid #E7EAEE;
        box-shadow: 0 2px 8px rgba(20,30,50,0.05);
        text-align: left;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #5C677D;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0B2545;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #8A93A2;
        margin-top: 2px;
    }

    /* Dictamen */
    .dictamen-box {
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        border-left: 7px solid;
        margin-top: 0.6rem;
        line-height: 1.55;
    }
    .dictamen-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .dictamen-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 20px;
        margin-left: 6px;
        vertical-align: middle;
    }

    .footer-note {
        font-size: 0.78rem;
        color: #8A93A2;
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E7EAEE;
    }

    section[data-testid="stSidebar"] {
        background-color: #0B2545;
    }
    section[data-testid="stSidebar"] * {
        color: #F4F6F8 !important;
    }
    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: #13315C !important;
        color: #FFFFFF !important;
        border: 1px solid #2E4670 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================

def parse_companies(raw_text: str):
    """
    Parsea cadenas del tipo 'Empresa A: 40, Empresa B: 30, Empresa C: 20'
    Retorna (lista_de_tuplas[(nombre, participacion)], lista_de_errores)
    """
    items, errors = [], []
    if not raw_text or not raw_text.strip():
        return items, ["No se ingresaron datos de empresas."]

    chunks = raw_text.split(",")
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" not in chunk:
            errors.append(f"Formato inválido en «{chunk}». Use el formato 'Nombre: Valor'.")
            continue
        name, value = chunk.rsplit(":", 1)
        name = name.strip()
        value = value.strip().replace("%", "").replace(",", ".")
        if not name:
            errors.append(f"Falta el nombre de la empresa en «{chunk}».")
            continue
        try:
            value_f = float(value)
        except ValueError:
            errors.append(f"El valor de participación de «{name}» no es numérico.")
            continue
        if value_f < 0:
            errors.append(f"La participación de «{name}» no puede ser negativa.")
            continue
        items.append((name, value_f))
    return items, errors


def hhi(shares):
    """Calcula el Índice de Herfindahl-Hirschman (escala 0 - 10.000)."""
    return float(sum(s ** 2 for s in shares))


def build_color_map(names):
    return {n: PALETTE[i % len(PALETTE)] for i, n in enumerate(names)}


def make_pie(df, title, color_map, highlight_name=None):
    colors = []
    for n in df["Empresa"]:
        if highlight_name is not None and n == highlight_name:
            colors.append(ALERT_COLOR)
        else:
            colors.append(color_map.get(n, "#9AA5B1"))

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["Empresa"],
                values=df["Participación (%)"],
                hole=0.45,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="label+percent",
                textfont=dict(size=12, family="Inter"),
                sort=False,
            )
        ]
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#0B2545", family="Inter"), x=0.5),
        margin=dict(t=60, b=20, l=10, r=10),
        height=380,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, xanchor="center", x=0.5, font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def metric_box(label, value, sub=""):
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def evaluate_scenario(post_hhi: float, delta_hhi: float):
    """
    Aplica la matriz de decisión sobre umbrales HHI / Delta-HHI
    y retorna un diccionario con la calificación jurídico-económica.
    """
    if post_hhi < 1500:
        return {
            "escenario": "Escenario 1 — Baja Concentración",
            "nivel": "BAJO RIESGO",
            "color": GREEN,
            "bg": "#E9F7EF",
            "fase": "No amerita revisión adicional (Fase de revisión preliminar / Fase I expedita)",
            "texto": (
                "El IHI post-operación se ubica por debajo del umbral de 1.500 puntos, lo que, "
                "conforme a los estándares de referencia comparados y a la práctica de la Fiscalía "
                "Nacional Económica, permite presumir razonablemente que el mercado relevante "
                "definido mantendrá una estructura competitiva atomizada o moderadamente concentrada. "
                "Bajo esta hipótesis, resulta poco probable que la operación genere, por sí sola, "
                "una <b>reducción sustancial de la competencia (RSC)</b> en los términos del artículo 47 "
                "del D.L. 211, sea por efectos unilaterales (aumento unilateral de precios por parte de "
                "la entidad fusionada) o por efectos coordinados (facilitación de colusión tácita o "
                "expresa entre los competidores remanentes). En este escenario, la operación se "
                "encontraría, en principio, dentro de la <i>«zona segura»</i> (safe harbor) que orienta "
                "el análisis preliminar de la autoridad de competencia."
            ),
        }

    if 1500 <= post_hhi <= 2500:
        if delta_hhi < 250:
            return {
                "escenario": "Escenario 2 — Concentración Media",
                "nivel": "RIESGO MODERADO-BAJO",
                "color": GREEN,
                "bg": "#FFF8E7",
                "fase": "Fase I — Revisión ordinaria sin medidas de mitigación intensas",
                "texto": (
                    "El IHI post-operación se sitúa en la banda de concentración media (entre 1.500 y "
                    "2.500 puntos); sin embargo, la variación marginal (ΔIHI) generada directamente por "
                    "la fusión es inferior a 250 puntos. De acuerdo con la metodología de umbrales "
                    "aplicada, un incremento marginal de esta magnitud usualmente <b>no amerita la "
                    "imposición de medidas de mitigación estructurales o de conducta intensas</b>, dado que "
                    "el aporte incremental de poder de mercado atribuible específicamente a la operación "
                    "es limitado. No obstante, la FNE conserva la facultad de profundizar el análisis "
                    "cualitativo —barreras de entrada, poder de compra contrapuesto (countervailing buyer "
                    "power), diferenciación de producto y rivalidad dinámica— antes de descartar "
                    "definitivamente riesgos para la competencia."
                ),
            }
        else:
            return {
                "escenario": "Escenario 2 — Concentración Media",
                "nivel": "RIESGO MODERADO-ALTO",
                "color": YELLOW,
                "bg": "#FFF3CD",
                "fase": "Fase I extendida — Posible solicitud de información adicional (Fase II eventual)",
                "texto": (
                    "Aunque el IHI post-operación permanece dentro de la banda de concentración media "
                    "(1.500–2.500 puntos), el ΔIHI generado por la fusión <b>supera los 250 puntos</b>, lo "
                    "que constituye una señal de alerta relevante conforme a los estándares de referencia "
                    "utilizados. Un incremento marginal de esta magnitud sugiere que la operación podría "
                    "estar generando una <b>reducción sustancial de la competencia</b> al eliminar una "
                    "rivalidad significativa entre las partes, incrementando el riesgo de efectos "
                    "unilaterales (poder para subir precios o degradar calidad) y/o efectos coordinados "
                    "entre los actores remanentes del mercado relevante. Se recomienda profundizar el "
                    "análisis económico (cuotas dinámicas, elasticidades cruzadas, condiciones de entrada) "
                    "y evaluar la pertinencia de medidas de mitigación."
                ),
            }

    # post_hhi > 2500
    if delta_hhi < 150:
        return {
            "escenario": "Escenario 3 — Alta Concentración",
            "nivel": "RIESGO BAJO (en mercado ya concentrado)",
            "color": YELLOW,
            "bg": "#FFF3CD",
            "fase": "Notificación recomendada — Revisión documentada en Fase I",
            "texto": (
                "El mercado relevante presenta, en términos absolutos, un IHI post-operación superior a "
                "2.500 puntos, lo que lo califica como <b>altamente concentrado</b>. No obstante, el "
                "aporte incremental específico de la operación (ΔIHI) es inferior a 150 puntos, lo que "
                "indica que la alta concentración del mercado es <b>preexistente</b> y no es causada de "
                "forma determinante por esta fusión en particular. Bajo los criterios de incrementalidad "
                "que inspiran el análisis de la autoridad, el riesgo causalmente atribuible a la operación "
                "es comparativamente bajo. Con todo, dada la concentración estructural del mercado, se "
                "recomienda documentar exhaustivamente el análisis de barreras de entrada y poder "
                "compensatorio de la demanda."
            ),
        }
    else:
        return {
            "escenario": "Escenario 3 — Alta Concentración",
            "nivel": "ALERTA ROJA — ALTO RIESGO",
            "color": RED,
            "bg": "#FBE5E8",
            "fase": "Notificación obligatoria — Alta probabilidad de inicio de Fase II (investigación profunda)",
            "texto": (
                "El IHI post-operación supera los 2.500 puntos <b>y</b> el ΔIHI atribuible a la fusión "
                "supera los 150 puntos. Esta combinación constituye, conforme a los estándares de "
                "referencia comparados y a la práctica consolidada de la Fiscalía Nacional Económica, el "
                "indicador cuantitativo más severo de riesgo para la competencia: la operación se "
                "desarrolla en un mercado ya altamente concentrado y, además, <b>contribuye de forma "
                "determinante y no marginal</b> a dicha concentración. Resulta altamente probable que la "
                "operación pueda producir una <b>reducción sustancial de la competencia</b> —por efectos "
                "unilaterales, coordinados, o de cierre de mercado (foreclosure) frente a competidores o "
                "proveedores—. En consecuencia, la operación debiese ser <b>notificada obligatoriamente</b> "
                "a la FNE conforme al procedimiento del Título IV del D.L. 211, siendo razonable anticipar "
                "el inicio de una <b>investigación de Fase II</b>, así como la eventual exigencia de medidas "
                "de mitigación estructurales (desinversiones) o de conducta, o incluso el rechazo de la "
                "operación si dichas medidas no resultan idóneas."
            ),
        }


# =====================================================================
# ENCABEZADO
# =====================================================================
st.markdown(
    """
    <div class="app-header">
        <span class="badge">DERECHO ECONÓMICO · ANÁLISIS DE COMPETENCIA</span>
        <h1>⚖️ Analizador Automatizado de Operaciones de Concentración</h1>
        <p>Simulación de fusiones horizontales bajo el estándar del Índice de Herfindahl-Hirschman (IHI) —
        Umbrales de referencia de la Fiscalía Nacional Económica (FNE) de Chile.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# SIDEBAR — ENTRADA DE DATOS
# =====================================================================
with st.sidebar:
    st.markdown("### 📊 Datos del Mercado")
    market_name = st.text_input(
        "Nombre del mercado relevante",
        value="Mercado de Distribución Minorista de Combustibles, Región Metropolitana",
        help="Defina el mercado relevante en su dimensión de producto y geográfica.",
    )

    st.markdown("### 🏢 Participaciones de Mercado")
    raw_companies = st.text_area(
        "Empresas y participación (%)",
        value="Empresa A: 40, Empresa B: 30, Empresa C: 20, Empresa D: 10",
        height=120,
        help="Formato: 'Nombre: Valor', separado por comas. Ej: Copec: 35, Shell: 25, Petrobras: 20, Otros: 20",
    )

    cargar = st.button("🔄 Cargar / Actualizar Datos", use_container_width=True)

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.78rem; opacity:0.75; line-height:1.5;">
        <b>Umbrales aplicados (IHI, escala 0–10.000):</b><br>
        • &lt; 1.500 → Baja concentración<br>
        • 1.500 – 2.500 → Concentración media<br>
        • &gt; 2.500 → Alta concentración<br><br>
        <b>ΔIHI crítico:</b><br>
        • Zona media: 250 pts<br>
        • Zona alta: 150 pts
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================================
# ESTADO DE SESIÓN
# =====================================================================
if "df" not in st.session_state:
    st.session_state.df = None
if "color_map" not in st.session_state:
    st.session_state.color_map = {}

if cargar or st.session_state.df is None:
    items, errors = parse_companies(raw_companies)

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    elif len(items) < 2:
        st.error("⚠️ Debe ingresar al menos dos empresas para simular una operación de concentración.")
    else:
        names = [i[0] for i in items]
        if len(set(names)) != len(names):
            st.error("⚠️ Hay nombres de empresas duplicados. Verifique los datos ingresados.")
        else:
            total = sum(v for _, v in items)

            if total > 100.5:
                st.error(
                    f"⚠️ La suma de las participaciones ingresadas es **{total:.2f}%**, lo cual supera "
                    f"el 100%. Por favor revise los valores."
                )
            else:
                df = pd.DataFrame(items, columns=["Empresa", "Participación (%)"])

                if total < 99.5:
                    residual = round(100 - total, 2)
                    df = pd.concat(
                        [df, pd.DataFrame([{"Empresa": "Otros", "Participación (%)": residual}])],
                        ignore_index=True,
                    )
                    st.info(
                        f"ℹ️ La suma ingresada fue {total:.2f}%. Se agregó automáticamente la categoría "
                        f"residual **'Otros' ({residual:.2f}%)** para representar el resto del mercado "
                        f"atomizado, completando el 100%."
                    )
                elif abs(total - 100) > 0.001:
                    df["Participación (%)"] = df["Participación (%)"] / total * 100
                    st.caption(
                        f"Se normalizaron las participaciones por una diferencia de redondeo "
                        f"(suma original: {total:.2f}%)."
                    )

                df = df.sort_values("Participación (%)", ascending=False).reset_index(drop=True)
                st.session_state.df = df
                st.session_state.color_map = build_color_map(df["Empresa"])
                st.session_state.market_name = market_name
                # Si se recargaron datos nuevos, se descarta cualquier simulación de fusión previa
                # para evitar referencias a empresas que ya no existen en el nuevo set de datos.
                if cargar and "last_merge" in st.session_state:
                    del st.session_state["last_merge"]

# =====================================================================
# CUERPO PRINCIPAL
# =====================================================================
if st.session_state.df is not None:
    df = st.session_state.df
    color_map = st.session_state.color_map
    market_name = st.session_state.get("market_name", market_name)

    # ---- Sección: Estructura de mercado actual ----
    st.markdown(
        f"""<div class="section-card">
        <div class="section-title">🏛️ Estructura Actual del Mercado Relevante</div>
        <p style="color:#5C677D; margin-top:-6px;">{market_name}</p>
        </div>""",
        unsafe_allow_html=True,
    )

    col_table, col_chart = st.columns([1, 1.3])
    with col_table:
        display_df = df.copy()
        display_df["Participación (%)"] = display_df["Participación (%)"].map(lambda x: f"{x:.2f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)

        pre_hhi_preview = hhi(df["Participación (%)"])
        metric_box("IHI Actual del Mercado", f"{pre_hhi_preview:,.0f}", "puntos (escala 0–10.000)")

    with col_chart:
        fig_before = make_pie(df, "Distribución de Mercado — Situación Actual", color_map)
        st.plotly_chart(fig_before, use_container_width=True)

    # ---- Sección: Simulación de fusión ----
    st.markdown(
        """<div class="section-card">
        <div class="section-title">🤝 Simulación de la Operación de Concentración</div>
        </div>""",
        unsafe_allow_html=True,
    )

    eligible = df["Empresa"].tolist()
    eligible_no_otros = [e for e in eligible if e != "Otros"]

    if len(eligible_no_otros) < 2:
        st.warning("Se requieren al menos dos empresas identificables (distintas de 'Otros') para simular una fusión.")
    else:
        c1, c2, c3 = st.columns([1, 1, 0.6])
        with c1:
            empresa_1 = st.selectbox("Parte adquirente / Empresa 1", eligible_no_otros, index=0)
        with c2:
            opciones_2 = [e for e in eligible_no_otros if e != empresa_1]
            empresa_2 = st.selectbox("Parte adquirida / Empresa 2", opciones_2, index=0)
        with c3:
            st.write("")
            st.write("")
            simular = st.button("⚙️ Simular Fusión", type="primary", use_container_width=True)

        if simular or "last_merge" in st.session_state:
            if simular:
                st.session_state.last_merge = (empresa_1, empresa_2)

            e1, e2 = st.session_state.last_merge

            if e1 not in df["Empresa"].values or e2 not in df["Empresa"].values:
                st.warning(
                    "La simulación anterior hacía referencia a empresas que ya no están en los datos "
                    "actuales. Por favor, vuelva a presionar **'Simular Fusión'**."
                )
                del st.session_state["last_merge"]
                st.stop()

            s1 = float(df.loc[df["Empresa"] == e1, "Participación (%)"].iloc[0])
            s2 = float(df.loc[df["Empresa"] == e2, "Participación (%)"].iloc[0])

            merged_name = f"{e1} + {e2} (Fusionada)"
            merged_share = s1 + s2

            df_after = df[~df["Empresa"].isin([e1, e2])].copy()
            df_after = pd.concat(
                [df_after, pd.DataFrame([{"Empresa": merged_name, "Participación (%)": merged_share}])],
                ignore_index=True,
            )
            df_after = df_after.sort_values("Participación (%)", ascending=False).reset_index(drop=True)

            pre_hhi = hhi(df["Participación (%)"])
            post_hhi = hhi(df_after["Participación (%)"])
            delta_hhi = post_hhi - pre_hhi
            # Nota técnica: delta_hhi es matemáticamente idéntico a 2 × s1 × s2,
            # la fórmula estándar para el aporte incremental de una fusión al IHI.

            # ---- Resultados numéricos ----
            st.markdown(
                """<div class="section-card">
                <div class="section-title">📐 Resultados del Cálculo Económico</div>
                </div>""",
                unsafe_allow_html=True,
            )

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                metric_box("IHI Antes de la Fusión", f"{pre_hhi:,.0f}", "puntos")
            with m2:
                metric_box("IHI Después de la Fusión", f"{post_hhi:,.0f}", "puntos")
            with m3:
                metric_box("ΔIHI (Variación)", f"+{delta_hhi:,.0f}", f"= 2 × {s1:.1f}% × {s2:.1f}%")
            with m4:
                var_pct = (delta_hhi / pre_hhi * 100) if pre_hhi > 0 else 0
                metric_box("Variación Relativa", f"+{var_pct:,.1f}%", "respecto al IHI inicial")

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Gráficos comparativos ----
            col_b, col_a = st.columns(2)
            with col_b:
                fig1 = make_pie(df, "ANTES de la Fusión", color_map)
                st.plotly_chart(fig1, use_container_width=True)
            with col_a:
                fig2 = make_pie(df_after, "DESPUÉS de la Fusión", color_map, highlight_name=merged_name)
                st.plotly_chart(fig2, use_container_width=True)

            with st.expander("Ver tabla detallada — Estructura post-fusión"):
                display_after = df_after.copy()
                display_after["Participación (%)"] = display_after["Participación (%)"].map(lambda x: f"{x:.2f}%")
                st.dataframe(display_after, use_container_width=True, hide_index=True)

            # ---- Dictamen jurídico-económico ----
            result = evaluate_scenario(post_hhi, delta_hhi)

            st.markdown(
                f"""
                <div class="dictamen-box" style="background:{result['bg']}; border-left-color:{result['color']};">
                    <div class="dictamen-title" style="color:{result['color']};">
                        📋 Dictamen Jurídico-Económico Preliminar
                        <span class="dictamen-tag" style="background:{result['color']}; color:#FFFFFF;">{result['nivel']}</span>
                    </div>
                    <p style="margin-bottom:6px;"><b>{result['escenario']}</b> · IHI post-fusión:
                    <b>{post_hhi:,.0f} pts</b> · ΔIHI: <b>{delta_hhi:,.0f} pts</b></p>
                    <p style="margin-bottom:10px;">{result['texto']}</p>
                    <p style="margin:0; font-size:0.9rem;"><b>Tratamiento procedimental estimado:</b>
                    {result['fase']}.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="footer-note">
                Herramienta de apoyo pedagógico para el análisis preliminar de operaciones de concentración
                horizontal (Derecho de la Competencia / Análisis Económico del Derecho). Los umbrales de IHI
                y ΔIHI utilizados corresponden a estándares de referencia comparados y no sustituyen el
                análisis técnico, cualitativo y procedimental que efectúa la Fiscalía Nacional Económica
                conforme al D.L. 211 y su Guía vigente para el Análisis de Operaciones de Concentración.
                </div>
                """,
                unsafe_allow_html=True,
            )

else:
    st.info("👈 Ingrese los datos del mercado y las empresas en el panel lateral, luego presione **'Cargar / Actualizar Datos'**.")
