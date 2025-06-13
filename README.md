# proyecto-integrado-v-datos-msft-analytics 🚀

<div align="center">
  <h1>Proyecto Integrado V – Línea de Énfasis</h1>
  <h3>Entrega 2: Automatización de la recolección y análisis de datos históricos del indicador MSFT (Microsoft) desde Yahoo Finanzas y MSFT Insight 360: Enriquecimiento, Predicción y Visualización 📈🤖🔍📊💡</h3>
</div>

---

<div align="center" style="margin: 40px 0;">
  <a href="https://msft-analytics-dashboard.streamlit.app/" target="_blank" 
     style="
       display: inline-block;
       background-color: #d32f2f;
       color: white;
       font-size: 26px;
       font-weight: bold;
       padding: 18px 45px;
       border-radius: 12px;
       text-decoration: none;
       box-shadow: 0 4px 12px rgba(211,47,47,0.4);
       transition: background-color 0.3s ease;
     "
     onmouseover="this.style.backgroundColor='#b02727'"
     onmouseout="this.style.backgroundColor='#d32f2f'"
  >
    🚀 Abrir Dashboard Interactivo en Streamlit
  </a>
  <div style="margin-top: 15px; font-size: 16px; font-style: italic;">
    Haz clic para explorar los KPIs y visualizaciones interactivas del proyecto.
  </div>
</div>

---

<div align="center" style="margin: 40px 0;">
  <a href="https://drive.google.com/file/d/1deOZeV6LxbOFJ_qomskiRrYN-A7QCvsy/view?usp=sharing" target="_blank" 
     style="
       display: inline-block;
       background-color: #1976d2;
       color: white;
       font-size: 26px;
       font-weight: bold;
       padding: 18px 45px;
       border-radius: 12px;
       text-decoration: none;
       box-shadow: 0 4px 12px rgba(25,118,210,0.4);
       transition: background-color 0.3s ease;
     "
     onmouseover="this.style.backgroundColor='#155a9c'"
     onmouseout="this.style.backgroundColor='#1976d2'"
  >
    🎥 Ver Video - Actividad Final
  </a>
  <div style="margin-top: 15px; font-size: 16px; font-style: italic;">
    Haz clic para ver la presentación en video de los resultados clave del proyecto.
  </div>
</div>

---

Este proyecto implementa **EA1 – Ingestión de Datos** para recolectar, transformar, persistir y auditar datos históricos de la acción **Microsoft Corporation (MSFT)** desde **Yahoo Finanzas**, 

El proyecto emplea:

- **Python** 🐍  
- **venv** 📦
- **yfinance** 🤖  
- **pandas** 📊 
- **numpy** 🔢
- **scikit-learn** 📊
- **statsmodels** 📉
- **matplotlib** 🎨
- **tensorflow** ⚡
- **streamlit** 🖥️
- **plotly** ✨
- **CSV** 📑 
- **SQLite** 🗄️    
- **logs** 📋
- **Modelo LSTM** 🧠
- **pkl** 💾
- **GitHub Actions** 🤖 (CI/CD diario automatizado)

Entre otros.

---

Este proyecto también implementa **EA2 – Entrega 2** para:


### 🔄 Enriquecimiento de Datos

Se añaden fuentes adicionales y transformaciones (variables temporales, indicadores macro).

Se incorporan transformaciones y nuevas variables a la serie temporal, incluyendo:

- Variables temporales (día de la semana, mes, etc.) 📅  
- Indicadores técnicos y macroeconómicos 📉  
- Limpieza y formateo avanzado de los datos 🧹  

---

### 🧠 Modelo Predictivo

Se ha utilizado un **modelo de red neuronal recurrente** concreto:

* **Arquitectura**: un `Sequential` de Keras con

  1. Una capa **LSTM** de 50 unidades (activación ReLU)
  2. Una capa **Dense** de salida (1 neurona)

Este tipo de modelo (Long Short-Term Memory) está diseñado para capturar dependencias temporales en series de datos (aquí, precios de cierre diarios), aprovechando su “memoria” interna para modelar patrones a lo largo de la ventana de entrada (30 días).


El modelo está implementado en una clase dedicada dentro de `src/modeller.py`, que incluye:

- `entrenar()`: entrena un modelo de series de tiempo y guarda el artefacto en `static/models/model.pkl`  
- `predecir()`: carga el modelo entrenado y genera predicciones futuras  

📐 **Métrica utilizada**:  
Se justifica el uso de **RMSE (Root Mean Squared Error)** por penalizar errores grandes, ideal para predicción de precios financieros. Se muestra su cálculo durante la evaluación del modelo.

