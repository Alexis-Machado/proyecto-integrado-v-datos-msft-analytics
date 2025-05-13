# proyecto-integrado-v-datos-msft-analytics 🚀

<div align="center">
  <h1>Proyecto Integrado V – Línea de Énfasis</h1>
  <h3>Entrega 1: Automatización de la recolección y análisis de datos históricos de MSFT (Microsoft) desde Yahoo Finanzas 📊</h3>
</div>

---

Este proyecto implementa **EA1 – Ingestión de Datos** para recolectar, transformar, persistir y auditar datos históricos de la acción **Microsoft Corporation (MSFT)** desde **Yahoo Finanzas**, empleando:

- **Python** 🐍
- **yfinance** 🤖
- **pandas** 📊
- **SQLite** 🗄️
- **CSV** 📑
- **GitHub Actions** 🤖 (CI/CD semanal)

---

## Contenido

1. [Descripción General](#descripción-general-🌟)  
2. [Características Principales](#características-principales-✨)  
3. [Estructura del Proyecto](#estructura-del-proyecto-📂)  
4. [Requerimientos Previos](#requerimientos-previos-✅)  
5. [Instalación y Setup](#instalación-y-setup-⚙️)  
6. [Uso Local](#uso-local-🚀)  
7. [Automatización con GitHub Actions](#automatización-con-github-actions-🤖)  
8. [Trazabilidad y Logging](#trazabilidad-y-logging-🪵)  
9. [Resultados Obtenidos](#resultados-obtenidos-📈)  
10. [Licencia y Autores](#licencia-y-autores-📝)
11. [Autores](#11-autores)

---

## 1. Descripción General 🌟

Desde su salida a bolsa el **13 de marzo de 1986**, MSFT ha generado **casi 40 años** de datos diarios (apertura, máximo, mínimo, cierre, volumen). Este proyecto:

- **Automatiza** la descarga de cotizaciones 📥  
- **Transforma** y estandariza formatos 🧹  
- **Persiste** el histórico de manera incremental en **SQLite** y **CSV** 🗄️📑  
- **Registra** cada paso con un **sistema de logging dual** (consola + archivo) 🪵  
- **Programa** actualizaciones diarias mediante **GitHub Actions** ⏰🤖  

Es la base para análisis cuantitativos, investigación académica y modelos predictivos.

---

## 2. Características Principales ✨

- **Descarga fiable** de Yahoo Finanzas (`yfinance`) hasta “mañana” para incluir el cierre más reciente.  
- **Columnas en español**: `Fecha`, `Abrir`, `Máx.`, `Mín.`, `Cerrar`, `Volumen`.  
- **Desglose de fecha** en `año`, `mes`, `día` para consultas granulares.  
- **Persistencia incremental**: sólo nuevos registros, sin duplicados.  
- **Formatos duales**:
  - **SQLite** (`static/data/historical.db`)  
  - **CSV**  (`static/data/historical.csv`)  
- **Trazabilidad completa** con logger que genera `static/logs/msft_analytics.log`.  
- **CLI**: comando `msft-collector` integrado en `setup.py`.  
- **CI/CD**: workflow diario (cron), manual (dispatch) y on-push en `.github/workflows/update_data.yml`.

---

## 3. Estructura del Proyecto 📂

```text
proyecto-integrado-v-datos-msft-analytics/
├── src/msft_analytics/
│   ├── collector.py         # Clase MSFTCollector
│   ├── logger.py            # Logger dual consola/archivo
│   └── static/
│       ├── data/
│       │   ├── historical.db     # Base SQLite
│       │   └── historical.csv    # Exportación CSV
│       └── logs/
│           └── msft_analytics.log
├── setup.py                 # Instalación y entry-point
├── requirements.txt         # pandas, yfinance
├── .github/
│   └── workflows/
│       └── update_data.yml  # CI: cron, dispatch, push
└── README.md                # (este archivo)
````

---

## 4. Requerimientos Previos ✅

Antes de ejecutar el proyecto, asegúrate de contar con:

* 🐍 **Python 3.8+**
* 🌐 **Internet** (para acceder a Yahoo Finanzas)
* 🔧 **Git** (clonación y CI)
* 🤖 **Cuenta en GitHub** para Actions

---

## 5. Instalación y Setup ⚙️

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
    version="1.0.0",  
    author="Jhon Alexis Machado Rodriguez",  
    author_email="jmachadoa12@gmail.com",  
    description="Proyecto Integrado V - Línea de Énfasis (Entrega 1): Automatización de la recolección y análisis de datos históricos del indicador MSFT (Microsoft) desde Yahoo Finanzas.",

    # Encontramos paquetes en la carpeta src
    packages=find_packages(where="src"), 
    # Definimos src como directorio raíz de código
    package_dir={"": "src"},  

    # Dependencias necesarias
    install_requires=[  
        "pandas",
        "yfinance",
    ],

    # Script de consola al instalar el paquete
    entry_points={  
        "console_scripts": [
            "msft-collector=msft_analytics.collector:run",
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

## 6. Uso Local 🚀

Tras configurar el entorno, ejecuta:

```bash
python src/msft_analytics/collector.py
```

> O simplemente:
>
> ```bash
> msft-collector
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

✔ **Archivo de log para auditoría:**
📝 Se registra toda la ejecución en `msft_analytics.log`, ubicado en `src/msft_analytics/static/logs/`.

✅ ¡Listo! El proceso de descarga, transformación, persistencia y auditoría de datos de **MSFT** se ha completado con éxito. 🎉

---

## 7. Automatización con GitHub Actions 🤖

El workflow `.github/workflows/update_data.yml` incluye:

```bash
name: 📈 Automatización de Datos Históricos MSFT

on:
  schedule:
    - cron: "0 0 * * *" # ⏰ Se Ejecuta Cada Día a La Medianoche (UTC)
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

      - name: 🚀 Ejecutar el colector
        run: |
          msft-collector

      - name: 📂 Configurar Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: 📤 Hacer commit de los datos actualizados
        run: |
          git add src/msft_analytics/static/data/*
          git add src/msft_analytics/static/logs/msft_analytics.log
          git commit -m "Actualización automática de datos MSFT [GitHub Actions]" || echo "No hay cambios para commitear"
          git push
```

* **cron**: 🤖 (diario a la medianoche 00:00 UTC)
* **workflow\_dispatch**: 🖱️ manual
* **push**: 🔀 a `main`

**Pasos**:

1. Checkout del repo
2. Setup Python 3.9
3. `pip install -e .`
4. `msft-collector`
5. Git commit & push de `historical.db` y `historical.csv` (si cambian)

---

## 8. Trazabilidad y Logging 🪵

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

## 9. Resultados Obtenidos 📈

* Histórico de MSFT desde 1986 completo y actualizado.
* Incremento diario 1 registro hábil o varios (sin duplicados).
* Datos accesibles para SQL, pandas, Excel, Tableau, Power BI.
* Base sólida para análisis de series temporales y ML.

---

## 10. Licencia y Autores 📝

**MIT © 2025**

**Integrantes**:

* Jhon Alexis Machado Rodríguez
* Julián José Martínez Camacho

IU Digital de Antioquia — Ingeniería de Software y Datos

---

## 11. Autores

<div align="center">
  <img src="https://www.iudigital.edu.co/images/11.-IU-DIGITAL.png" alt="IU Digital" width="350">

  ━━━━━━━━━━━━━━━━━━━━━━━

  <h1>📋 Evidencia de Aprendizaje 1<br>
  <sub>Proyecto Integrado V - Linea de Énfasis (Entrega 1)
<sub></h1>
  <h3>Primera parte del Proyecto Integrador</h3>

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

  **🗓 Lunes, 12 de Mayo del 2025**  

</div>

---