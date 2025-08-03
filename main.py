
# -*- coding: utf-8 -*-
# MBI 360° - Evaluación Integral con PDF UTF-8
# Autor: Aníbal Saavedra

import streamlit as st
from datetime import datetime
import csv
from fpdf import FPDF
import os

# ============================
# FORMULARIO DE DATOS PERSONALES
# ============================

st.set_page_config(page_title="MBI 360°", page_icon="🌀", layout="centered")
st.title("🌀 MBI 360° – Evaluación Integral del Ser")

st.markdown("Completa tus datos antes de comenzar")

nombre = st.text_input("Nombre completo")
dni = st.text_input("RUT / DNI")
sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
genero = st.text_input("Género (como te identificas)")
fecha_nacimiento = st.date_input("Fecha de nacimiento")
correo = st.text_input("Correo electrónico")
whatsapp = st.text_input("Número de WhatsApp (+código...) ej: +56912345678")

if not all([nombre, dni, genero, correo, whatsapp]):
    st.warning("Completa todos los campos para habilitar la evaluación.")
    st.stop()

st.success("✅ Datos validados correctamente.")

# ============================
# SELECCIÓN DE MÓDULOS
# ============================

st.markdown("### Selecciona uno o varios módulos que deseas realizar:")

modulos = [
    "Test de disociación o trauma",
    "Estado epigenético emocional (líneas materna/paterna)",
    "Condiciones clínicas opcionales"
]
modulos_seleccionados = st.multiselect("", modulos)

# ============================
# FUNCIONES DE RESULTADOS
# ============================

resultados = {}

def ejecutar_test_disociacion():
    st.subheader("🧠 Test de Disociación o Trauma")
    puntaje = st.slider("¿Cuánto te desconectas de tus emociones?", 0, 100, 50)
    interpretacion = "Alta disociación" if puntaje > 70 else "Disociación leve/moderada"
    st.write("Resultado:", interpretacion)
    resultados["Disociación"] = interpretacion

def ejecutar_test_epigenetico():
    st.subheader("🧬 Estado Epigenético Emocional")
    madre = st.slider("Carga emocional heredada de la madre", 0, 100, 40)
    padre = st.slider("Carga emocional heredada del padre", 0, 100, 60)
    interpretacion = "Predomina línea paterna" if padre > madre else "Predomina línea materna"
    st.write("Resultado:", interpretacion)
    resultados["Epigenético"] = interpretacion

def ejecutar_test_condiciones_clinicas():
    st.subheader("⚕️ Condiciones Clínicas")
    inflamacion = st.checkbox("Inflamación crónica")
    fatiga = st.checkbox("Fatiga persistente")
    sintomas = []
    if inflamacion: sintomas.append("Inflamación crónica")
    if fatiga: sintomas.append("Fatiga persistente")
    resultado = ", ".join(sintomas) if sintomas else "Sin condiciones seleccionadas"
    st.write("Resultado:", resultado)
    resultados["Condiciones clínicas"] = resultado

# ============================
# EJECUCIÓN DE MÓDULOS
# ============================

if modulos_seleccionados:
    if "Test de disociación o trauma" in modulos_seleccionados:
        ejecutar_test_disociacion()
    if "Estado epigenético emocional (líneas materna/paterna)" in modulos_seleccionados:
        ejecutar_test_epigenetico()
    if "Condiciones clínicas opcionales" in modulos_seleccionados:
        ejecutar_test_condiciones_clinicas()

    # ============================
    # GUARDAR RESULTADOS EN CSV
    # ============================
    st.markdown("---")
    st.subheader("💾 Guardar Resultados")

    csv_file = "respuestas_mbi360.csv"
    campos = ["Fecha", "Nombre", "DNI", "Sexo", "Género", "Nacimiento", "Correo", "WhatsApp"] + list(resultados.keys())
    datos = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nombre, dni, sexo, genero, str(fecha_nacimiento), correo, whatsapp] + list(resultados.values())

    escribir_csv = not os.path.exists(csv_file)
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if escribir_csv:
            writer.writerow(campos)
        writer.writerow(datos)

    st.success("✅ Resultados guardados en CSV correctamente.")

    # ============================
    # GENERAR PDF CON UTF-8
    # ============================

    pdf_file = "informe_mbi360.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "🌀 Informe MBI 360° – Evaluación Integral", ln=True)
    pdf.ln(4)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 10, f"DNI: {dni}", ln=True)
    pdf.cell(0, 10, f"Sexo: {sexo} | Género: {genero}", ln=True)
    pdf.cell(0, 10, f"Nacimiento: {fecha_nacimiento}", ln=True)
    pdf.cell(0, 10, f"Correo: {correo}", ln=True)
    pdf.cell(0, 10, f"WhatsApp: {whatsapp}", ln=True)
    pdf.ln(10)

    for modulo, resultado in resultados.items():
        pdf.cell(0, 10, f"{modulo}: {resultado}", ln=True)

    pdf.output(pdf_file)
    st.success("📄 Informe PDF generado correctamente.")

    # ============================
    # ENLACES Y DESCARGAS
    # ============================
    st.markdown("---")
    st.subheader("📂 Descargas")

    with open(csv_file, "rb") as f:
        st.download_button("📥 Descargar CSV", f, file_name="respuestas_mbi360.csv")

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Descargar Informe PDF", f, file_name="informe_mbi360.pdf", mime="application/pdf")

    # ============================
    # MENSAJE WHATSAPP
    # ============================
    st.markdown("---")
    st.subheader("📲 Compartir por WhatsApp")
    mensaje = f"Hola, acabo de realizar mi evaluación MBI 360° y estos fueron mis resultados:\n" + "\n".join([f"{k}: {v}" for k,v in resultados.items()])
    enlace = f"https://wa.me/56967010107?text={mensaje.replace(' ', '%20')}"
    st.markdown(f"[Enviar resumen por WhatsApp]({enlace})")
