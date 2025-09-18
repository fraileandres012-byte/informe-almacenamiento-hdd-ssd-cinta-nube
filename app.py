import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

st.set_page_config(page_title="Comparativa de almacenamiento", layout="wide")

st.title("Informe comparativo: HDD | SSD | Cinta | Nube")
st.caption("Todos los supuestos sin fuente explícita están marcados como [Inference]/[Unverified]. I cannot verify this.")

seccion = st.sidebar.selectbox(
    "Secciones",
    [
        "Resumen ejecutivo",
        "Escenario",
        "Criterios de evaluación",
        "Comparación (tabla)",
        "Gráficos (especificación)",
        "Simulación",
        "Arquitectura propuesta",
        "Riesgos y mitigaciones",
        "Conclusiones y próximos pasos",
        "Referencias (APA7)"
    ]
)
def datos_base():
    # Valores de referencia educativos. Marca los rangos no citados como [Inference]/[Unverified]
    # Ejemplos de valores orientativos (rellena tú con tus rangos/medias):
    data = [
        # Rellena con tus propios números/medias/rangos según tu informe
        {"Tecnologia":"HDD",  "Lectura_MB_s": "150–200 [Unverified]", "Escritura_MB_s":"120–180 [Unverified]",
         "Capacidad_TB":"1–20 [Unverified]", "Costo_GB_USD":"0.02–0.03 [Unverified]", "MTBF_horas":"1.2M–1.5M [Unverified]",
         "Consumo_W":"6–9 [Unverified]", "Seguridad_1_5":3, "Escalabilidad_1_5":3},
        {"Tecnologia":"SSD",  "Lectura_MB_s": "500–3500 [Unverified]", "Escritura_MB_s":"450–3000 [Unverified]",
         "Capacidad_TB":"1–8 [Unverified]", "Costo_GB_USD":"0.08–0.12 [Unverified]", "MTBF_horas":"1.5M–2M [Unverified]",
         "Consumo_W":"2–4 [Unverified]", "Seguridad_1_5":4, "Escalabilidad_1_5":3},
        {"Tecnologia":"Cinta","Lectura_MB_s": "250–300 [Unverified]", "Escritura_MB_s":"100–200 [Unverified]",
         "Capacidad_TB":"10–30 [Unverified]", "Costo_GB_USD":"0.01–0.02 [Unverified]", "MTBF_horas":"2M+ [Unverified]",
         "Consumo_W":"5–10 [Unverified]", "Seguridad_1_5":2, "Escalabilidad_1_5":2},
        {"Tecnologia":"Nube","Lectura_MB_s": "200–500* [Unverified]", "Escritura_MB_s":"150–400* [Unverified]",
         "Capacidad_TB":"Ilimitada (proveedor)", "Costo_GB_USD":"0.02–0.10** [Unverified]", "MTBF_horas":"SLA proveedor",
         "Consumo_W":"Proveedor", "Seguridad_1_5":5, "Escalabilidad_1_5":5}
    ]
    return pd.DataFrame(data)
if seccion == "Resumen ejecutivo":
    st.subheader("Resumen ejecutivo")
    st.write("""
    Este proyecto compara HDD, SSD, Cinta y Nube con foco en coste/rendimiento/escalabilidad.
    Recomendación: enfoque híbrido (SSD para OLTP, HDD secundario, Cinta archivo, Nube para picos/DR).
    Implicaciones: latencia, OPEX/CAPEX, cumplimiento (GDPR), continuidad de negocio.
    """)
if seccion == "Escenario":
    st.subheader("Descripción del escenario")
    st.markdown("""
- Necesidades: baja latencia (OLTP), analítica, backups, archivado.
- Restricciones: presupuesto CAPEX/OPEX, cumplimiento (GDPR), SLA 99.9%.
- Cargas: transaccional, analítica secuencial, copias periódicas.
- Crecimiento esperado: 20% anual.
- Métricas de partida (ejemplo educativo):
  - Volumen inicial: 100 TB [Inference]/[Unverified] — *I cannot verify this*.
  - Latencia objetivo: 10 ms en operaciones críticas [Inference]/[Unverified].
""")
if seccion == "Comparación (tabla)":
    st.subheader("Tabla comparativa")
    df_csv = None
    try:
        df_csv = cargar_csv()
    except Exception:
        pass

    df = df_csv if df_csv is not None else datos_base()
    st.dataframe(df, use_container_width=True)
    st.info("Valores marcados [Unverified] son orientativos/educativos. I cannot verify this.")
    st.markdown("""
**Lectura ejecutiva (trade-offs)**
- SSD: mejor latencia/rendimiento; mayor coste por GB.
- HDD: equilibrio coste/GB con rendimiento medio.
- Cinta: mínimo coste para archivo; acceso lento.
- Nube: elasticidad y seguridad avanzada; depende de conectividad y puede elevar OPEX según uso.
""")
if seccion == "Gráficos (especificación)":
    st.subheader("Especificación de gráficos con matplotlib")
    st.markdown("""
- **Barras**: velocidad de **lectura** por tecnología (una figura).
- **Barras**: velocidad de **escritura** por tecnología (otra figura).
- **Barras**: costo por GB por tecnología (otra figura). Opcional: estimación de costo anual (explicar supuestos).
- **Radar** (o alternativa en barras): Fiabilidad, Escalabilidad, Seguridad en escala 1–5.
**Reglas**: matplotlib, **una figura por gráfico**, **sin fijar colores**.
""")
    st.warning("Este apartado describe la especificación. Implementa los gráficos respetando las reglas si decides añadirlos.")
