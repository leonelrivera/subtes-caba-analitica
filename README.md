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
👉 **[Acceder al Tablero en Streamlit Cloud](https://subtes-caba-tablero-g31.streamlit.app)**

---

## 📖 Manual de Usuario y Guía Metodológica

Para conocer en detalle el funcionamiento de cada filtro, el significado de las tarjetas de indicadores (KPIs), la interpretación de los gráficos temporales/espaciales y el modelado econométrico de elasticidad, consulta la guía detallada con capturas de pantalla:

👉 **[Ver Manual de Usuario del Tablero](docs/MANUAL_USUARIO.md)**

---

## 💻 Instrucciones para Ejecución Local

Si deseas clonar el proyecto y ejecutar el tablero en tu máquina:

### 1. Clonar el repositorio
```bash
git clone https://github.com/leonelrivera/subtes-caba-analitica.git
```
```bash
cd subtes-caba-analitica
```
### 2. Crear y activar un entorno virtual (recomendado)
```bash
python -m venv venv
```
* En Windows (Git Bash):
```bash
source venv/Scripts/activate
```
* En Windows (CMD / PowerShell):
```bash
venv\Scripts\activate
```
* En Linux / macOS:
```bash
source venv/bin/activate
```
### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```
### 4. Iniciar el Tablero Interactivo
```bash
streamlit run app.py
```
Una vez iniciado el servidor, la aplicación se abrirá de manera automática en tu navegador web. En caso de que no lo haga, podés ingresar manualmente a:
URL Local: 
```bash
http://localhost:8501
```
URL de Red: 
```bash
http://127.0.0.1:8501
```

---

## 📂 Estructura del Repositorio y Artefactos de la Solución

* `app.py`: Código fuente del tablero interactivo de control operacional y analítico desarrollado con Streamlit y Plotly.
* `subte_procesado.csv`: Dataset principal limpio, optimizado y preprocesado (822.363 registros), consumido de forma directa por la aplicación web para maximizar el rendimiento.
* `BaseUnificadaEstaciones.csv`: Corpus de datos original consolidado a nivel de estación y molinete, utilizado como insumo inicial en el pipeline de transformación.
* `registro-historico-del-precio-del-boleto.csv`: Serie temporal histórica de los cuadros tarifarios y valores nominales aprobados por SBASE.
* `viajes_anual.csv`: Serie histórica consolidada con los volúmenes anuales de pasajeros transportados discriminados por línea.
* `requirements.txt`: Especificación estandarizada de librerías y dependencias necesarias para la reproducción del entorno.
* `docs/`: Directorio que contiene el `MANUAL_USUARIO.md` y los recursos visuales del proyecto.

### 🔬 Cuaderno de Auditoría Metodológica: `EDA_ETL_Subtes.ipynb`
El cuaderno Jupyter/Colab documenta el ciclo de datos completo previo al despliegue:
* **Pipeline ETL:** Auditoría de valores nulos, depuración de anomalías tipográficas en líneas y categorización de franjas horarias operativas y días hábiles.
* **Análisis Exploratorio (EDA):** Caracterización de curvas de afluencia intradiarias, cálculo del ratio hábil vs. fin de semana y estimación econométrica de la Elasticidad de Arco ($E_p$).
* **Generación del artefacto:** Exportación del dataset depurado `subte_procesado.csv`.

> **Nota para la evaluación:** El cuaderno se encuentra **completamente ejecutado y con todas sus salidas, métricas y gráficos visibles**. Puede auditarse de forma estática en GitHub o abrirse directamente en [Google Colab](https://colab.research.google.com/drive/172n230bqL_U_Mtcg70EkQixY7GbV63lb). Para interactuar con la solución desarrollada no es necesario ejecutar nuevamente el pipeline de datos; basta con acceder al tablero en la nube o correr `streamlit run app.py`.

---