---

### 📊 Dashboard BI Interactivo

Interfaz interactiva con 5 KPI (tasa de variación, media móvil, volatilidad, retorno acumulado, desviación estándar).

Desarrollado con **Streamlit**, visualiza y permite explorar de forma intuitiva **5 KPIs clave**:

- 📈 Tasa de variación  
- 🔁 Media móvil  
- ⚖️ Volatilidad  
- 💹 Retorno acumulado  
- 📏 Desviación estándar  

Se encuentra en `src/dashboard.py` y se actualiza automáticamente mediante GitHub Actions, asi también mediante Streamlit.

---

## Contenido

1. [Descripción General](#descripción-general-🌟)   
2. [Estructura del Proyecto](#estructura-del-proyecto-📂)  
3. [Requerimientos Previos](#requerimientos-previos-✅)  
4. [Instalación y Setup](#instalación-y-setup-⚙️)  
5. [Uso Local](#uso-local-🚀)  
6. [Automatización con GitHub Actions](#automatización-con-github-actions-🤖)  
7. [Trazabilidad y Logging](#trazabilidad-y-logging-🪵)  
8. [Licencia y Autores](#licencia-y-autores-📝)
9. [Autores](#11-autores)

---

## 1. Descripción General 🌟

Desde su salida a bolsa el **13 de marzo de 1986**, MSFT ha generado **casi 40 años** de datos diarios (apertura, máximo, mínimo, cierre, volumen). Este proyecto:

- **Automatiza** la descarga de cotizaciones 📥  
- **Transforma** y estandariza formatos 🧹  
- **Enriquece** los datos con variables adicionales (p. ej., temporales o indicadores macroeconómicos, entre otras) 📊  
- **Persiste** el histórico de manera incremental en **SQLite** y **CSV** 🗄️📑  
- **Registra** cada paso con un **sistema de logging dual** (consola + archivo) 🪵  
- **Programa** actualizaciones diarias mediante **GitHub Actions** ⏰🤖  

Además, incluye:

- **Modelo predictivo** en un módulo independiente (`src/modeller.py`) 🤖📈  
  - `entrenar()`: entrena y guarda el modelo como artefacto, archivo en `static/models/model.pkl`  
  - `predecir()`: carga `model.pkl` y devuelve predicciones  
  - Justificación y cálculo de métricas como **RMSE**, **MAE**, u otras apropiadas según el caso 📐  

- **Dashboard BI interactivo** con al menos **5 KPI clave**:  
  - Tasa de variación 📈  
  - Media móvil 📉  
  - Volatilidad 📊  
  - Retorno acumulado 🔁  
  - Desviación estándar 📏  

---

## 2. Estructura del Proyecto 📂

```text
proyecto-integrado-v-datos-msft-analytics/
├── .github/
│   └── workflows/
│       └── update_data.yml              # CI: cron, dispatch, push
├── docs/
│   └── AlexisMachado_JuliánMartínez # Documento de entrega
├── src/
│   └── msft_analytics/
│       ├── __pycache__/
│       ├── collector.py                # Clase MSFTCollector
│       ├── dashboard.py                # Dashboard BI con KPIs
│       ├── enricher.py                 # Enriquecimiento de datos
│       ├── logger.py                   # Logger dual consola/archivo
│       ├── modeller.py                 # Modelo predictivo (entrenar / predecir)
│       ├── predict_lstm.py             # (Model.pkl LSTM Artefacto entrenado)
│       ├── msft_analysis.ipynb         # Exploración y pruebas en notebook
│       ├── static/
│       │   ├── data/
│       │   │   ├── historical.db              # Base SQLite
│       │   │   ├── historical.csv             # Datos históricos
│       │   │   └── historical_enriched.csv    # Enriquecidos
│       │   ├── logs/
│       │   │   ├── msft_analytics.log         # Log collector
│       │   │   ├── msft_enricher.log          # Log enricher
│       │   │   ├── msft_inference.log         # Log de predicciones
│       │   │   └── msft_model.log             # Log modelado
│       │   └── models/
│       │       └── model.pkl                  # Artefacto entrenado
├── setup.py                         # Instalación y entry-point CLI
├── requirements.txt                 # Dependencias: pandas, yfinance, etc.
├── .gitignore
└── README.md                        # (este archivo)

````

---

## 3. Requerimientos Previos ✅

Antes de ejecutar el proyecto, asegúrate de contar con:

* 🐍 **Python 3.8+**
* 🌐 **Internet**
* 🔧 **Git** (clonación y CI)
* 🤖 **Cuenta en GitHub** para Actions

---

## 4. Instalación y Setup ⚙️

### 🔹 1. Clonar con Git
Ejecuta el siguiente comando en tu terminal:  

```bash
git clone https://github.com/Alexis-Machado/proyecto-integrado-v-datos-msft-analytics.git
``` 

### Creación y Activación de un Entorno Virtual (Recomendado) 🛠️

Para mantener organizadas las dependencias del proyecto y evitar conflictos con otras instalaciones de Python, se recomienda usar un entorno virtual.

Ejecuta el siguiente comando dentro de la carpeta del proyecto:

```bash
python -m venv venv
```

🔹 Activar el entorno virtual

🔹 En Windows 🖥️

```bash
venv\Scripts\activate
```

🔹 En Linux/Mac 💻

```bash
source venv/bin/activate
```

🔹 Verificar la activación ✅  
Si el entorno se activó correctamente, deberías ver **(venv)** al inicio de tu línea de comandos.<br><br>

### 🔹 Instalación de dependencias  

Para ejecutar el proyecto correctamente y facilitar su instalación, es necesario instalar las bibliotecas requeridas o utilizar setup.py.


Ejecuta los siguientes comandos en la raíz del proyecto (asegúrate de tener el entorno virtual activo si lo estás usando):  

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará todas las bibliotecas necesarias para el proyecto (por ejemplo: pandas
yfinance, etc.). ✅

## 🔹 Recomendado Uso de setup.py (Empaquetado e Instalación)

El proyecto incluye un setup.py que permite instalarlo como un paquete Python local.

```python
from setuptools import setup, find_packages 

setup(
    name="proyecto-integrado-v-datos-msft-analytics", 
    version="2.0.0",  
    author="Jhon Alexis Machado Rodriguez",  
    author_email="jmachadoa12@gmail.com",  
    description="Proyecto Integrado V - Línea de Énfasis (Entrega 2): Automatización de la recolección y análisis de datos históricos del indicador MSFT (Microsoft) desde Yahoo Finanzas y MSFT Insight 360: Enriquecimiento, Predicción y Visualización",

    # Encontramos paquetes en la carpeta src
    packages=find_packages(where="src"), 
    # Definimos src como directorio raíz de código
    package_dir={"": "src"},  

    # Dependencias necesarias
    install_requires=[
        "pandas>=2.2.3",
        "yfinance>=0.2.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.0.0",
        "statsmodels>=0.14.0",
        "matplotlib>=3.7.0",
        "tensorflow>=2.11.0",
        "streamlit>=1.24.0",
        "plotly>=5.15.0"
    ],

    # Scripts de consola al instalar los paquetes
    entry_points={  
        "console_scripts": [
            "msft-collector=msft_analytics.collector:run",
            "msft-enricher=msft_analytics.enricher:run",
            "msft-modeller=msft_analytics.modeller:run",
            "msft-predict=msft_analytics.predict_lstm:run"
        ],
    },

    # Metadatos estándar
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # Versión mínima de Python
    python_requires=">=3.8", 
)

```

Asegúrate de estar en el directorio raíz del proyecto (donde está setup.py).  
Para instalarlo, ejecuta:

```bash
pip install -e .
```

Esto instalará el paquete en tu entorno Python y permitirá modificar el código sin necesidad de reinstalarlo.

---

## 5. Uso Local 🚀

Tras configurar el entorno, ejecuta:

```bash
python src/msft_analytics/collector.py
python src/msft_analytics/enricher.py  
python src/msft_analytics/modeller.py   
python src/msft_analytics/predict_lstm.py
streamlit run src/msft_analytics/dashboard.py  

```

> O simplemente:
>
> ```bash
> msft-collector
> msft-enricher
> msft-modeller
> msft-predict
> streamlit run src/msft_analytics/dashboard.py  
> ```
>
> 

Al finalizar, verás en consola logs detallados y en `static/data/` los archivos actualizados.

---

### 🔹 Archivos generados al finalizar

✔ **Base de datos SQLite:**  
📂 Se crea (o actualiza) el archivo `historical.db` en `src/msft_analytics/static/data/`.

✔ **Archivo CSV completo:**  
📊 Se genera o actualiza el archivo `historical.csv` con todos los registros históricos desde 1986 en `src/msft_analytics/static/data/`.

✔ **Archivo CSV enriquecido:**  
➕ Se guarda `historical_enriched.csv` con variables derivadas o fuentes adicionales en `src/msft_analytics/static/data/`.

✔ **Modelo entrenado:**  
🧠 Se guarda el artefacto de modelo en `model.pkl`, ubicado en `src/msft_analytics/static/models/`.

✔ **Logs detallados de cada componente:**  
📝  
- `msft_analytics.log`: proceso de recolección  
- `msft_enricher.log`: proceso de enriquecimiento  
- `msft_model.log`: entrenamiento del modelo  
- `msft_inference.log`: predicciones generadas  
Ubicados todos en `src/msft_analytics/static/logs/`.

📊 **Dashboard interactivo:**  
🚀 Para visualizar el panel BI con KPIs y visualizaciones, ejecuta:

```bash
streamlit run src/msft_analytics/dashboard.py
```

---

## 6. Automatización con GitHub Actions 🤖

El workflow `.github/workflows/update_data.yml` incluye:

```bash
name: 📊 MSFT DataOps - Colector, Enriquecimiento, Modelo y Dashboard

on:
  schedule:
    - cron: "0 5 * * *" # ⏰ Se Ejecuta Cada Día a Medianoche (hora de Colombia, UTC-5)
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: 🛎️ Checkout del repositorio
        uses: actions/checkout@v3

      - name: 🐍 Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 📦 Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: 🚀 Ejecutar colector
        run: |
          msft-collector

      - name: ✨ Ejecutar enriquecimiento
        run: |
          msft-enricher

      - name: 🧠 Ejecutar modelo
        run: |
          msft-modeller

      - name: 🔮 Ejecutar predicción
        run: |
          msft-predict

      - name: 📂 Configurar Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: 📤 Commit del Colector, Enriquecimiento, Modelo y Dashboard
        run: |
          git add src/msft_analytics/static/data/*.csv
          git add src/msft_analytics/static/logs/*.log
          git add src/msft_analytics/static/models/*.pkl
          git commit -m "📊 Actualización Automática de Datos [GitHub Actions]" || echo "No hay cambios para commitear"
          git push

```

* **cron**: 🤖 (diario a la medianoche "0 5 * * *" hora de Colombia, UTC-5)
* **workflow\_dispatch**: 🖱️ manual
* **push**: 🔀 a `main`

---

## 7. Trazabilidad y Logging 🪵

El logger registra:

* **INFO**: inicio/fin de descarga, número de registros, rutas generadas
* **WARNING/ERROR**: problemas de conexión, estructura de tabla, etc.

**Ejemplo en** `static/logs/msft_analytics.log`:

```text
2025-05-12 15:57:14,252 – INFO  – Descargando Datos Desde Yahoo Finanzas...
2025-05-12 15:57:19,168 – INFO  – Guardando Datos En SQLite...
2025-05-12 15:57:19,230 – INFO  – Tabla msft_data Creada Con 9868 Registros.
2025-05-12 15:57:19,230 – INFO  – Base De Datos SQLite Generada En: …/historical.db
2025-05-12 15:57:19,261 – INFO  – Guardando Datos En CSV...
2025-05-12 15:57:19,336 – INFO  – Archivo CSV Generado En: …/historical.csv
2025-05-12 15:57:19,336 – INFO  – Proceso Completado Con Éxito.
```

---

## 8. Licencia y Autores 📝

**MIT © 2025**

**Integrantes**:

* Jhon Alexis Machado Rodríguez
* Julián José Martínez Camacho

IU Digital de Antioquia — Ingeniería de Software y Datos

---

## 9. Autores

<div align="center">
  <img src="https://www.iudigital.edu.co/images/11.-IU-DIGITAL.png" alt="IU Digital" width="350">

  ━━━━━━━━━━━━━━━━━━━━━━━

  <h1>📋 Evidencia de Aprendizaje 2<br>
  <sub>Proyecto Integrado V - Linea de Énfasis (Entrega 2)
<sub></h1>
  <h3>Segunda parte del Proyecto Integrador</h3>

  ━━━━━━━━━━━━━━━━━━━━━━━

  ### 👥 **Integrantes**
  **Jhon Alexis Machado Rodríguez**  
  **Julián José Martínez Camacho**

  ━━━━━━━━━━━━━━━━━━━━━━━

  #### 🎓 **Ingeniería de Software y Datos**  
  #### 🏛️ Institución Universitaria Digital de Antioquia  
  #### 📅 Semestre 9°  
  #### 📦 Proyecto Integrado V - Linea de Énfasis
  #### 🔖 PREICA2501B020128  
  #### 👨‍🏫🏫 Andres Felipe Callejas  

  ━━━━━━━━━━━━━━━━━━━━━━━

  **🗓 Domingo, 25 de Mayo del 2025**  

</div>

---