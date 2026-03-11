import re
import logging

logger = logging.getLogger("cloudmatchpdf")

class LatexValidator:
    @staticmethod
    def process(source: str) -> str:
        reparaciones = []
        lines = source.split('\n')
        fixed_lines = []

        # Regex para encontrar '_' que NO tengan '\' antes (Negative Lookbehind)
        # Solo lo aplicaremos en condiciones muy específicas.
        underscore_pattern = re.compile(r'(?<!\\)_')

        for line in lines:
            line_content = line.strip()
            
            # REGLAS DE EXCLUSIÓN (No tocar la línea si...)
            # 1. Es un comando (\section, \usepackage, etc.)
            # 2. Contiene delimitadores matemáticos ($, \[, \()
            # 3. Está vacía
            if not line_content or \
               line_content.startswith('\\') or \
               any(delim in line for delim in ['$', r'\[', r'\(', r'\]', r'\)']):
                fixed_lines.append(line)
                continue

            # Si pasa los filtros, es texto plano. Buscamos guiones bajos huérfanos.
            if underscore_pattern.search(line):
                new_line = underscore_pattern.sub(r'\_', line)
                if new_line != line:
                    reparaciones.append(f"Escape de '_' en texto: '{line_content[:15]}...' ")
                    line = new_line
            
            fixed_lines.append(line)

        final_source = '\n'.join(fixed_lines)

        # BALANCEO DE ENTORNOS (Solo inyecta si falta el cierre antes del final del documento)
        # Esto previene el error "Emergency stop" de LaTeX
        if "document" in final_source:
            # Buscamos entornos abiertos vs cerrados (excluyendo 'document')
            begins = re.findall(r"\\begin\{([^*][^}]+)\}", final_source)
            ends = re.findall(r"\\end\{([^*][^}]+)\}", final_source)
            
            for env in reversed(begins):
                if env != "document" and env not in ends:
                    final_source = final_source.replace(r"\end{document}", f"\\end{{{env}}}\n\\end{{document}}")
                    reparaciones.append(f"Cierre de emergencia del entorno: {env}")
                    ends.append(env) # Evita duplicar cierres

        if reparaciones:
            print(f"\n VALIDATOR: {len(reparaciones)} ajustes realizados.")
        
        return final_source