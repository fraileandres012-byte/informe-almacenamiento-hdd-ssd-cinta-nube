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
