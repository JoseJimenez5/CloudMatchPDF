import sympy as sp
import matplotlib.pyplot as plt
import io
import logging
from typing import List, Union, Optional
from pathlib import Path
import base64
from cloudmatchpdf.latex_validator import LatexValidator

logger = logging.getLogger("cloudmatchpdf")

class LatexBuilder:
    """
    Arquitecto de documentos LaTeX de alta fidelidad.
    Permite la construcción fluida de reportes científicos integrando 
    SymPy, Matplotlib (vía PGF) y archivos externos.
    """

    def __init__(self, title: str = "Escuela Politécnica Nacional (EPN)", author: str = "Jose Jimenez"):
        self._metadata = {
            "title": title, 
            "author": author, 
            "date": r"\today"
        }
        
        # Paquetes esenciales para rigor científico
        self.packages = {
            "inputenc": "utf8",
            "amsmath": None,
            "amsfonts": None,
            "amssymb": None,
            "geometry": "margin=1in",
            "graphicx": None,
            "physics": None,
            "mathtools": None,
            "float": None,      # Para posicionamiento estricto [H]
            "pgf": None         # Para renderizado vectorial de plots
        }
        
        self.elements: List[str] = []

    # --- Configuración Estructural (Fluent API) ---

    def set_title(self, title: str):
        self._metadata["title"] = title
        return self

    def set_author(self, author: str):
        self._metadata["author"] = author
        return self

    def add_package(self, name: str, options: Optional[str] = None):
        """Añade o actualiza un paquete en el preámbulo."""
        self.packages[name] = options
        return self

    def add_section(self, name: str, numbered: bool = True):
        cmd = "\\section" if numbered else "\\section*"
        self.elements.append(f"\n{cmd}{{{name}}}")
        return self

    def add_subsection(self, name: str, numbered: bool = True):
        cmd = "\\subsection" if numbered else "\\subsection*"
        self.elements.append(f"\n{cmd}{{{name}}}")
        return self

    # --- Inyección de Contenido ---

    def add_text(self, text: str):
        """Añade bloques de texto con soporte para saltos de línea."""
        self.elements.append(f"\n{text}\n")
        return self

    def add_equation(self, obj: Union[sp.Basic, sp.Matrix, str], subtitle: Optional[str] = None):
        """
        Convierte objetos SymPy o LaTeX crudo en ecuaciones centradas.
        """
        if subtitle:
            self.elements.append(f"\\paragraph{{{subtitle}}}")
        
        # Conversión inteligente: si es SymPy usa sp.latex, si es str lo deja crudo
        latex_str = sp.latex(obj) if not isinstance(obj, str) else obj
        self.elements.append(rf"\[ {latex_str} \]")
        return self

    def add_math_block(self, latex_str: str, numbered: bool = False):

        # Limpiamos posibles espacios en blanco laterales
        content = latex_str.strip()
        
        if numbered:
            block = f"\\begin{{equation}}\n  {content}\n\\end{{equation}}"
        else:
            block = f"\\[\n  {content}\n\\]"
            
        self.elements.append(block)
        logger.info(f"Builder: Añadido bloque matemático {'numerado' if numbered else 'estándar'}")


    # --- Integración Gráfica Vectorial (Nube-Safe) ---
    def add_plot(self, obj: Union[plt.Figure, str], caption: str = "Gráfica", x_range: str = "-2:2"):

        import numpy as np
        logger.info("")
        
        try:
            # 1. Obtención de datos (Fórmula o Figura)
            if isinstance(obj, str):
                func_str = obj.replace("exp", "np.exp").replace("sin", "np.sin").replace("cos", "np.cos")
                start, end = map(float, x_range.split(':'))
                x_s = np.linspace(start, end, 25) # Reducimos a 25 puntos para evitar archivos largos
                y_s = eval(func_str, {"np": np, "x": x_s})
            else:
                ax = obj.gca()
                line = ax.get_lines()[0]
                x_s, y_s = line.get_data()
                indices = np.linspace(0, len(x_s) - 1, 25, dtype=int)
                x_s, y_s = x_s[indices], y_s[indices]

            # 2. Normalización a enteros (0-100)
            x_n = ((x_s - x_s.min()) / (x_s.max() - x_s.min()) * 100).astype(int)
            y_n = ((y_s - y_s.min()) / (y_s.max() - y_s.min()) * 80).astype(int)

            # 3. Construcción con puntos y líneas básicas
            puntos = ""
            for i in range(len(x_n)):
                puntos += f"\\put({x_n[i]},{y_n[i]}){{\\circle*{{1.5}}}}"

            fig_latex = [
                "\\begin{figure}[H]",
                "  \\centering",
                "  \\setlength{\\unitlength}{0.6mm}",
                "  \\begin{picture}(100,90)",
                "    \\put(0,0){\\line(1,0){105}}", # Eje X
                "    \\put(0,0){\\line(0,1){85}}",  # Eje Y
                f"    {puntos}",
                "  \\end{picture}",
                f"  \\caption{{{caption}}}",
                "\\end{figure}"
            ]
            self.elements.append("\n".join(fig_latex))
            
        except Exception as e:
            logger.error(f"Fallo crítico final en add_plot: {e}")
            self.elements.append(f"\n% Error final en plot: {e}\n")
            
        return self
    
    # --- Utilidades de Archivos ---

    def import_file(self, file_path: Union[str, Path]):
        """Importa contenido de archivos externos (.txt, .tex) al cuerpo."""
        path = Path(file_path)
        if path.exists():
            content = path.read_text(encoding="utf-8")
            self.elements.append(f"\n% --- Inicio Importación: {path.name} ---\n{content}\n")
            logger.info(f"Archivo {path.name} importado correctamente.")
        else:
            logger.warning(f"No se pudo encontrar el archivo: {file_path}")
        return self

    # --- Generación Final de Código Fuente ---

    def _generate_preamble(self) -> str:
        lines = []
        lines.append("\\documentclass[12pt]{article}")
        
        for pkg, opt in self.packages.items():
            if opt:
                lines.append(f"\\usepackage[{opt}]{{{pkg}}}")
            else:
                lines.append(f"\\usepackage{{{pkg}}}")
        
        lines.append(f"\n\\title{{{self._metadata['title']}}}")
        lines.append(f"\\author{{{self._metadata['author']}}}")
        lines.append(f"\\date{{{self._metadata['date']}}}")
        return "\n".join(lines)

    def build(self) -> str:
      
        # 1. Generación del preámbulo (paquetes, título, autor)
        preamble = self._generate_preamble()
        
        # 2. Unión de todos los elementos del cuerpo (secciones, texto, plots)
        body = "\n".join(self.elements)
        
        # 3. Construcción del código LaTeX crudo
        raw_source = (
            f"{preamble}\n\n"
            f"\\begin{{document}}\n"
            f"\\maketitle\n\n"
            f"{body}\n\n"
            f"\\end{{document}}"
        )

        # 4. PASO DE RIGOR CIENTÍFICO: Autocuración
        # Aquí interceptamos el código para corregir guiones bajos, 
        # cerrar entornos matemáticos y asegurar dependencias.
        try:
            logger.info("Builder: Iniciando validación de sintaxis...")
            # Importante: Asegúrate de que LatexValidator esté importado en el archivo
            safe_source = LatexValidator.process(raw_source)
            return safe_source
        except Exception as e:
            logger.error(f"Error crítico en la validación: {e}")
            # En caso de fallo catastrófico del validador, retornamos el raw para no detener el flujo
            return raw_source

    def save_tex(self, filename: str = "output.tex"):
        """Guarda el código generado en un archivo local para depuración."""
        Path(filename).write_text(self.build(), encoding="utf-8")
        logger.info(f"Código fuente LaTeX guardado en {filename}")
        return self
