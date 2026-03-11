from cloudmatchpdf.cloud_compiler import CloudCompiler
from cloudmatchpdf.latex_builder import LatexBuilder
from cloudmatchpdf.latex_validator import LatexValidator
import sympy as sp

def ejecutar_deduccion_maestra():
    print("INICIANDO DEDUCCIÓN DE EULER-LAGRANGE (SISTEMA INTEGRADO)")
    
    doc = LatexBuilder(
        title="Deducción Formal de las Ecuaciones de Euler-Lagrange",
        author="Jose Jimenez"
    )

    # Introducción con guiones bajos intencionales para probar el validador pasivo
    doc.add_section("I. Planteamiento Variacional")
    doc.add_text("En la mecanica_lagrangiana, buscamos la evolucion_temporal del sistema "
                 "que minimiza la accion_funcional definida como la integral del Lagrangiano.")

    # Simbología con SymPy
    t = sp.Symbol('t')
    q = sp.Function('q')(t)
    dq = sp.diff(q, t)
    L = sp.Function('L')(q, dq, t)
    
    doc.add_text("Definimos el funcional de accion:")
    doc.add_equation(sp.Integral(L, t), subtitle="Accion de Hamilton")

    # Desarrollo matemático riguroso
    doc.add_section("II. Derivacion por Primeros Principios")
    doc.add_text(r"Consideramos una variacion $\delta q$ tal que los extremos son fijos:")
    doc.add_math_block(r"\delta S = \int_{t_1}^{t_2} \left( \frac{\partial L}{\partial q} \delta q + \frac{\partial L}{\partial \dot{q}} \delta \dot{q} \right) dt = 0")

    doc.add_text("Aplicando integracion_por_partes y el lema_fundamental del calculo variacional:")
    
    # Ecuación Final de Euler-Lagrange
    doc.add_section("III. Ecuaciones de Movimiento")
    doc.add_math_block(r"\frac{d}{dt} \left( \frac{\partial L}{\partial \dot{q}_i} \right) - \frac{\partial L}{\partial q_i} = 0", numbered=True)

    # --- FLUJO DE PRODUCCIÓN ---
    
    # 1. Build (Generación de código LaTeX)
    raw_source = doc.build()
    
    # 2. Validation (Filtro no intrusivo)
    safe_source = LatexValidator.process(raw_source)
    
    # 3. Compilation (Transmisión a la nube)
    compiler = CloudCompiler()
    if compiler.compile(safe_source, output="Deduccion_Final_EL.pdf"):
        print("\n¡INTEGRACIÓN TOTAL EXITOSA!")
        print("El PDF 'Deduccion_Final_EL.pdf' ha sido generado.")
    else:
        print("\nFALLO CRÍTICO: Revisa los logs del compilador.")

if __name__ == "__main__":
    ejecutar_deduccion_maestra()