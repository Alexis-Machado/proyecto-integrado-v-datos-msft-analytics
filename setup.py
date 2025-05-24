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