if seccion == "Simulación":
    st.subheader("Simulación de rendimiento (modelo simple)")

    col1, col2, col3 = st.columns(3)
    with col1:
        vol_inicial_tb = st.number_input("Volumen inicial (TB)", min_value=10, max_value=5000, value=100, step=10)
    with col2:
        crecimiento_pct = st.number_input("Crecimiento anual (%)", min_value=0, max_value=200, value=20, step=5)
    with col3:
        horizonte_anios = st.number_input("Horizonte (años)", min_value=1, max_value=10, value=5, step=1)

    st.markdown("""
**Supuesto de cálculo (simplificado):**
`tiempo_horas = (volumen_TB * 1024 GB/TB * 1024 MB/GB) / (velocidad_MB_s * 3600 s/h)`

[Inference]/[Unverified] — No considera IOPS, colas, latencias de red, compresión, paralelismo real, ni políticas de caché.
    """)

    # Plantilla de velocidades promedio (rellena con tus promedios estimados)
    velocidades = {
        "HDD": 180,   # MB/s [Unverified]
        "SSD": 1400,  # MB/s [Unverified]
        "Cinta": 270, # MB/s [Unverified]
        "Nube": 300   # MB/s [Unverified] (dependiente de red)
    }

    # Cálculo de la serie de volúmenes y tiempos
    anos = list(range(1, horizonte_anios + 1))
    volumenes = []
    v = float(vol_inicial_tb)
    for _ in anos:
        volumenes.append(v)
        v = v * (1 + crecimiento_pct/100.0)

    resultados = []
    for idx, vol_tb in enumerate(volumenes, start=1):
        fila = {"Año": idx, "Volumen_TB": ceil(vol_tb)}
        for tech, vel in velocidades.items():
            try:
                segundos = (vol_tb * 1024 * 1024) / vel
                horas = segundos / 3600
                fila[tech] = round(horas, 1)
            except Exception:
                fila[tech] = None
        resultados.append(fila)

    st.dataframe(pd.DataFrame(resultados), use_container_width=True)
    st.markdown("""
**Interpretación ejecutiva (ejemplo educativo):**
- SSD mantiene tiempos significativamente menores; útil para SLA ajustados o ventanas de backup cortas.
- HDD y Cinta se tensionan con volúmenes crecientes; adecuados para secundario/archivo.
- Nube es competitiva si la conectividad es estable; revisar ancho de banda y egress.
""")
if seccion == "Conclusiones y próximos pasos":
    st.subheader("Conclusiones y recomendación")
    st.markdown("""
- **Recomendación**: arquitectura híbrida (SSD + HDD + Cinta + Nube) por balance de coste/rendimiento/escalabilidad.
- **Justificación**: latencia crítica en OLTP (SSD); coste/GB competitivo en secundario (HDD); archivo barato (Cinta); elasticidad y DR (Nube).
""")
    st.subheader("Próximos pasos")
    st.markdown("""
1. PoC con dataset real: medir latencia, throughput y ventana de backup.
2. Validar costes con proveedores (almacenamiento y nube); modelar TCO 3-5 años.
3. Pruebas de carga/fallo: RPO/RTO, restauraciones, pruebas de conectividad.
4. Plan de migración por fases; métricas de éxito y governance.
""")
if seccion == "Referencias (APA7)":
    st.subheader("Referencias (APA7)")
    st.markdown("""
- [Inference]/[Unverified] Valores orientativos sin fuente: “I cannot verify this.”
- Ejemplos de referencias a completar cuando cites fuentes reales:
  - IDC. (2023). *Worldwide Hard Disk Drive Forecast, 2023–2027*. IDC Research.
  - AWS. (2024). *Amazon S3 pricing*. https://aws.amazon.com/s3/pricing/
  - IBM. (2023). *LTO Ultrium Tape Storage*.
  - Seagate. (2023). *Exos Enterprise HDD Datasheet*.
""")
HDD,"150–200 [Unverified]","120–180 [Unverified]","1–20 [Unverified]","0.02–0.03 [Unverified]","1.2M–1.5M [Unverified]","6–9 [Unverified]",3,3
SSD,"500–3500 [Unverified]","450–3000 [Unverified]","1–8 [Unverified]","0.08–0.12 [Unverified]","1.5M–2M [Unverified]","2–4 [Unverified]",4,3
Cinta,"250–300 [Unverified]","100–200 [Unverified]","10–30 [Unverified]","0.01–0.02 [Unverified]","2M+ [Unverified]","5–10 [Unverified]",2,2
Nube,"200–500* [Unverified]","150–400* [Unverified]","Ilimitada (proveedor)","0.02–0.10** [Unverified]","SLA proveedor","Proveedor",5,5
