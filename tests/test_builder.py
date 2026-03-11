import pytest
import sympy as sp
from cloudmatchpdf.latex_builder import LatexBuilder

def test_builder_sympy_integration():
    doc = LatexBuilder(title="Test Rigor", author="Jose Jimenez")
    
    # Probamos una matriz (Álgebra Lineal / Data Science)
    m = sp.Matrix([[1, 0], [0, 1]])
    doc.add_math(m)
    
    # Probamos una integral (Física Teórica)
    x = sp.Symbol('x')
    f = sp.Integral(sp.exp(-x**2), x)
    doc.add_math(f, numbered=True)
    
    full_code = doc.build()
    
    # Verificaciones de integridad
    assert r"\begin{pmatrix}" in full_code
    assert r"\int e^{- x^{2}} \, dx" in full_code
    assert r"\begin{equation}" in full_code
    assert r"\mathtt" not in full_code  # Verificamos que se eliminó el error anterior