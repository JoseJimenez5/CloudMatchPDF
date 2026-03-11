import pytest
from cloudmatchpdf.cloud_compiler import CloudCompiler
from cloudmatchpdf.latex_builder import LatexBuilder
from cloudmatchpdf.latex_validator import LatexValidator
def test_compiler_connectivity():
    compiler = CloudCompiler()
    # Código LaTeX minimalista pero válido
    valid_latex = r"\documentclass{article}\begin{document}Test\end{document}"
    
    # Probamos la compilación (esto requiere internet)
    # Usamos un nombre de archivo temporal para no ensuciar
    success = compiler.compile(valid_latex, output="test_output.pdf")
    
    assert success is True
    import os
    if os.path.exists("test_output.pdf"):
        os.remove("test_output.pdf")

def test_compiler_fail_handling():
    compiler = CloudCompiler()
    # Código LaTeX inválido que debería provocar un 400
    invalid_latex = r"\documentclass{article}\begin{document} \frac{1}{0} % Sin cerrar llave"
    
    success = compiler.compile(invalid_latex, output="fail.pdf")
    assert success is False