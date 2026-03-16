# CloudMatchPDF: Scientific Reporting Framework

**CloudMatchPDF** es un motor de automatización en Python diseñado para la generación de documentos LaTeX técnicos y académicos de alta precisión. El sistema integra el poder de **SymPy** para cálculo simbólico y **Matplotlib** para visualización vectorial, todo procesado mediante una infraestructura de compilación distribuida en la nube.

---

##  Características Principales

* **LatexBuilder (The Architect):** Arquitecto de documentos con API fluida. Permite inyectar ecuaciones de SymPy, bloques de código y gráficas vectoriales sin tocar una sola línea de código LaTeX.
* **Integración Gráfica (Cloud-Safe):** Renderizado de funciones matemáticas y figuras de Matplotlib mediante primitivas vectoriales de LaTeX, garantizando compatibilidad total con compiladores en la nube.
* **LatexValidator (The Shield):** Sistema de autocuración sintáctica que sanitiza caracteres reservados y asegura la integridad de los entornos matemáticos antes de la compilación.
* **CloudCompiler (The Bridge):** Motor de compilación asíncrona que utiliza *mirrors* distribuidos, eliminando la necesidad de instalaciones locales de TeX Live (+20GB).

---

##  Estructura del Proyecto

```bash
CloudMatchPDF/
<<<<<<< HEAD
├── cloudmatchpdf/          # Core del Framework
│   ├── latex_builder.py    # Arquitecto de documentos y Fluent API
│   ├── latex_validator.py  # Sanitización y validación de sintaxis
│   └── cloud_compiler.py   # Gestión de mirrors y peticiones API
├── tests/                  # Suite de Pruebas Unitarias
├── outputs/                # Directorio de salida de documentos (PDFs)
└── README.md
=======
├── src/                        # El contenedor de código fuente (obligatorio para el setup.py actual)
│   └── cloudmatchpdf/          # El paquete real (lo que se importa)
│       ├── __init__.py         # ¡FUNDAMENTAL! Expone las clases para importaciones limpias
│       ├── latex_builder.py    # Arquitecto de documentos
│       ├── latex_validator.py  # Sanitización y validación
│       └── cloud_compiler.py   # Gestión de mirrors y peticiones API
├── tests/                      # Suite de Pruebas Unitarias
├── outputs/                    # Directorio de salida (ignorado en el empaquetado)
├── setup.py                    # El mapa que apunta a src/
├── pyproject.toml              # Estándar de construcción moderno
└── README.md                   # Documentación técnica
```

---

##  Referencia Detallada de la API

### Clase `LatexBuilder`
Es el núcleo de la construcción lógica del documento. Soporta encadenamiento de métodos (Fluent API).

#### Configuración Estructural
* **`set_title(title)` / `set_author(author)`**: Define los metadatos del documento.
* **`add_package(name, options)`**: Registra nuevos paquetes en el preámbulo (ej. `geometry`, `physics`).
* **`add_section(name, numbered=True)`**: Crea secciones o secciones de tipo *asterisco*.

#### Inyección de Contenido
* **`add_text(text)`**: Añade párrafos con sanitización automática de caracteres reservados.
* **`add_equation(obj, subtitle)`**: Convierte automáticamente objetos **SymPy** o strings en ecuaciones centradas.
* **`add_math_block(latex_str, numbered)`**: Inyecta bloques matemáticos puros con control de numeración.
* **`add_plot(obj, caption, x_range)`**: 
    * **Funcionalidad:** Renderiza funciones matemáticas (como strings) o figuras de **Matplotlib** directamente en el PDF.
    * **Mecánica:** Traduce los datos a lenguaje `picture` de LaTeX para un acabado vectorial perfecto.

#### Utilidades y Generación
* **`import_file(path)`**: Importa contenido de archivos externos (.txt, .tex) directamente al cuerpo del reporte.
* **`build()`**: Ejecuta el pipeline de construcción y activa el `LatexValidator` para devolver un código fuente seguro.
* **`save_tex(filename)`**: Exporta el código generado a un archivo local para depuración.

---

##  Ejemplo Avanzado: Reporte Científico

```python
from cloudmatchpdf.latex_builder import LatexBuilder
from cloudmatchpdf.cloud_compiler import CloudCompiler
import sympy as sp

# Inicializar constructor con metadatos
doc = LatexBuilder(title="Análisis de Osciladores", author="Jose Jimenez")

# Construcción fluida
(doc.add_section("Cinemática del Sistema")
    .add_text("Se analiza la ecuación de movimiento para un sistema masa-resorte:")
    .add_equation(sp.Function('x')(sp.Symbol('t')), subtitle="Posición temporal")
    .add_plot(obj="sin(x) * exp(-0.1*x)", caption="Decaimiento de Amplitud", x_range="0:10")
)

# Compilación en la nube
compiler = CloudCompiler()
compiler.compile(doc.build(), output="Reporte_Cientifico.pdf")
```

---

##  Calidad y Rigor (QA)

El sistema mantiene integridad mediante pruebas automatizadas con **Pytest**:

```bash
pytest tests/
```

| Componente | Validación |
| :--- | :--- |
| **Builder** | Renderizado SymPy, Fluent API y manejo de metadatos. |
| **Validator** | Escape de guiones bajos (`_`), porcentajes (`%`) y cierre de entornos. |
| **Plotter** | Normalización de datos y generación de entorno `picture`. |
| **Compiler** | Disponibilidad de mirrors y manejo de errores HTTP. |

---

##  Reconocimientos
Este proyecto fue desarrollado como parte de un proceso de aprendizaje continuo y búsqueda de la excelencia técnica. Un agradecimiento especial a:
* **Harvard CS50P:** Por sentar las bases de la programación robusta en Python.
* **David J. Malan:** Por la inspiración y la metodología de enseñanza que impulsaron la creación de este framework.

---

##  Licencia y Créditos
Desarrollado por **Jose V. Jimenez**. Proyecto enfocado en la excelencia académica y la automatización científica para investigadores y estudiantes de ingeniería.
