import re
import logging

logger = logging.getLogger("cloudmatchpdf")

class LatexValidator:
    @staticmethod
    def analyze(source: str) -> bool:
        """
        Analyzes LaTeX source code for common pitfalls without modifying it.
        Returns True if no critical issues are found, False otherwise.
        """
        issues = []
        lines = source.split('\n')
        
        # Regex for orphan underscores (Negative Lookbehind)
        underscore_pattern = re.compile(r'(?<!\\)_')

        for i, line in enumerate(lines, 1):
            line_content = line.strip()
            
            # Exclusion rules: Skip commands or math modes
            if not line_content or line_content.startswith('\\') or \
               any(delim in line for delim in ['$', r'\[', r'\(', r'\]', r'\)']):
                continue

            # Detect underscores in plain text
            if underscore_pattern.search(line):
                issues.append(f"Line {i}: Raw underscore '_' detected in plain text. "
                              f"This will likely cause a LaTeX compilation error.")

        # Environment balance check
        if "document" in source:
            begins = re.findall(r"\\begin\{([^*][^}]+)\}", source)
            ends = re.findall(r"\\end\{([^*][^}]+)\}", source)
            
            for env in begins:
                if env != "document" and env not in ends:
                    issues.append(f"CRITICAL: Environment '\\begin{{{env}}}' is missing a closing '\\end{{{env}}}'.")

        # Clinical Report Output
        if issues:
            print(f"\n{'!'*12} LATEX SYNTAX REVIEW {'!'*12}")
            for issue in issues:
                print(f"-> {issue}")
            print(f"{'!'*46}\n")
            return False 
        
        return True