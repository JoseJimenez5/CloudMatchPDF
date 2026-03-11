from cloudmatchpdf.latex_validator import LatexValidator

def test_validator_passive_escape():
    # Caso 1: Texto plano con guion bajo (Debe escapar)
    input_text = "La variable energia_total es constante."
    output = LatexValidator.process(input_text)
    assert r"energia\_total" in output

    # Caso 2: Modo matemático (No debe tocar)
    math_text = r"\[ E_{total} = T + V \]"
    output_math = LatexValidator.process(math_text)
    assert "E_{total}" in output_math
    assert r"E\_total" not in output_math

def test_validator_env_closure():
    # Caso 3: Cierre de emergencia de entornos
    broken_latex = r"\begin{itemize} \item Prueba \end{document}"
    fixed = LatexValidator.process(broken_latex)
    assert r"\end{itemize}" in fixed
    assert fixed.find(r"\end{itemize}") < fixed.find(r"\end{document}")