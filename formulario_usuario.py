import streamlit as st
import re
from datetime import date, datetime
import pandas as pd
from fpdf import FPDF
import base64
import io
import urllib.parse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def formulario_usuario():
    st.header("🧬 Evaluación MBI 360°")
    st.subheader("Completa tus datos antes de comenzar")

    nombre = st.text_input("Nombre completo")
    rut_dni = st.text_input("RUT / DNI")
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
    genero = st.text_input("Género (como te identificas)")
    fecha_nacimiento = st.date_input("Fecha de nacimiento", min_value=date(1900, 1, 1), max_value=date.today())
    correo = st.text_input("Correo electrónico")
    whatsapp = st.text_input("Número de WhatsApp (+código...) ej: +56912345678")

    errores = []

    if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        errores.append("❌ Correo no válido.")

    if whatsapp and not re.match(r"^\+\d{6,15}$", whatsapp):
        errores.append("❌ WhatsApp debe tener el formato internacional: +[código][número], sin espacios ni guiones.")

    def validar_rut_chileno(rut):
        rut = rut.upper().replace("-", "").replace(".", "")
        if len(rut) < 2:
            return False
        cuerpo = rut[:-1]
        dv = rut[-1]
        suma = sum(int(cuerpo[::-1][i]) * (2 + i % 6) for i in range(len(cuerpo)))
        dv_calc = 11 - (suma % 11)
        if dv_calc == 11:
            dv_calc = "0"
        elif dv_calc == 10:
            dv_calc = "K"
        else:
            dv_calc = str(dv_calc)
        return dv == dv_calc

    if rut_dni:
        rut_clean = rut_dni.strip()
        if re.match(r"^\d{7,8}-[\dkK]$", rut_clean):
            if not validar_rut_chileno(rut_clean):
                errores.append("❌ RUT chileno no válido.")

    if st.button("➡️ Continuar"):
        if errores:
            for error in errores:
                st.error(error)
        elif not nombre or not rut_dni or not genero:
            st.warning("⚠️ Por favor completa todos los campos obligatorios.")
        else:
            st.success("✅ Datos validados correctamente.")
            st.session_state["datos_usuario"] = {
                "Nombre": nombre,
                "RUT/DNI": rut_dni,
                "Sexo": sexo,
                "Género": genero,
                "Fecha de nacimiento": str(fecha_nacimiento),
                "Correo": correo,
                "WhatsApp": whatsapp
            }
            st.session_state["pagina"] = "seleccion_modulos"

formulario_usuario()
