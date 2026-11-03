# 🚇 Análisis de Demanda y Sensibilidad Tarifaria - Subtes de Buenos Aires

**Trabajo Final Integrador | Metodología de la Investigación**  
*Licenciatura en Ciencia de Datos — Universidad del Gran Rosario (UGR)*  
**Ciclo Lectivo:** 2026  

### 👥 Integrantes (Grupo 31)
* Leonel Rivera
* Cristian Brandino
* Bruno Suarez

---

## 📌 Descripción del Proyecto
Este proyecto analiza los patrones espaciotemporales de demanda y la sensibilidad de los usuarios ante adecuaciones tarifarias en la red de subterráneos de la Ciudad Autónoma de Buenos Aires (CABA). Mediante la metodología **CRISP-DM**, se integraron microdatos de validaciones por molinete con series históricas de tarifas para evaluar la concentración en horas pico, la brecha hábil vs. fin de semana y la elasticidad precio de la demanda ($E_p$).

---

## ⚙️ Requisitos Previos

Para ejecutar este proyecto en tu computadora local necesitas tener instalado:
* **Python:** Versión 3.10, 3.11 o 3.12 ([Descargar Python](https://www.python.org/downloads/)).
* **Git:** Para clonar el repositorio ([Descargar Git](https://git-scm.com/)).

---

## 🚀 Despliegue en la Nube
El tablero interactivo se encuentra publicado y accesible públicamente sin costo en:  
👉 **[Acceder al Tablero en Streamlit Cloud](https://TU_USUARIO.streamlit.app)** *(reemplazar con tu enlace final)*

---

## 💻 Instrucciones para Ejecución Local

Si deseas clonar el proyecto y ejecutar el tablero en tu máquina:

### 1. Clonar el repositorio

git clone [https://github.com/leonelrivera/subtes-caba-analitica.git](https://github.com/leonelrivera/subtes-caba-analitica.git)
cd subte-caba-analitica

### 2. Crear y activar un entorno virtual (recomendado)
python -m venv venv

* En Windows:
venv\Scripts\activate

* En Linux / macOS:
source venv/bin/activate

### 3. Instalar las dependencias
pip install -r requirements.txt

### 4. Iniciar el Tablero Interactivo
streamlit run app.py