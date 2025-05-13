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
