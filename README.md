# CloudMatchPDF: Scientific Reporting Framework

**CloudMatchPDF** es un motor de automatización en Python diseñado para la generación de documentos $\LaTeX$ técnicos y académicos de alta precisión. El sistema integra el motor de cálculo simbólico de **SymPy** con una infraestructura de compilación distribuida en la nube, optimizando el flujo de trabajo editorial sin requerir instalaciones locales de TeX Live.

---

## Características Principales

* **LatexBuilder (The Architect):** Abstracción para la construcción de documentos complejos. Permite la inyección directa de objetos SymPy (matrices, tensores, integrales) eliminando la escritura manual de sintaxis $\LaTeX$.
* **LatexValidator (The Shield):** Sistema de validación pasiva que automatiza la corrección de errores de sintaxis comunes, asegurando la integridad del documento sin alterar los bloques matemáticos.
* **CloudCompiler (The Bridge):** Motor de compilación asíncrona mediante *mirrors* distribuidos (LaTeXOnline, TeXLive-Net). Genera archivos PDF en segundos, eliminando la necesidad de una instalación local de +20GB.
* **Agnosticismo de Dominio:** Arquitectura flexible aplicable a la física teórica, ingeniería mecánica y ciencia de datos.

---

## Estructura del Proyecto

```bash
CloudMatchPDF/
├── cloudmatchpdf/          # Core del Framework
│   ├── latex_builder.py    # Generación de estructuras y lógica de renderizado
│   ├── latex_validator.py  # Sanitización y seguridad de sintaxis
│   └── cloud_compiler.py   # Gestión de mirrors y peticiones API
├── tests/                  # Suite de Pruebas Unitarias
├── outputs/                # Directorio de salida de documentos (PDFs)
└── README.md
---
## Guía de Uso Rápido
1. Instalación de Dependencias
pip install sympy requests pytest

## 2. Ejemplo: Dinámica de Sistemas
from cloudmatchpdf.latex_builder import LatexBuilder
from cloudmatchpdf.cloud_compiler import CloudCompiler
import sympy as sp

# 1. Definición de variables simbólicas
I = sp.MatrixSymbol('I', 3, 3)
omega = sp.MatrixSymbol('omega', 3, 1)
L = I * omega

# 2. Construcción del reporte
doc = LatexBuilder(title="Momento Angular", author="Jose Jimenez")
doc.add_section("Formalismo Vectorial")
doc.add_text("Definición del momento angular $L$ mediante el tensor de inercia:")
doc.add_math(sp.Eq(sp.Symbol('L'), L), numbered=True)

# 3. Compilación remota
compiler = CloudCompiler()
compiler.compile(doc.build(), output="Momento_Angular.pdf")

 ## Validación y Calidad (QA)
El framework utiliza Pytest para garantizar la estabilidad de los módulos. Ejecute el siguiente comando para validar la integridad del sistema:Bashpytest tests/
MóduloObjetivo del TestBuilderValida el renderizado correcto de objetos SymPy y estructuras $\LaTeX$.ValidatorVerifica el escape automático de caracteres especiales en bloques de texto.CompilerTestea la latencia de mirrors y el manejo de excepciones HTTP (400/404).

## Licencia y Créditos
Desarrollado por Jose Jimenez. Proyecto enfocado en la excelencia académica y la automatización científica.

