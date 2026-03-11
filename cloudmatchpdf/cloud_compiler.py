import requests
import logging
import socket
from time import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


logger = logging.getLogger("cloudmatchpdf")
logging.basicConfig(level=logging.INFO)


def check_internet():
    """Verifica conexión a internet."""
    try:
        socket.create_connection(("8.8.8.8", 53), 2)
        return True
    except OSError:
        return False


class CloudCompiler:
    """
    Motor de compilación LaTeX en la nube.
    """

    def __init__(self, timeout=40):

        self.timeout = timeout

        self.headers = {
            "User-Agent": "CloudMatchPDF/1.0",
            "Accept": "*/*"
        }

        self.endpoints = [
            {
                "name": "LaTeXOnline (GET)",
                "method": "GET",
                "url": "https://latexonline.cc/compile",
                "param": "text"
            },
            {
                "name": "LaTeXOnline (POST)",
                "method": "POST",
                "url": "https://latexonline.cc/compile",
                "param": "text"
            },
            {
                "name": "TeXLive-Net",
                "method": "POST",
                "url": "https://texlive.net/cgi-bin/latexml.cgi",
                "param": "text" 
            }
        ]

    # Añadir servidor

    def add_endpoint(self, name, method, url, param="text"):
        """Permite añadir nuevos servidores."""
        self.endpoints.append({
            "name": name,
            "method": method,
            "url": url,
            "param": param
        })

    # request individual

    def _request(self, server, source):

        name = server["name"]

        try:

            logger.info(f"Conectando a {name}")

            start = time()

            if server["method"] == "GET":

                r = requests.get(
                    server["url"],
                    params={server["param"]: source},
                    headers=self.headers,
                    timeout=self.timeout
                )

            else:

                r = requests.post(
                    server["url"],
                    data={server["param"]: source},
                    headers=self.headers,
                    timeout=self.timeout
                )

            latency = time() - start

            logger.info(f"{name} status {r.status_code}")
            logger.info(f"{name} latency {latency:.2f}s")

            if r.status_code != 200:
                logger.warning(f"{name} respondió con HTTP {r.status_code}")
                return None

            # Detectar PDF
            if r.content.startswith(b"%PDF") or "application/pdf" in r.headers.get("Content-Type", ""):

                logger.info(f"{name} Compiló correctamente")

                return r.content

            # Guardar debug
            debug_file = f"debug_{name}_{int(time())}.txt"

            Path(debug_file).write_bytes(r.content)

            logger.warning(f"{name} No devolvió PDF")
            logger.warning(f"Respuesta guardada en {debug_file}")

            debug_file = f"debug_{name}_{int(time())}.txt"
            
            # Usamos un context manager explícito para asegurar la escritura
            with open(debug_file, "wb") as f:
                f.write(r.content)
                f.flush() # Forzamos la salida al disco físico
            
            logger.warning(f"{name} No devolvió PDF. Log guardado en {debug_file}")
            return None

        except Exception as e:

            logger.error(f"{name} Fallo: {e}")

        return None

    # compilación paralela

    def compile(self, source: str, output="output.pdf") -> bool:

        if not source.strip():
            logger.error("El código LaTeX está vacío")
            return False

        if not check_internet():
            logger.error("No hay conexión a internet")
            return False

        logger.info("Intentando compilación en paralelo")

        with ThreadPoolExecutor(max_workers=len(self.endpoints)) as executor:

            futures = {
                executor.submit(self._request, server, source): server
                for server in self.endpoints
            }

            for future in as_completed(futures):

                pdf = future.result()

                if pdf:

                    Path(output).write_bytes(pdf)

                    logger.info(f"PDF generado: {output}")

                    # cancelar otros servidores
                    for f in futures:
                        f.cancel()

                    return True

        logger.error("Todos los servidores fallaron")
        backup_tex = Path(output).with_suffix(".tex") # Cambia .pdf por .tex
        try:
            backup_tex.write_text(source, encoding="utf-8")
            logger.warning(f"Todos los servidores fallaron. Respaldo generado en: {backup_tex}")
        except Exception as e:
            logger.error(f"No se pudo generar el archivo de respaldo .tex: {e}")

        logger.error("Todos los servidores fallaron")
        return False

        return False
